# Feuersoftware

Feuersoftware is a library that allow you to interact with the [Feuersoftware Connect Public API](https://connectapi.feuersoftware.com/swagger/index.html).

All routes of the public API are implemented. Request bodies are passed as
plain dicts (or lists of dicts) and validated with pydantic before they are
sent, so invalid data raises a `pydantic.ValidationError` without hitting the API.
Only the fields you pass are sent.

## Installation

```sh
pip install feuersoftware
```

## Setup the API

```python
from feuersoftware import FeuersoftwareAPI

TOKEN = '2xgRoQfoMGb4IveCDJIZqOO1l8hZZ5jT5mAw7SSk1otrFSq50IA2HIYB3luEpv7Vw8BWwG'\
        'Y2zV96VUkOF3FCZs2OP03qaTWF3CDrUHOKndvLIFTTgx0FCMBTFBRF1DfG4g3rs8BSMHB4'\
        '6qph1AlxOZ6parmJlp90V3GQB4EoI6DFdKE4SZeBuu46mXoaDlSmpTTS3FCpeG7oEUJVgy'\
        'pLZkZSFPRng5HdKhp6HG2XmNIMAtKTG3DAUWuKRi3cZ4JstLj05y4r7jt81g4DYXz9gVYc'\
        'UWk2pOkIZ9RPmu0s4LlaXHEK3TJlxLIUt5eHIzPUVKXyhdJDckviPsTYNfRxkpcNGd0vAb'\
        'zfzwMadgb4xaOi1v6ZpsRfXyOPgpudcnO6rwwi9TlAWNZ2075CO7HVFEP31yGhXmYsdFwj'\
        'ne3UIraWovMWHqeyv2yQLigKLePDAgXYUFqQpZ9P5ScznSMUg0ZnxS0Miy0qKe9zDYtqTk'\
        'qQVwrUGfGVFp4Ti83NJLCCGUOCmF0ovOB28mYyQIqGAi2MDaNIuAvz6HT1tGAo5nYdzOeu'

api = FeuersoftwareAPI(TOKEN)
```

## Return values

Every method returns the `requests.Response` of the call, or `None` if the
request could not be sent at all (connection error, timeout, ...). Failed
requests (non 2xx status codes) are logged to the `Feuersoftware` logger but
not raised, so check the response yourself:

```python
r = api.get_vehicles()
if r is not None and r.ok:
    vehicles = r.json()
```

## OData queries

`get_operations`, `get_appointments` and `get_vehicle_availabilities` accept
the optional OData arguments `filter`, `orderby`, `top` and `skip`:

```python
api.get_appointments(filter="End ge 2025-05-15", orderby="Start desc", top=10)
```

## Enums

Fields that take an enum value accept plain integers or the `IntEnum`s from
`feuersoftware.models`:

| Enum                   | Values                                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| `AvailabilityStatus`   | `Available` (0), `LimitedAvailable` (1), `NotAvailable` (2)                                            |
| `AvailabilitySource`   | `None_` (0), `Manual` (1), `Pager` (2), `Auto` (3), `Scheduled` (4), `ScheduledRecurring` (5), `UserApi` (6) |
| `DefectReportStatus`   | `Reported` (0), `Reviewed` (1), `InProgress` (2), `Resolved` (3), `Rejected` (4), `Paused` (5)         |
| `DefectReportPriority` | `Low` (0), `Medium` (1), `High` (2)                                                                    |
| `NewsCategory`         | `Announcement` (0), `TrafficObstruction` (1), `FasNotification` (2)                                    |
| `NewsType`             | `SiteNews` (0), `OrganizationNews` (1)                                                                 |
| `SiteInfoType`         | `PhoneNumber` (0), `EmailAddress` (1), `WebReference` (2), `DocumentReference` (3), `Text` (4)         |
| `UserOperationStatus`  | `NotSet` (0), `Coming` (1), `NotComing` (2), `ComingLater` (3)                                         |
| `VehiclePropertyType`  | `String` (0), `Integer` (1), `Double` (2), `Boolean` (3), `DateTime` (4)                               |
| `VehicleUserPosition`  | `None_` (0), `Leader` (1), `Driver` (2)                                                                |

# Endpoints

## Alarm groups

| Method                         | HTTP                          |
| ------------------------------ | ----------------------------- |
| `get_alarmgroup()`             | `GET /alarmgroup`             |
| `put_alarmgroup(id, data)`     | `PUT /alarmgroup/{id}`        |

```python
api.put_alarmgroup(42, {
    "Name": "Vollalarm",
    "Users": [{"Email": "jane@example.com", "UserName": "jane"}],
})
```

## Appointments

| Method                                          | HTTP               |
| ----------------------------------------------- | ------------------ |
| `get_appointments(filter, orderby, top, skip)`  | `GET /appointment` |

Results are sorted by start date ascending, at most 1000 items are returned.
To get current and future appointments filter by today's date:

```python
api.get_appointments(filter="End ge 2025-05-15")
```

## Billing

| Method                    | HTTP                   |
| ------------------------- | ---------------------- |
| `get_billing_accounts()`  | `GET /billing/account` |

## Defect reports

| Method                                                       | HTTP                                          |
| ------------------------------------------------------------ | --------------------------------------------- |
| `get_defect_reports()`                                       | `GET /defectReport`                           |
| `post_defect_report(data)`                                   | `POST /defectReport`                          |
| `get_defect_report(id)`                                      | `GET /defectReport/{id}`                      |
| `put_defect_report(id, data)`                                | `PUT /defectReport/{id}`                      |
| `delete_defect_report(id)`                                   | `DELETE /defectReport/{id}`                   |
| `get_defect_report_history(id)`                              | `GET /defectReport/{id}/statusHistory`        |
| `post_defect_report_attachment(id, data)`                    | `POST /defectReport/{id}/attach`              |
| `put_defect_report_attachment_attach(id, attachmentId, ok)`  | `PUT /defectReport/{id}/attach/{attachmentId}`|
| `get_defect_report_attachment(attachmentId)`                 | `GET /defectReport/attach/{attachmentId}`     |
| `put_defect_report_attachment(attachmentId, data)`           | `PUT /defectReport/attach/{attachmentId}`     |
| `delete_defect_report_attachment(attachmentId)`              | `DELETE /defectReport/attach/{attachmentId}`  |
| `get_defect_report_attachment_url(attachmentId)`             | `GET /defectReport/attach/url/{attachmentId}` |
| `put_defect_report_attachment_abuse(attachmentId, data)`     | `PUT /defectReport/attachabuse/{attachmentId}`|

```python
from feuersoftware.models import DefectReportPriority, DefectReportStatus

api.post_defect_report({
    "SiteId": 1,
    "Status": DefectReportStatus.Reported,
    "Priority": DefectReportPriority.High,
    "ShortDescription": "Blaulicht defekt",
    "DetailedDescription": "Das linke Blaulicht auf dem Dach blinkt nicht mehr.",
    "VehicleId": 12345678,
})
```

Attachments are added in two steps: register the file metadata, then confirm
(`ok=True`) or discard (`ok=False`) the attachment:

```python
api.post_defect_report_attachment(17, {
    "Name": "foto.jpg",
    "Size": 123456,
    "MimeType": "image/jpeg",
})
api.put_defect_report_attachment_attach(17, attachmentId=99, ok=True)
```

`get_defect_report_attachment` follows the server redirect to the file, so the
response body is the file itself.

> [!NOTE]
> The API spec only states that the body of `put_defect_report_attachment`
> and `put_defect_report_attachment_abuse` is a JSON string, it doesn't
> document what the string is for.

## Defect report categories

| Method                                   | HTTP                                |
| ---------------------------------------- | ----------------------------------- |
| `get_defect_report_categories()`         | `GET /defectReportCategory`         |
| `post_defect_report_category(data)`      | `POST /defectReportCategory`        |
| `put_defect_report_category(id, data)`   | `PUT /defectReportCategory/{id}`    |
| `delete_defect_report_category(id)`      | `DELETE /defectReportCategory/{id}` |

```python
api.post_defect_report_category({"Name": "Fahrzeugtechnik", "SiteId": 1})
api.put_defect_report_category(3, {"Name": "Fahrzeuge"})
```

## Diagnostics

| Method                                                                         | HTTP                                  |
| ------------------------------------------------------------------------------ | ------------------------------------- |
| `post_diagnostics_upload_request(data, monitor_timestamp, monitor_signature)`  | `POST /diagnostics/upload-request`    |

`monitor_timestamp` and `monitor_signature` are sent as the
`X-Monitor-Timestamp` and `X-Monitor-Signature` headers if given.

```python
api.post_diagnostics_upload_request({
    "Message": "Monitor crashed",
    "MonitorName": "Wache 1",
    "MonitorVersion": "1.2.3",
    "OsInfo": "Windows",
    "OsVersion": "11",
})
```

## Functions

| Method             | HTTP            |
| ------------------ | --------------- |
| `get_functions()`  | `GET /function` |

## Geocoding

| Method                    | HTTP             |
| ------------------------- | ---------------- |
| `get_geocoding(address)`  | `GET /geocoding` |

```python
api.get_geocoding("Hauptstraße 1, 79761 Waldshut-Tiengen")
```

## Infoboard

| Method                            | HTTP                           |
| --------------------------------- | ------------------------------ |
| `get_infoboard()`                 | `GET /infoboard`               |
| `post_infoboard(data)`            | `POST /infoboard`              |
| `get_infoboard_info(id)`          | `GET /infoboard/{id}`          |
| `put_infoboard_info(id, data)`    | `PUT /infoboard/{id}`          |
| `delete_infoboard_info(id)`       | `DELETE /infoboard/{id}`       |
| `get_infoboard_groups()`          | `GET /infoboard/groups`        |
| `post_infoboard_group(data)`      | `POST /infoboard/groups`       |
| `put_infoboard_group(id, data)`   | `PUT /infoboard/groups/{id}`   |

```python
from feuersoftware.models import SiteInfoType

api.post_infoboard_group({"Name": "Telefonnummern", "SiteId": 1})
api.post_infoboard({
    "InfoGroupId": 5,
    "Description": "Leitstelle",
    "InfoType": SiteInfoType.PhoneNumber,
    "Value": "+49 7751 12345",
})
```

## Mailing lists

| Method                 | HTTP                |
| ---------------------- | ------------------- |
| `get_mailinglists()`   | `GET /mailinglists` |

## News

| Method                         | HTTP                 |
| ------------------------------ | -------------------- |
| `get_news()`                   | `GET /news`          |
| `post_news(data, news_type)`   | `POST /news`         |
| `put_news(id, data)`           | `PUT /news/{id}`     |
| `delete_news(id)`              | `DELETE /news/{id}`  |

`news_type` defaults to `NewsType.SiteNews` on the server side.

```python
from feuersoftware.models import NewsCategory, NewsType

api.post_news(
    {
        "Title": "Übung",
        "Content": "Am Freitag findet eine Übung statt.",
        "Start": "2025-05-15",
        "End": "2025-05-16",
        "Category": NewsCategory.Announcement,
    },
    news_type=NewsType.OrganizationNews,
)
```

## Operations

| Method                                                                   | HTTP                                                          |
| ------------------------------------------------------------------------ | ------------------------------------------------------------- |
| `get_operations(only_latest, filter, orderby, top, skip)`                | `GET /operation`                                              |
| `post_operation(data, update_strategy)`                                  | `POST /operation`                                             |
| `get_operation_message(id)`                                              | `GET /operation/{id}/message`                                 |
| `post_operation_message(id, data)`                                       | `POST /operation/{id}/message`                                |
| `get_operation_assignment(id)`                                           | `GET /operation/{id}/assignment`                              |
| `post_operation_assignment(id, data)`                                    | `POST /operation/{id}/assignment`                             |
| `put_operation_assignment_crew(id, vehicle_id, data)`                    | `PUT /operation/{id}/assignment/{vehicleId}/crew`             |
| `get_operation_assignment_users(id, vehicle_id)`                         | `GET /operation/{id}/assignment/{vehicleId}/users`            |
| `post_operation_assignment_user(id, vehicle_id, data)`                   | `POST /operation/{id}/assignment/{vehicleId}/users`           |
| `put_operation_assignment_users(id, vehicle_id, data)`                   | `PUT /operation/{id}/assignment/{vehicleId}/users`            |
| `delete_operation_assignment_user(id, vehicle_id, user_assignment_id)`   | `DELETE /operation/{id}/assignment/{vehicleId}/users/{id}`    |
| `get_operation_user_status(id)`                                          | `GET /operation/{id}/userstatus`                              |
| `post_operation_user_status(data)`                                       | `POST /operation/userstatus`                                  |
| `get_operation_documentation(id)`                                        | `GET /operation/{id}/documentation`                           |
| `put_operation_documentation(id, data)`                                  | `PUT /operation/{id}/documentation`                           |

### Receive data about running operations

```python
api.get_operations()
```

By default the server only returns operations of the last 4 hours. Pass
`only_latest=False` to get the operation history. At most 100 items are
returned per request, use `top`/`skip` to page through them:

```python
api.get_operations(only_latest=False, orderby="Start desc", top=100, skip=100)
```

### Start new operation

```python

alarm_data = {
  "Start": "2025-05-15T12:19:48.909Z",
  "End": "2025-05-15T12:19:48.909Z",
  "Status": 0,
  "AlarmEnabled": True,
  "Keyword": "string",
  "Address": {
    "Street": "string",
    "HouseNumber": "string",
    "ZipCode": "string",
    "City": "string",
    "District": "string"
  },
  "Reporter": {
    "Name": "string",
    "PhoneNumber": "string"
  },
  "Position": {
    "Latitude": 0,
    "Longitude": 0
  },
  "Facts": "string",
  "Ric": "string",
  "Number": "string",
  "Source": "string",
  "Properties": [
    {
      "Key": "string",
      "Value": "string",
      "Priority": 0
    }
  ],
  "AlarmedVehicles": [
    {
      "Id": 0,
      "RadioIdentifier": "string"
    }
  ],
  "AssignedVehicles": [
    {
      "Name": "string",
      "VehicleId": 0,
      "RadioId": "string",
      "Assigned": "2025-05-15T12:19:48.909Z",
      "Alerted": "2025-05-15T12:19:48.909Z",
      "Finished": "2025-05-15T12:19:48.909Z",
      "Status1": "2025-05-15T12:19:48.909Z",
      "Status2": "2025-05-15T12:19:48.909Z",
      "Status3": "2025-05-15T12:19:48.909Z",
      "Status4": "2025-05-15T12:19:48.909Z",
      "Status7": "2025-05-15T12:19:48.909Z",
      "Status8": "2025-05-15T12:19:48.909Z"
    }
  ]
}


api.post_operation(alarm_data)

```

If you want to update a running operation, you can pass an argument to `api.post_operation`:

```python
api.post_operation(alarm_data, update_strategy="byNumber")
```

`update_strategy` can be one of four strings: `"none", "byNumber", "byAddress", "byPosition"`

> [!NOTE]
> Only Start and Keyword are mandatory. `Status` and `Priority` must be one of 0, 1, 2, 3.

### Operation messages

```python
api.post_operation_message("4711", {
    "MessageText": "Lage unter Kontrolle",
    "Source": "ILS",
    "SenderName": "Florian Waldshut 1/44-1",
})
```

### Vehicle assignments

```python
from feuersoftware.models import VehicleUserPosition

api.post_operation_assignment("4711", {"VehicleId": 12345678, "Source": "ILS"})

api.put_operation_assignment_crew("4711", "12345678", {
    "Crew": 9,
    "RespiratorCarriers": 4,
})

api.post_operation_assignment_user("4711", "12345678", {
    "UserName": "jane",
    "Position": VehicleUserPosition.Leader,
    "IsRespiratorCarrier": False,
})
```

`put_operation_assignment_users` takes a list of user assignments and replaces
all user assignments of the vehicle.

### User operation status

```python
from feuersoftware.models import UserOperationStatus

api.post_operation_user_status({
    "OperationId": 4711,
    "PagerIssi": "1234567",
    "Status": UserOperationStatus.Coming,
    "TimeUntilArrival": {"Duration": 300, "Distance": 2500},
})
```

### Operation documentation

```python
api.put_operation_documentation("4711", {
    "SituationOnArrival": "Rauchentwicklung aus Kellerfenster",
    "Activity": "Brandbekämpfung mit 1 C-Rohr unter PA",
    "Leader": "Max Mustermann",
})
```

## Organization

| Method                  | HTTP                |
| ----------------------- | ------------------- |
| `get_organization()`    | `GET /organization` |

## Users

| Method                                | HTTP                                    |
| ------------------------------------- | --------------------------------------- |
| `get_users()`                         | `GET /user`                             |
| `get_user(id)`                        | `GET /user/{id}`                        |
| `put_user(id, data)`                  | `PUT /user/{id}`                        |
| `patch_user(id, data)`                | `PATCH /user/{id}`                      |
| `delete_user(id)`                     | `DELETE /user/{id}`                     |
| `post_user_invite(data)`              | `POST /user/invite`                     |
| `put_user_availability(id, data)`     | `PUT /user/{id}/availability/current`   |
| `get_user_profilepicture(id)`         | `GET /user/{id}/profilepicture`         |

```python
api.post_user_invite({
    "Email": "jane@example.com",
    "FirstName": "Jane",
    "LastName": "Doe",
    "Roles": [{"RoleName": "User"}],
})
```

`patch_user` takes a [JSON Patch](https://jsonpatch.com/) document, the
supported ops are `add`, `remove` and `replace`:

```python
api.patch_user("abc123", [{"op": "replace", "path": "/lastName", "value": "Doe"}])
```

The `id` of `put_user_availability` can be the user id or the pager number:

```python
from feuersoftware.models import AvailabilityStatus

api.put_user_availability("1234567", {
    "Status": AvailabilityStatus.NotAvailable,
    "Until": "2025-05-16T08:00:00Z",
    "Info": "Urlaub",
})
```

## User API

These endpoints are authenticated with a personal user token instead of the
API token.

| Method                                                                         | HTTP                         |
| ------------------------------------------------------------------------------ | ---------------------------- |
| `get_user_availablity(token, status, lifeTimeDays)`                            | `GET /user/useravailability` |
| `get_user_status(token, status, driveTimeSeconds, driveDistanceMeters, siteId)`| `GET /user/userstatus`       |

```python
api.get_user_availablity("usertoken", status=0, lifeTimeDays=1)
api.get_user_status(
    "usertoken", status=1, driveTimeSeconds=300, driveDistanceMeters=2500, siteId=1
)
```

## Vehicles

| Method                                                       | HTTP                        |
| ------------------------------------------------------------ | --------------------------- |
| `get_vehicles()`                                             | `GET /vehicle`              |
| `get_vehicle_image(id, identifier_preference)`               | `GET /vehicle/{id}/image`   |
| `get_vehicle_status(id, identifier_preference)`              | `GET /vehicle/{id}/status`  |
| `post_vehicle_status(id, data, identifier_preference)`       | `POST /vehicle/{id}/status` |

`id` can be either the vehicle id or the radio id. The server resolves it
according to `identifier_preference`, which defaults to `"PreferRadioId"` on
the server side.

### Set vehicle status

```python
status_data = {
  "Status": 3,
  "Position": {
    "Latitude": 47.59902386911071,
    "Longitude": 8.334801219413004
  },
  "StatusTimestamp": "2025-05-15T12:24:08.905Z",
  "PositionTimestamp": "2025-05-15T12:24:08.905Z",
  "Source": "ILS"
}

api.post_vehicle_status(12345678, status_data)
```

## Vehicle availability

| Method                                                       | HTTP                                              |
| ------------------------------------------------------------ | ------------------------------------------------- |
| `get_vehicle_availabilities(id, filter, orderby, top, skip)` | `GET /vehicle/{id}/availability`                  |
| `post_vehicle_availability(id, data)`                        | `POST /vehicle/{id}/availability`                 |
| `put_vehicle_availability(id, availability_id, data)`        | `PUT /vehicle/{id}/availability/{availabilityId}` |
| `delete_vehicle_availability(id, availability_id)`           | `DELETE /vehicle/{id}/availability/{availabilityId}` |

`get_vehicle_availabilities` returns current and future availabilities,
sorted by start date ascending. `VehicleId` is filled in from `id` if it's
missing in `data`.

```python
from feuersoftware.models import AvailabilityStatus

api.post_vehicle_availability(12345678, {
    "Status": AvailabilityStatus.NotAvailable,
    "Info": "TÜV",
    "Start": "2025-05-20T07:00:00Z",
    "End": "2025-05-20T16:00:00Z",
})
```

## Vehicle CVM modules

| Method                               | HTTP                                |
| ------------------------------------ | ----------------------------------- |
| `get_vehicle_cvms(id)`               | `GET /vehicle/{id}/cvm`             |
| `post_vehicle_cvm(id, data)`         | `POST /vehicle/{id}/cvm`            |
| `get_vehicle_cvm(id, cvm_id)`        | `GET /vehicle/{id}/cvm/{cvmId}`     |
| `put_vehicle_cvm(id, cvm_id, data)`  | `PUT /vehicle/{id}/cvm/{cvmId}`     |
| `delete_vehicle_cvm(id, cvm_id)`     | `DELETE /vehicle/{id}/cvm/{cvmId}`  |

```python
api.post_vehicle_cvm(12345678, {
    "SerialNumber": "CVM-0001",
    "Description": "HLF 20",
    "OverrideDescription": False,
})
```

## Vehicle properties

| Method                                | HTTP                            |
| ------------------------------------- | ------------------------------- |
| `get_vehicle_properties(id)`          | `GET /vehicle/{id}/properties`  |
| `post_vehicle_properties(id, data)`   | `POST /vehicle/{id}/properties` |

```python
from feuersoftware.models import VehiclePropertyType

api.post_vehicle_properties(12345678, [
    {"Key": "Tankinhalt", "Value": "75", "Unit": "%", "Type": VehiclePropertyType.Integer},
    {"Key": "Kilometerstand", "Value": "48211", "Unit": "km"},
])
```

## Wasserkarte

These endpoints live under `/interfaces/wasserkarte` instead of
`/interfaces/public`.

| Method                                                | HTTP                       |
| ----------------------------------------------------- | -------------------------- |
| `get_wasserkarte_active()`                            | `GET /wasserkarte/active`  |
| `get_wasserkarte_hydrants(lat, lng, range, numItems)` | `GET /wasserkarte/hydrant` |

```python
api.get_wasserkarte_hydrants(lat=47.599, lng=8.334, range=500, numItems=10)
```
