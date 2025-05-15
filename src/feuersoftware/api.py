import inspect
import json
import logging
from typing import Literal

import requests
from .models import CreateOperationModel, SetVehicleStatusModel

LOGGER = logging.getLogger("Feuersoftware")
BASE_URL = "https://connectapi.feuersoftware.com/interfaces/public"


class APIEndpointNotImplementedError(NotImplementedError):
    def __init__(self, endpoint: str, url: str):
        super().__init__(f"API endpoint '{endpoint}' ({url}) is not implemented.")


class FeuersoftwareAPI(object):
    def __init__(self, token: str):
        self._headers = {
            "authorization": f"bearer {token}",
            "accept": "application/json",
            "content-type": "application/json",
        }

    def _get_current_method_name(self, default="unknown"):
        frame = inspect.currentframe()
        return frame.f_back.f_code.co_name if frame and frame.f_back else default

    def _get(self, url: str):
        r = requests.get(url, headers=self._headers)
        if not r.ok:
            LOGGER.error(f"GET '{url}' failed: {r.status_code} - {r.text}")
        else:
            LOGGER.info(f"GET '{url}' success: {r.status_code} - {r.text}")
        return r

    def _post(self, url: str, data: str):
        r = requests.post(url, headers=self._headers, data=data)
        if not r.ok:
            LOGGER.error(f"POST '{url}' failed: {r.status_code} - {r.text}")
        else:
            LOGGER.info(f"POST '{url}' success: {r.status_code} - {r.text}")
        return r

    def _put(self, url: str, data: str):
        r = requests.put(url, headers=self._headers, data=data)
        if not r.ok:
            LOGGER.error(f"PUT '{url}' failed: {r.status_code} - {r.text}")
        else:
            LOGGER.info(f"PUT '{url}' success: {r.status_code} - {r.text}")
        return r

    def _delete(self, url: str):
        r = requests.delete(url, headers=self._headers)
        if not r.ok:
            LOGGER.error(f"DELETE '{url}' failed: {r.status_code} - {r.text}")
        else:
            LOGGER.info(f"DELETE '{url}' success: {r.status_code} - {r.text}")
        return r

    # ========================================================================
    # ALARMGROUP
    # ========================================================================

    def get_alarmgroup(self):
        url = f"{BASE_URL}/alarmgroup"
        return self._get(url)

    def put_alarmgroup(self, id: int):
        url = f"{BASE_URL}/alarmgroup/{id}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

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

    def post_defect_report(self, data: dict):
        url = f"{BASE_URL}/defectReport"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def get_defect_report_history(self, id: int):
        url = f"{BASE_URL}/defectReport/{id}/statusHistory"
        return self._get(url)

    def get_defect_report(self, id: int):
        url = f"{BASE_URL}/defectReport/{id}"
        return self._get(url)

    def put_defect_report(self, id: int, data: dict):
        url = f"{BASE_URL}/defectReport/{id}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def delete_defect_report(self, id: int):
        url = f"{BASE_URL}/defectReport/{id}"
        return self._delete(url)

    def post_defect_report_attachment(self, id: int, data: dict):
        url = f"{BASE_URL}/defectReport/{id}/attach"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def put_defect_report_attachment_attach(self, id: int, attachmentId: int):
        url = f"{BASE_URL}/defectReport/{id}/attach/{attachmentId}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def delete_defect_report_attachment(self, attachmentId: int):
        url = f"{BASE_URL}/defectReport/attach/{attachmentId}"
        return self._delete(url)

    def put_defect_report_attachment(self, attachmentId: int):
        url = f"{BASE_URL}/defectReport/attach/{attachmentId}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def get_defect_report_attachment(self, attachmentId: int):
        url = f"{BASE_URL}/defectReport/attach/{attachmentId}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def get_defect_report_attachment_url(self, attachmentId: int):
        url = f"{BASE_URL}/defectReport/attach/url/{attachmentId}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def get_defect_report_attachment_abuse(self, attachmentId: int):
        url = f"{BASE_URL}/defectReport/attachabuse/{attachmentId}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    # ========================================================================
    # DEFECT REPORT CATEGORY
    # ========================================================================

    def get_defect_report_categories(self):
        url = f"{BASE_URL}/defectReportCaregory"
        return self._get(url)

    def post_defect_report_category(self, data: dict):
        url = f"{BASE_URL}/defectReportCaregory"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def put_defect_report_category(self, id: int, data: dict):
        url = f"{BASE_URL}/defectReportCaregory/{id}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def delete_defect_report_category(self, id: int):
        url = f"{BASE_URL}/defectReportCaregory/{id}"
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
        url = f"{BASE_URL}/geocoding?address={address}"
        return self._get(url)

    # ========================================================================
    # NEWS
    # ========================================================================

    def get_news(self):
        url = f"{BASE_URL}/news"
        return self._get(url)

    def post_news(self, data: dict):
        url = f"{BASE_URL}/news"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def put_news(self, id: int, data: dict):
        url = f"{BASE_URL}/news/{id}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

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
        url = f"{BASE_URL}/operation?updateStrategy={update_strategy}"
        _data = CreateOperationModel(**data)
        return self._post(url, _data.model_dump_json())

    def get_operation_message(self, id: str):
        url = f"{BASE_URL}/operation/{id}/message"
        return self._get(url)

    def post_operation_message(self, id: str, data: dict):
        url = f"{BASE_URL}/operation/{id}/message"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def get_operation_assignment(self, id: str):
        url = f"{BASE_URL}/operation/{id}/assignment"
        return self._get(url)

    def post_operation_assignment(self, id: str, data: dict):
        url = f"{BASE_URL}/operation/{id}/assignment"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def get_operation_user_status(self, id: str):
        url = f"{BASE_URL}/operation/{id}/userstatus"
        return self._get(url)

    def post_operation_user_status(self, data: dict):
        url = f"{BASE_URL}/operation/userstatus"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

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

    def put_user(self, id: int, data: dict):
        url = f"{BASE_URL}/user/{id}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def delete_user(self, id: int):
        url = f"{BASE_URL}/user/{id}"
        return self._delete(url)

    def post_user_invite(self, data: dict):
        url = f"{BASE_URL}/user"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def put_user_availability(self, id: int, data: dict):
        url = f"{BASE_URL}/user/{id}/availability/current"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    # ========================================================================
    # USER API
    # ========================================================================

    def get_user_availablity(self, token: str, status: int, lifeTimeDays: int):
        url = f"{BASE_URL}/user/useravailability?token={token}&status={status}&lifeTimeDays={lifeTimeDays}"
        return self._get(url)

    def get_user_status(
        self,
        token: str,
        status: int,
        driveTimeSeconds: int,
        driveDistanceMeters: int,
        siteId: int,
    ):
        url = f"{BASE_URL}/user/useravailability?token={token}&status={status}&driveTimeSeconds={driveTimeSeconds}&driveDistanceMeters={driveDistanceMeters}&siteId={siteId}"
        return self._get(url)

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

    def post_vehicle_cvm(self, id: int, data: dict):
        url = f"{BASE_URL}/vehicle/{id}/cvm"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def get_vehicle_cvm(self, id: int, cvm_id: int):
        url = f"{BASE_URL}/vehicle/{id}/cvm/{cvm_id}"
        return self._get(url)

    def put_vehicle_cvm(self, id: int, cvm_id: int, data: dict):
        url = f"{BASE_URL}/vehicle/{id}/cvm/{cvm_id}"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    def delete_vehicle_cvm(self, id: int, cvm_id: int):
        url = f"{BASE_URL}/vehicle/{id}/cvm/{cvm_id}"
        return self._get(url)

    # ========================================================================
    # VEHICLE PROPERTIES
    # ========================================================================

    def get_vehicle_properties(self, id: int):
        url = f"{BASE_URL}/vehicle/{id}/properties"
        return self._get(url)

    def post_vehicle_properties(self, id: int, data: dict):
        url = f"{BASE_URL}/vehicle/{id}/properties"
        raise APIEndpointNotImplementedError(self._get_current_method_name(), url)

    # ========================================================================
    # WASSERKARTE
    # ========================================================================

    def get_wasserkarte_active(self):
        url = f"{BASE_URL}/wasserkarte/active"
        return self._get(url)

    def get_wasserkarte_hydrants(
        self, lat: float, lng: float, range: float, numItems: int
    ):
        url = f"{BASE_URL}/wasserkarte/active?lat={lat}&lng={lng}&range={range}&numItems={numItems}"
        return self._get(url)

