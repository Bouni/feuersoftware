# Feuersoftware

Feuersoftware is a library that allow you to interact with the [Feuersoftware Connect Public API](https://connectapi.feuersoftware.com/swagger/index.html).

> [!IMPORTANT]  
> A lot of API routes are not yet implemented. 
> If you need a specific API route, open an issue or submit a Pull request an I try to implement it ASAP.


## Example

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

### Receive data about running operations

```python
api.get_operations()
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
> Only Start and Keyword are mandatory


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

api.post_vehicle_status(radioid=12345678, status_data)
```
