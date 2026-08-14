"""
Tests for feuersoftware.api.

Organized into:
- Regression tests for each fix made to api.py (see comments in api.py
  itself for the corresponding CHANGE numbers).
- Coverage of the plain GET/DELETE endpoints (parametrized, since they're
  all structurally identical: build a URL, call self._get/_delete).
- Coverage of the "not implemented" stub endpoints (parametrized).
- Coverage of the endpoints with request bodies or query parameters
  (post_operation, post_vehicle_status, get_geocoding, etc).
"""

import json

import pytest
import requests
from pydantic import ValidationError

from feuersoftware.api import (
    DEFAULT_TIMEOUT,
    APIEndpointNotImplementedError,
)

# ============================================================================
# CHANGE #1 regression test: delete_vehicle_cvm must issue a DELETE, not a GET
# ============================================================================


def test_delete_vehicle_cvm_sends_delete_not_get(api, base_url, requests_mock):
    """
    Regression test for the copy-paste bug where delete_vehicle_cvm called
    self._get(url) instead of self._delete(url). If this regresses, the
    GET-mock below would satisfy the call and the DELETE-mock would not
    have been hit, so we assert on requests_mock's call history directly
    rather than just checking the response.
    """
    url = f"{base_url}/vehicle/1/cvm/2"
    requests_mock.get(url, status_code=200, json={"should": "not be used"})
    requests_mock.delete(url, status_code=204)

    api.delete_vehicle_cvm(1, 2)

    assert requests_mock.call_count == 1
    assert requests_mock.last_request.method == "DELETE"


# ============================================================================
# CHANGE #2 / #3: timeout + exception handling in _request
# ============================================================================


def test_default_timeout_constant_is_set():
    # Simple guard that a timeout constant exists and is a sane positive
    # number, since requests_mock can't easily observe the timeout kwarg
    # that was actually passed to the transport layer.
    assert isinstance(DEFAULT_TIMEOUT, (int, float))
    assert DEFAULT_TIMEOUT > 0


@pytest.mark.parametrize(
    "exc",
    [
        requests.exceptions.ConnectionError("DNS resolution failed"),
        requests.exceptions.Timeout("request timed out"),
        requests.exceptions.RequestException("generic request failure"),
    ],
)
def test_request_returns_none_on_network_exception(
    api, base_url, requests_mock, exc, logs
):
    """
    Regression test for CHANGE #3: previously, any network exception
    (connection error, timeout, DNS failure) would propagate uncaught out
    of the library and crash the caller. Now it should be caught, logged,
    and result in None being returned instead of a Response object.
    """
    url = f"{base_url}/alarmgroup"
    requests_mock.get(url, exc=exc)

    result = api.get_alarmgroup()

    assert result is None
    assert "failed" in logs.error


def test_request_does_not_raise_on_ok_response(api, base_url, requests_mock):
    url = f"{base_url}/alarmgroup"
    requests_mock.get(url, status_code=200, json={"ok": True})

    result = api.get_alarmgroup()

    assert result is not None
    assert result.ok
    assert result.json() == {"ok": True}


def test_request_returns_response_on_http_error_status(api, base_url, requests_mock):
    """A non-2xx HTTP response is a valid Response, not a network exception,
    so it should still be returned (just logged as an error) rather than
    converted to None."""
    url = f"{base_url}/alarmgroup"
    requests_mock.get(url, status_code=403, text="forbidden")

    result = api.get_alarmgroup()

    assert result is not None
    assert not result.ok
    assert result.status_code == 403


# ============================================================================
# CHANGE #10: logging behavior (success at INFO/DEBUG, no full-body leakage
# at INFO)
# ============================================================================


def test_success_logs_status_but_not_full_body_at_info(
    api, base_url, requests_mock, logs
):
    long_body = "x" * 2000
    url = f"{base_url}/alarmgroup"
    requests_mock.get(url, status_code=200, text=long_body)

    api.get_alarmgroup()

    assert "200" in logs.info
    # The full 2000-char body should not be dumped at INFO level.
    assert long_body not in logs.info


def test_success_logs_truncated_body_at_debug(api, base_url, requests_mock, logs):
    long_body = "y" * 2000
    url = f"{base_url}/alarmgroup"
    requests_mock.get(url, status_code=200, text=long_body)

    api.get_alarmgroup()

    # First 500 chars should show up in the debug log...
    assert long_body[:500] in logs.debug
    # ...but not the full un-truncated body.
    assert long_body not in logs.debug


def test_failure_logs_error_with_status_and_body(api, base_url, requests_mock, logs):
    url = f"{base_url}/alarmgroup"
    requests_mock.get(url, status_code=500, text="server exploded")

    api.get_alarmgroup()

    assert "500" in logs.error
    assert "server exploded" in logs.error


# ============================================================================
# CHANGE #4: params-based query strings (URL-encoding safety)
# ============================================================================


def test_get_geocoding_url_encodes_special_characters(api, base_url, requests_mock):
    url = f"{base_url}/geocoding"
    requests_mock.get(url, status_code=200, json={})

    api.get_geocoding("Musterstraße 1 & Co")

    assert requests_mock.last_request.qs == {"address": ["musterstraße 1 & co"]}


def test_get_user_availablity_query_params(api, base_url, requests_mock):
    url = f"{base_url}/user/useravailability"
    requests_mock.get(url, status_code=200, json={})

    api.get_user_availablity(token="abc&def", status=1, lifeTimeDays=5)

    qs = requests_mock.last_request.qs
    assert qs["token"] == ["abc&def"]
    assert qs["status"] == ["1"]
    assert qs["lifetimedays"] == ["5"]


def test_get_user_status_query_params(api, base_url, requests_mock):
    url = f"{base_url}/user/useravailability"
    requests_mock.get(url, status_code=200, json={})

    api.get_user_status(
        token="abc",
        status=2,
        driveTimeSeconds=10,
        driveDistanceMeters=20,
        siteId=3,
    )

    qs = requests_mock.last_request.qs
    assert qs["token"] == ["abc"]
    assert qs["status"] == ["2"]
    assert qs["drivetimeseconds"] == ["10"]
    assert qs["drivedistancemeters"] == ["20"]
    assert qs["siteid"] == ["3"]


def test_get_wasserkarte_hydrants_query_params(api, base_url, requests_mock):
    url = f"{base_url}/wasserkarte/active"
    requests_mock.get(url, status_code=200, json={})

    api.get_wasserkarte_hydrants(lat=47.5990, lng=8.3348, range=300, numItems=5)

    qs = requests_mock.last_request.qs
    assert qs["lat"] == ["47.599"]
    assert qs["lng"] == ["8.3348"]
    assert qs["range"] == ["300"]
    assert qs["numitems"] == ["5"]


def test_post_operation_sends_update_strategy_as_query_param(
    api, base_url, requests_mock
):
    url = f"{base_url}/operation"
    requests_mock.post(url, status_code=200, json={})

    api.post_operation(
        {"Start": "2025-01-01T00:00:00Z", "Keyword": "Test"},
        update_strategy="byNumber",
    )

    assert requests_mock.last_request.qs == {"updatestrategy": ["bynumber"]}


def test_post_operation_sends_validated_json_body(api, base_url, requests_mock):
    url = f"{base_url}/operation"
    requests_mock.post(url, status_code=200, json={})

    api.post_operation({"Start": "2025-01-01T00:00:00Z", "Keyword": "Probealarm"})

    sent_body = json.loads(requests_mock.last_request.text)
    assert sent_body["Keyword"] == "Probealarm"
    assert sent_body["Start"].startswith("2025-01-01T00:00:00")


def test_post_operation_rejects_invalid_status(api):
    with pytest.raises(ValidationError):
        api.post_operation(
            {"Start": "2025-01-01T00:00:00Z", "Keyword": "Test", "Status": 99}
        )


def test_post_vehicle_status_sends_validated_json_body(api, base_url, requests_mock):
    url = f"{base_url}/vehicle/42/status"
    requests_mock.post(url, status_code=200, json={})

    api.post_vehicle_status(42, {"Status": 3, "Source": "ILS"})

    sent_body = json.loads(requests_mock.last_request.text)
    assert sent_body["Status"] == 3
    assert sent_body["Source"] == "ILS"


# ============================================================================
# CHANGE #13: _post/_put/_get all accept an optional params kwarg
# ============================================================================


def test_post_accepts_params_kwarg(api, base_url, requests_mock):
    url = f"{base_url}/operation"
    requests_mock.post(url, status_code=200, json={})

    # Calling the private helper directly to confirm the signature itself
    # (this is what previously raised "No parameter named params").
    api._post(url, data="{}", params={"updateStrategy": "byNumber"})

    assert requests_mock.last_request.qs == {"updatestrategy": ["bynumber"]}


def test_put_accepts_params_kwarg(api, base_url, requests_mock):
    url = f"{base_url}/some/put/endpoint"
    requests_mock.put(url, status_code=200, json={})

    api._put(url, data="{}", params={"foo": "bar"})

    assert requests_mock.last_request.qs == {"foo": ["bar"]}


def test_delete_accepts_params_kwarg(api, base_url, requests_mock):
    url = f"{base_url}/some/delete/endpoint"
    requests_mock.delete(url, status_code=204)

    api._delete(url, params={"foo": "bar"})

    assert requests_mock.last_request.qs == {"foo": ["bar"]}


# ============================================================================
# CHANGE #9: not_implemented decorator
# ============================================================================


NOT_IMPLEMENTED_CALLS = [
    ("put_alarmgroup", (5,)),
    ("post_defect_report", ({},)),
    ("put_defect_report", (1, {})),
    ("post_defect_report_attachment", (1, {})),
    ("put_defect_report_attachment_attach", (1, 2)),
    ("put_defect_report_attachment", (1,)),
    ("get_defect_report_attachment", (1,)),
    ("get_defect_report_attachment_url", (1,)),
    ("get_defect_report_attachment_abuse", (1,)),
    ("post_defect_report_category", ({},)),
    ("put_defect_report_category", (1, {})),
    ("post_news", ({},)),
    ("put_news", (1, {})),
    ("post_operation_message", ("1", {})),
    ("post_operation_assignment", ("1", {})),
    ("post_operation_user_status", ({},)),
    ("put_user", (1, {})),
    ("post_user_invite", ({},)),
    ("put_user_availability", (1, {})),
    ("post_vehicle_cvm", (1, {})),
    ("put_vehicle_cvm", (1, 2, {})),
    ("post_vehicle_properties", (1, {})),
]


@pytest.mark.parametrize("method_name, args", NOT_IMPLEMENTED_CALLS)
def test_not_implemented_endpoints_raise_without_network_call(
    api, requests_mock, method_name, args
):
    """
    Every stub endpoint should raise APIEndpointNotImplementedError and
    must NOT attempt any HTTP call in the process. No mocks are
    registered here on purpose: if the decorator regressed and let a
    real request slip through, requests_mock would raise its own
    NoMockAddress error instead of APIEndpointNotImplementedError,
    which would also fail this test (just with a different exception
    type), pointing at the actual bug.
    """
    method = getattr(api, method_name)
    with pytest.raises(APIEndpointNotImplementedError) as exc_info:
        method(*args)

    assert method_name in str(exc_info.value)
    assert requests_mock.call_count == 0


def test_not_implemented_error_message_includes_url(api):
    with pytest.raises(APIEndpointNotImplementedError) as exc_info:
        api.put_alarmgroup(5)

    message = str(exc_info.value)
    assert "put_alarmgroup" in message
    assert "/alarmgroup/5" in message


# ============================================================================
# Plain GET endpoints (parametrized: build URL, call self._get)
# ============================================================================


SIMPLE_GET_CALLS = [
    ("get_alarmgroup", (), "/alarmgroup"),
    ("get_billing_accounts", (), "/billing/account"),
    ("get_defect_reports", (), "/defectReport"),
    ("get_defect_report_history", (7,), "/defectReport/7/statusHistory"),
    ("get_defect_report", (7,), "/defectReport/7"),
    ("get_defect_report_categories", (), "/defectReportCategory"),
    ("get_functions", (), "/function"),
    ("get_news", (), "/news"),
    ("get_operations", (), "/operation"),
    ("get_operation_message", ("op-1",), "/operation/op-1/message"),
    ("get_operation_assignment", ("op-1",), "/operation/op-1/assignment"),
    ("get_operation_user_status", ("op-1",), "/operation/op-1/userstatus"),
    ("get_organization", (), "/organization"),
    ("get_users", (), "/user"),
    ("get_user", (3,), "/user/3"),
    ("get_vehicles", (), "/vehicle"),
    ("get_vehicle_image", (9,), "/vehicle/9"),
    ("get_vehicle_status", (9,), "/vehicle/9/status"),
    ("get_vehicle_cvms", (9,), "/vehicle/9/cvm"),
    ("get_vehicle_cvm", (9, 2), "/vehicle/9/cvm/2"),
    ("get_vehicle_properties", (9,), "/vehicle/9/properties"),
    ("get_wasserkarte_active", (), "/wasserkarte/active"),
]


@pytest.mark.parametrize("method_name, args, path", SIMPLE_GET_CALLS)
def test_simple_get_endpoints(api, base_url, requests_mock, method_name, args, path):
    url = f"{base_url}{path}"
    requests_mock.get(url, status_code=200, json={"data": "ok"})

    result = getattr(api, method_name)(*args)

    assert result is not None
    assert result.ok
    assert requests_mock.last_request.method == "GET"


# ============================================================================
# Plain DELETE endpoints (parametrized)
# ============================================================================


SIMPLE_DELETE_CALLS = [
    ("delete_defect_report", (7,), "/defectReport/7"),
    ("delete_defect_report_attachment", (11,), "/defectReport/attach/11"),
    ("delete_defect_report_category", (4,), "/defectReportCategory/4"),
    ("delete_news", (2,), "/news/2"),
    ("delete_user", (3,), "/user/3"),
    ("delete_vehicle_cvm", (9, 2), "/vehicle/9/cvm/2"),
]


@pytest.mark.parametrize("method_name, args, path", SIMPLE_DELETE_CALLS)
def test_simple_delete_endpoints(api, base_url, requests_mock, method_name, args, path):
    url = f"{base_url}{path}"
    requests_mock.delete(url, status_code=204)

    result = getattr(api, method_name)(*args)

    assert result is not None
    assert result.ok
    assert requests_mock.last_request.method == "DELETE"
