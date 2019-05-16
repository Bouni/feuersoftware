# feuersoftware

feuersoftware is a library that allow you to interact with the [Feuersoftware Connect Public API](http://dokumentation.feuersoftware.com/pages/viewpage.action?pageId=2490428).

## Example
```
from feuersoftware import PublicAPI

TOKEN = ""

with open("token.txt") as f:
    TOKEN = f.read().strip()

api = PublicAPI(token=TOKEN)

# Einsatz auslösen
api.operation(
    start="2018-08-30T08:00:00", 
    keyword="Brand", 
    status="new",
    alarm_enabled=True,
    address="Musterweg 4, 12345 Entenhausen", 
    position={"latitude":"47.592127",·"longitude":"8.296870"}, 
    facts="Küchenbrand", 
    ric="10B", 
    number=54321,
    properties=[{"key":"Fettbrand":"value":"Nein"},{"key":"Noch Personen im Gebäude","value":"Ja"}],
    updateStrategy="none"
    )
api.send()

# Fahzeug Status setzen
api.vehicle_status(
    radioid=12345678, 
    status=2, 
    position={"latitude":"47.592127",·"longitude":"8.296870"}):
api.send()
```

