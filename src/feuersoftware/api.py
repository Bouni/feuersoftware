import functools
import logging
from typing import Literal

import requests

from .models import CreateOperationModel, SetVehicleStatusModel

LOGGER = logging.getLogger("Feuersoftware")
BASE_URL = "https://connectapi.feuersoftware.com/interfaces/public"

DEFAULT_TIMEOUT = 10


class APIEndpointNotImplementedError(NotImplementedError):
    def __init__(self, endpoint: str, url: str):
        super().__init__(f"API endpoint '{endpoint}' ({url}) is not implemented.")


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
    def get_defect_report_attachment_abuse(self, attachmentId: int):
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

    def get_operations(self):
        url = f"{BASE_URL}/operation"
        return self._get(url)

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
        return f"{BASE_URL}/user"

    @not_implemented
    def put_user_availability(self, id: int, data: dict):
        return f"{BASE_URL}/user/{id}/availability/current"

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
        url = f"{BASE_URL}/user/useravailability"
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

    def get_vehicle_image(self, id: int | str):
        url = f"{BASE_URL}/vehicle/{id}"
        return self._get(url)

    def post_vehicle_status(self, id: int | str, data: dict):
        url = f"{BASE_URL}/vehicle/{id}/status"
        _data = SetVehicleStatusModel(**data)
        return self._post(url, _data.model_dump_json())

    def get_vehicle_status(self, id: int | str):
        url = f"{BASE_URL}/vehicle/{id}/status"
        return self._get(url)

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
        url = f"{BASE_URL}/wasserkarte/active"
        return self._get(url)

    def get_wasserkarte_hydrants(
        self, lat: float, lng: float, range: float, numItems: int
    ):
        url = f"{BASE_URL}/wasserkarte/active"
        return self._get(
            url,
            params={"lat": lat, "lng": lng, "range": range, "numItems": numItems},
        )
