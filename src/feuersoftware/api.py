import functools
import logging
from typing import Literal

import requests

from .models import CreateOperationModel, SetVehicleStatusModel

LOGGER = logging.getLogger("Feuersoftware")
ROOT_URL = "https://connectapi.feuersoftware.com/interfaces"
BASE_URL = f"{ROOT_URL}/public"
WASSERKARTE_URL = f"{ROOT_URL}/wasserkarte"

DEFAULT_TIMEOUT = 10


class APIEndpointNotImplementedError(NotImplementedError):
    def __init__(self, endpoint: str, url: str):
        super().__init__(f"API endpoint '{endpoint}' ({url}) is not implemented.")


def _drop_none(params: dict) -> dict | None:
    params = {k: v for k, v in params.items() if v is not None}
    return params or None


def _odata_params(
    filter: str | None = None,
    orderby: str | None = None,
    top: int | None = None,
    skip: int | None = None,
) -> dict:
    return {"$filter": filter, "$orderby": orderby, "$top": top, "$skip": skip}


def not_implemented(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        url = func(self, *args, **kwargs)
        raise APIEndpointNotImplementedError(func.__name__, url)

    return wrapper


class FeuersoftwareAPI:
    def __init__(self, token: str):
        self._headers = {
            "authorization": f"bearer {token}",
            "accept": "application/json",
            "content-type": "application/json",
        }

    def _request(
        self,
        method: str,
        url: str,
        data: str | None = None,
        params: dict | None = None,
    ) -> requests.Response | None:
        try:
            r = requests.request(
                method,
                url,
                headers=self._headers,
                data=data,
                params=params,
                timeout=DEFAULT_TIMEOUT,
            )
        except requests.exceptions.RequestException as err:
            LOGGER.error(f"{method} '{url}' failed: {err}")
            return None

        body_preview = r.text[:500]
        if not r.ok:
            LOGGER.error(f"{method} '{url}' failed: {r.status_code} - {body_preview}")
        else:
            LOGGER.info(f"{method} '{url}' success: {r.status_code}")
            LOGGER.debug(f"{method} '{url}' response body: {body_preview}")
        return r

    def _get(self, url: str, params: dict | None = None):
        return self._request("GET", url, params=params)

    def _post(self, url: str, data: str, params: dict | None = None):
        return self._request("POST", url, data=data, params=params)

    def _put(self, url: str, data: str, params: dict | None = None):
        return self._request("PUT", url, data=data, params=params)

    def _delete(self, url: str, params: dict | None = None):
        return self._request("DELETE", url, params=params)

    # ========================================================================
    # ALARMGROUP
    # ========================================================================

    def get_alarmgroup(self):
        url = f"{BASE_URL}/alarmgroup"
        return self._get(url)

    @not_implemented
    def put_alarmgroup(self, id: int):
        return f"{BASE_URL}/alarmgroup/{id}"

    # ========================================================================
    # APPOINTMENT
    # ========================================================================

    def get_appointments(
        self,
        filter: str | None = None,
        orderby: str | None = None,
        top: int | None = None,
        skip: int | None = None,
    ):
        """
        Results are sorted by start date ascending, at most 1000 items are
        returned. To get current and future appointments use
        filter="End ge YYYY-MM-DD" with today's date.
        """
        url = f"{BASE_URL}/appointment"
        params = _odata_params(filter, orderby, top, skip)
        return self._get(url, params=_drop_none(params))

    # ========================================================================
    # BILLING
    # ========================================================================

    def get_billing_accounts(self):
        url = f"{BASE_URL}/billing/account"
        return self._get(url)

    # ========================================================================
    # DEFECT REPORT
    # ========================================================================

    def get_defect_reports(self):
        url = f"{BASE_URL}/defectReport"
        return self._get(url)

    @not_implemented
    def post_defect_report(self, data: dict):
        return f"{BASE_URL}/defectReport"

    def get_defect_report_history(self, id: int):
        url = f"{BASE_URL}/defectReport/{id}/statusHistory"
        return self._get(url)

    def get_defect_report(self, id: int):
        url = f"{BASE_URL}/defectReport/{id}"
        return self._get(url)

    @not_implemented
    def put_defect_report(self, id: int, data: dict):
        return f"{BASE_URL}/defectReport/{id}"

    def delete_defect_report(self, id: int):
        url = f"{BASE_URL}/defectReport/{id}"
        return self._delete(url)

    @not_implemented
    def post_defect_report_attachment(self, id: int, data: dict):
        return f"{BASE_URL}/defectReport/{id}/attach"

    @not_implemented
    def put_defect_report_attachment_attach(self, id: int, attachmentId: int):
        return f"{BASE_URL}/defectReport/{id}/attach/{attachmentId}"

    def delete_defect_report_attachment(self, attachmentId: int):
        url = f"{BASE_URL}/defectReport/attach/{attachmentId}"
        return self._delete(url)

    @not_implemented
    def put_defect_report_attachment(self, attachmentId: int):
        return f"{BASE_URL}/defectReport/attach/{attachmentId}"

    @not_implemented
    def get_defect_report_attachment(self, attachmentId: int):
        return f"{BASE_URL}/defectReport/attach/{attachmentId}"

    @not_implemented
    def get_defect_report_attachment_url(self, attachmentId: int):
        return f"{BASE_URL}/defectReport/attach/url/{attachmentId}"

    @not_implemented
    def put_defect_report_attachment_abuse(self, attachmentId: int):
        return f"{BASE_URL}/defectReport/attachabuse/{attachmentId}"

    # ========================================================================
    # DEFECT REPORT CATEGORY
    # ========================================================================

    def get_defect_report_categories(self):
        url = f"{BASE_URL}/defectReportCategory"
        return self._get(url)

    @not_implemented
    def post_defect_report_category(self, data: dict):
        return f"{BASE_URL}/defectReportCategory"

    @not_implemented
    def put_defect_report_category(self, id: int, data: dict):
        return f"{BASE_URL}/defectReportCategory/{id}"

    def delete_defect_report_category(self, id: int):
        url = f"{BASE_URL}/defectReportCategory/{id}"
        return self._delete(url)

    # ========================================================================
    # DIAGNOSTICS
    # ========================================================================

    @not_implemented
    def post_diagnostics_upload_request(self, data: dict):
        return f"{BASE_URL}/diagnostics/upload-request"

    # ========================================================================
    # FUNCTION
    # ========================================================================

    def get_functions(self):
        url = f"{BASE_URL}/function"
        return self._get(url)

    # ========================================================================
    # GEOCODING
    # ========================================================================

    def get_geocoding(self, address: str):
        url = f"{BASE_URL}/geocoding"
        return self._get(url, params={"address": address})

    # ========================================================================
    # INFOBOARD
    # ========================================================================

    def get_infoboard(self):
        url = f"{BASE_URL}/infoboard"
        return self._get(url)

    @not_implemented
    def post_infoboard(self, data: dict):
        return f"{BASE_URL}/infoboard"

    def get_infoboard_info(self, id: int):
        url = f"{BASE_URL}/infoboard/{id}"
        return self._get(url)

    @not_implemented
    def put_infoboard_info(self, id: int, data: dict):
        return f"{BASE_URL}/infoboard/{id}"

    def delete_infoboard_info(self, id: int):
        url = f"{BASE_URL}/infoboard/{id}"
        return self._delete(url)

    def get_infoboard_groups(self):
        url = f"{BASE_URL}/infoboard/groups"
        return self._get(url)

    @not_implemented
    def post_infoboard_group(self, data: dict):
        return f"{BASE_URL}/infoboard/groups"

    @not_implemented
    def put_infoboard_group(self, id: int, data: dict):
        return f"{BASE_URL}/infoboard/groups/{id}"

    # ========================================================================
    # MAILING LISTS
    # ========================================================================

    def get_mailinglists(self):
        url = f"{BASE_URL}/mailinglists"
        return self._get(url)

    # ========================================================================
    # NEWS
    # ========================================================================

    def get_news(self):
        url = f"{BASE_URL}/news"
        return self._get(url)

    @not_implemented
    def post_news(self, data: dict):
        return f"{BASE_URL}/news"

    @not_implemented
    def put_news(self, id: int, data: dict):
        return f"{BASE_URL}/news/{id}"

    def delete_news(self, id: int):
        url = f"{BASE_URL}/news/{id}"
        return self._delete(url)

    # ========================================================================
    # OPERATION
    # ========================================================================

    def get_operations(
        self,
        only_latest: bool | None = None,
        filter: str | None = None,
        orderby: str | None = None,
        top: int | None = None,
        skip: int | None = None,
    ):
        """
        only_latest defaults to True on the server side (last 4 hours only),
        pass False to get the operation history. The server returns at most
        100 items per request, use top/skip (OData) to page through them.
        """
        url = f"{BASE_URL}/operation"
        params = {
            "onlyLatest": None if only_latest is None else str(only_latest).lower(),
            **_odata_params(filter, orderby, top, skip),
        }
        return self._get(url, params=_drop_none(params))

    def post_operation(
        self,
        data: dict,
        update_strategy: Literal[
            "none", "byNumber", "byAddress", "byPosition"
        ] = "none",
    ):
        url = f"{BASE_URL}/operation"
        _data = CreateOperationModel(**data)
        return self._post(
            url, _data.model_dump_json(), params={"updateStrategy": update_strategy}
        )

    def get_operation_message(self, id: str):
        url = f"{BASE_URL}/operation/{id}/message"
        return self._get(url)

    @not_implemented
    def post_operation_message(self, id: str, data: dict):
        return f"{BASE_URL}/operation/{id}/message"

    def get_operation_assignment(self, id: str):
        url = f"{BASE_URL}/operation/{id}/assignment"
        return self._get(url)

    @not_implemented
    def post_operation_assignment(self, id: str, data: dict):
        return f"{BASE_URL}/operation/{id}/assignment"

    def get_operation_user_status(self, id: str):
        url = f"{BASE_URL}/operation/{id}/userstatus"
        return self._get(url)

    @not_implemented
    def post_operation_user_status(self, data: dict):
        return f"{BASE_URL}/operation/userstatus"

    def get_operation_documentation(self, id: str):
        url = f"{BASE_URL}/operation/{id}/documentation"
        return self._get(url)

    @not_implemented
    def put_operation_documentation(self, id: str, data: dict):
        return f"{BASE_URL}/operation/{id}/documentation"

    @not_implemented
    def put_operation_assignment_crew(self, id: str, vehicle_id: str, data: dict):
        return f"{BASE_URL}/operation/{id}/assignment/{vehicle_id}/crew"

    def get_operation_assignment_users(self, id: str, vehicle_id: str):
        url = f"{BASE_URL}/operation/{id}/assignment/{vehicle_id}/users"
        return self._get(url)

    @not_implemented
    def post_operation_assignment_user(self, id: str, vehicle_id: str, data: dict):
        return f"{BASE_URL}/operation/{id}/assignment/{vehicle_id}/users"

    @not_implemented
    def put_operation_assignment_users(self, id: str, vehicle_id: str, data: list):
        return f"{BASE_URL}/operation/{id}/assignment/{vehicle_id}/users"

    def delete_operation_assignment_user(
        self, id: str, vehicle_id: str, user_assignment_id: int
    ):
        url = (
            f"{BASE_URL}/operation/{id}/assignment/{vehicle_id}"
            f"/users/{user_assignment_id}"
        )
        return self._delete(url)

    # ========================================================================
    # ORGANIZATION
    # ========================================================================

    def get_organization(self):
        url = f"{BASE_URL}/organization"
        return self._get(url)

    # ========================================================================
    # USER
    # ========================================================================

    def get_users(self):
        url = f"{BASE_URL}/user"
        return self._get(url)

    def get_user(self, id: int):
        url = f"{BASE_URL}/user/{id}"
        return self._get(url)

    @not_implemented
    def put_user(self, id: int, data: dict):
        return f"{BASE_URL}/user/{id}"

    def delete_user(self, id: int):
        url = f"{BASE_URL}/user/{id}"
        return self._delete(url)

    @not_implemented
    def post_user_invite(self, data: dict):
        return f"{BASE_URL}/user/invite"

    @not_implemented
    def put_user_availability(self, id: int, data: dict):
        return f"{BASE_URL}/user/{id}/availability/current"

    @not_implemented
    def patch_user(self, id: int, data: list):
        return f"{BASE_URL}/user/{id}"

    def get_user_profilepicture(self, id: int | str):
        url = f"{BASE_URL}/user/{id}/profilepicture"
        return self._get(url)

    # ========================================================================
    # USER API
    # ========================================================================

    def get_user_availablity(self, token: str, status: int, lifeTimeDays: int):
        url = f"{BASE_URL}/user/useravailability"
        return self._get(
            url,
            params={"token": token, "status": status, "lifeTimeDays": lifeTimeDays},
        )

    def get_user_status(
        self,
        token: str,
        status: int,
        driveTimeSeconds: int,
        driveDistanceMeters: int,
        siteId: int,
    ):
        url = f"{BASE_URL}/user/userstatus"
        return self._get(
            url,
            params={
                "token": token,
                "status": status,
                "driveTimeSeconds": driveTimeSeconds,
                "driveDistanceMeters": driveDistanceMeters,
                "siteId": siteId,
            },
        )

    # ========================================================================
    # VEHICLE
    # ========================================================================

    def get_vehicles(self):
        url = f"{BASE_URL}/vehicle"
        return self._get(url)

    # id can be either the vehicle id or the radio id. The server resolves
    # it according to identifier_preference, which defaults to
    # "PreferRadioId" on the server side.

    def get_vehicle_image(
        self, id: int | str, identifier_preference: str | None = None
    ):
        url = f"{BASE_URL}/vehicle/{id}/image"
        params = {"identifierPreference": identifier_preference}
        return self._get(url, params=_drop_none(params))

    def post_vehicle_status(
        self, id: int | str, data: dict, identifier_preference: str | None = None
    ):
        url = f"{BASE_URL}/vehicle/{id}/status"
        _data = SetVehicleStatusModel(**data)
        params = {"identifierPreference": identifier_preference}
        return self._post(url, _data.model_dump_json(), params=_drop_none(params))

    def get_vehicle_status(
        self, id: int | str, identifier_preference: str | None = None
    ):
        url = f"{BASE_URL}/vehicle/{id}/status"
        params = {"identifierPreference": identifier_preference}
        return self._get(url, params=_drop_none(params))

    # ========================================================================
    # VEHICLE AVAILABILITY
    # ========================================================================

    def get_vehicle_availabilities(
        self,
        id: int,
        filter: str | None = None,
        orderby: str | None = None,
        top: int | None = None,
        skip: int | None = None,
    ):
        """Current and future availabilities, sorted by start date ascending."""
        url = f"{BASE_URL}/vehicle/{id}/availability"
        params = _odata_params(filter, orderby, top, skip)
        return self._get(url, params=_drop_none(params))

    @not_implemented
    def post_vehicle_availability(self, id: int, data: dict):
        return f"{BASE_URL}/vehicle/{id}/availability"

    @not_implemented
    def put_vehicle_availability(self, id: int, availability_id: int, data: dict):
        return f"{BASE_URL}/vehicle/{id}/availability/{availability_id}"

    def delete_vehicle_availability(self, id: int, availability_id: int):
        url = f"{BASE_URL}/vehicle/{id}/availability/{availability_id}"
        return self._delete(url)

    # ========================================================================
    # VEHICLE CVM MODULE
    # ========================================================================

    def get_vehicle_cvms(self, id: int):
        url = f"{BASE_URL}/vehicle/{id}/cvm"
        return self._get(url)

    @not_implemented
    def post_vehicle_cvm(self, id: int, data: dict):
        return f"{BASE_URL}/vehicle/{id}/cvm"

    def get_vehicle_cvm(self, id: int, cvm_id: int):
        url = f"{BASE_URL}/vehicle/{id}/cvm/{cvm_id}"
        return self._get(url)

    @not_implemented
    def put_vehicle_cvm(self, id: int, cvm_id: int, data: dict):
        return f"{BASE_URL}/vehicle/{id}/cvm/{cvm_id}"

    def delete_vehicle_cvm(self, id: int, cvm_id: int):
        url = f"{BASE_URL}/vehicle/{id}/cvm/{cvm_id}"
        return self._delete(url)

    # ========================================================================
    # VEHICLE PROPERTIES
    # ========================================================================

    def get_vehicle_properties(self, id: int):
        url = f"{BASE_URL}/vehicle/{id}/properties"
        return self._get(url)

    @not_implemented
    def post_vehicle_properties(self, id: int, data: dict):
        return f"{BASE_URL}/vehicle/{id}/properties"

    # ========================================================================
    # WASSERKARTE
    # ========================================================================

    def get_wasserkarte_active(self):
        url = f"{WASSERKARTE_URL}/active"
        return self._get(url)

    def get_wasserkarte_hydrants(
        self, lat: float, lng: float, range: float, numItems: int
    ):
        url = f"{WASSERKARTE_URL}/hydrant"
        return self._get(
            url,
            params={"lat": lat, "lng": lng, "range": range, "numItems": numItems},
        )
