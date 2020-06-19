# feuersoftware

feuersoftware is a library that allow you to interact with the [Feuersoftware Connect Public API](https://connectapi.feuersoftware.com/swagger/ui/index#!/Public32API/).

## Example

Note: Every resource returns the [python requests](https://2.python-requests.org/en/master/) response object.

## Setup the API
```

from feuersoftware import PublicAPI

TOKEN = '2xgRoQfoMGb4IveCDJIZqOO1l8hZZ5jT5mAw7SSk1otrFSq50IA2HIYB3luEpv7Vw8BWwG'\
        'Y2zV96VUkOF3FCZs2OP03qaTWF3CDrUHOKndvLIFTTgx0FCMBTFBRF1DfG4g3rs8BSMHB4'\
        '6qph1AlxOZ6parmJlp90V3GQB4EoI6DFdKE4SZeBuu46mXoaDlSmpTTS3FCpeG7oEUJVgy'\
        'pLZkZSFPRng5HdKhp6HG2XmNIMAtKTG3DAUWuKRi3cZ4JstLj05y4r7jt81g4DYXz9gVYc'\
        'UWk2pOkIZ9RPmu0s4LlaXHEK3TJlxLIUt5eHIzPUVKXyhdJDckviPsTYNfRxkpcNGd0vAb'\
        'zfzwMadgb4xaOi1v6ZpsRfXyOPgpudcnO6rwwi9TlAWNZ2075CO7HVFEP31yGhXmYsdFwj'\
        'ne3UIraWovMWHqeyv2yQLigKLePDAgXYUFqQpZ9P5ScznSMUg0ZnxS0Miy0qKe9zDYtqTk'\
        'qQVwrUGfGVFp4Ti83NJLCCGUOCmF0ovOB28mYyQIqGAi2MDaNIuAvz6HT1tGAo5nYdzOeu'

api = PublicAPI(TOKEN)
```

### Receive data about running operations

```
api.get_operation()
```

### Start new operation

```
api.post_operation(
    start="2019-06-06T08:00:00", 
    end="2019-06-06T18:00:00", 
    keyword="Brand 2", 
    status="new",
    alarmenabled=True,
    address="Musterweg 4, 12345 Entenhausen", 
    position={"latitude":"47.592127",·"longitude":"8.296870"}, 
    facts="Küchenbrand", 
    ric="10B", 
    number=54321,
    properties=[{"key":"Fettbrand":"value":"Nein"},{"key":"Noch Personen im Gebäude","value":"Ja"}],
    updateStrategy="none"
    )
```

### Set user status for a running operation

```
api.post_user_status(
    operationid=1,
    name="Hans Maier",
    status="coming"
    )
```

### Set vehicle status

```
api.post_vehicle_status(
    radioid=12345678, 
    status=2, 
    position={"latitude":"47.592127",·"longitude":"8.296870"}
    )
```

### Get alarmgroup

```
api.get_alarm_group()
```

### Put a user into an alarmgroup

```
api.put_alarm_group(
    id=0,
    name="Alarmgruppe 1",
    users=[
        {"id":1, "firstname": "Hans", "lastname": "Maier", "email": "hans.maier@ffw.de"},
        {"id":2, "firstname": "Peter", "lastname": "Baumann", "email": "peter.baumann@ffw.de"}
    ])
```

### Get geocoordinates for an address

```
api.get_geocoding("Musterstrasse 1, 12345 Musterstadt")
```

### Check password

```
api.post_passwordcheck("MySecurePassword123!")
```

### Get news

```
api.get_news()
```

### Post news

```
api.post_news(
    title="News title",
    content="An alle, bitte bechten dass ...",
    start="2019-06-06T18:00:00",
    end="2019-06-06T18:00:00",
    news_type="siteNews",
    groups=[
        "Gruppenführer",
        "Gerätewarte"
        ],
    mailinglists=[
        "Mailingliste FFW"
        ]
    )
```

### Delete news

```
api.delete_news(1)
```


### Update a news entry

```
api.put_news(
    id=1,
    title="News title",
    content="An alle, bitte bechten dass ...",
    start="2019-06-06T18:00:00",
    end="2019-06-06T18:00:00",
    groups=[
        "Gruppenführer",
        "Gerätewarte"
        ],
    mailinglists=[
        "Mailingliste FFW"
        ]
    )
```

