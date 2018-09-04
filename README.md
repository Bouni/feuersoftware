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
    start="2018-08.30T08:00:00", 
    keyword="Brand", 
    address="Musterweg 4, 12345 Entenhausen", 
    position="47.616239,9.3392483", 
    facts="Küchenbrand", 
    ric="10B", 
    properties=[{"key":"Fettbrand":"value":"Nein"},{"Noch Personen im Gebäude","Ja"}])
api.send()

# Fahzeug Status setzen
api.vehicle_status(
    radioid="12345678", 
    status=2, 
    position="47.616239,9.3392483"):
api.send()
```

