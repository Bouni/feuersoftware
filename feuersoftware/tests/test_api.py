from unittest import TestCase

import feuersoftware

class TestAPI(TestCase):

    def test_token_length(self):
        with self.assertRaises(Exception):
            api = feuersoftware.PublicAPI(token="A")
        with self.assertRaises(Exception):
            api = feuersoftware.PublicAPI(token="A"*561)
         
    def test_token_type(self):
        with self.assertRaises(Exception):
            api = feuersoftware.PublicAPI(token=[])
        with self.assertRaises(Exception):
            api = feuersoftware.PublicAPI(token={})
        with self.assertRaises(Exception):
            api = feuersoftware.PublicAPI(token=123)
        with self.assertRaises(Exception):
            api = feuersoftware.PublicAPI(token=123.44)
        with self.assertRaises(Exception):
            api = feuersoftware.PublicAPI()

    def test_token_valid(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        self.assertIn("bearer "+"A"*560, api._headers["authorization"])


class TestOperation(TestCase):

    def test_start_format(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.operation(start="30.08.2018 08:06:00", keyword="THL 1")
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1")
        self.assertEqual("2018-08-30T08:06:00", api._body["start"])
    
    def test_start_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.operation(start=1234, keyword="THL 1")
        with self.assertRaises(Exception):
            api.operation(start=12.45, keyword="THL 1")
        with self.assertRaises(Exception):
            api.operation(start=[], keyword="THL 1")
        with self.assertRaises(Exception):
            api.operation(start={}, keyword="THL 1")

    def test_start_mendatory(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.operation(keyword="THL 1")

    def test_keyword_length(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.operation(start="2018-08-30T08:06:00", keyword="")
        with self.assertRaises(Exception):
            api.operation(start="2018-08-30T08:06:00", keyword="A"*260)

    def test_keyword_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.operation(start="2018-08-30T08:06:00", keyword=[])
        with self.assertRaises(Exception):
            api.operation(start="2018-08-30T08:06:00", keyword={})
        with self.assertRaises(Exception):
            api.operation(start="2018-08-30T08:06:00", keyword=1234)

    def test_keyword_mendatory(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.operation(start="2018-08-30T08:06:00")

    def test_minimal_operation(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1")
        self.assertEqual({"start":"2018-08-30T08:06:00", "keyword":"THL 1"}, api._body)

    def test_address_length(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", address="")
        self.assertNotIn("address", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", address="A"*260)
        self.assertNotIn("address", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", address="Musterweg 23, 79812 Entenhausen")
        self.assertEqual("Musterweg 23, 79812 Entenhausen", api._body["address"])
    
    def test_address_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", address=123)
        self.assertNotIn("address", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", address=123.34)
        self.assertNotIn("address", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", address=[])
        self.assertNotIn("address", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", address={})
        self.assertNotIn("address", api._body)

    def test_position_format(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", position="47.627720, 9.356430")
        self.assertEqual({"latitude":47.627720, "longitude":9.356430}, api._body["position"])
    
    def test_position_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", position=123)
        self.assertNotIn("position", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", position=123.34)
        self.assertNotIn("position", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", position=[])
        self.assertNotIn("position", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", position={})
        self.assertNotIn("position", api._body)

    def test_facts_length(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", facts="")
        self.assertNotIn("facts", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", facts="A"*260)
        self.assertNotIn("facts", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", facts="Küchenbrand")
        self.assertEqual("Küchenbrand", api._body["facts"])
    
    def test_facts_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", facts=123)
        self.assertNotIn("facts", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", facts=123.34)
        self.assertNotIn("facts", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", facts=[])
        self.assertNotIn("facts", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", facts={})
        self.assertNotIn("facts", api._body)
    
    def test_ric_length(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", ric="")
        self.assertNotIn("ric", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", ric="A"*260)
        self.assertNotIn("ric", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", ric="10B")
        self.assertEqual("10B", api._body["ric"])
    
    def test_ric_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", ric=123)
        self.assertNotIn("ric", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", ric=123.34)
        self.assertNotIn("ric", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", ric=[])
        self.assertNotIn("ric", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", ric={})
        self.assertNotIn("ric", api._body)

    def test_properties_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=123)
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=123.34)
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties={})
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties="")
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"a":"b"}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"key":"Hans"}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":"Maier"}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":12,"value":"Maier"}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":12.23,"value":"Maier"}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":[],"value":"Maier"}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":{},"value":"Maier"}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":"Maier","value":12}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":"Maier","value":12.23}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":"Maier","value":[]}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"value":"Maier","value":{}}])
        self.assertNotIn("properties", api._body)
        api.operation(start="2018-08-30T08:06:00", keyword="THL 1", properties=[{"key":"Solaranlage","value":"Ja"},{"key":"Melder","value":"Hans Maier"}])
        self.assertEqual([{"key":"Solaranlage","value":"Ja"},{"key":"Melder","value":"Hans Maier"}], api._body["properties"])


class TestVehicleStatus(TestCase):
        
    def test_radioid_length(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="", status=2)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="1"*260, status=2)
        api.vehicle_status(radioid="12345678", status=2)
        self.assertIn("12345678", api._url)
    
    def test_radioid_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid=123, status=2)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid=123.34, status=2)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid=[], status=2)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid={}, status=2)

    def test_radioid_mendatory(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.vehicle_status(status=2)
    
    def test_status_range(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="12345678", status=-1)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="12345678", status=10)
        api.vehicle_status(radioid="12345678", status=2)
        self.assertEqual(2, api._body["status"])
    
    def test_status_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="12345678", status="2")
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="12345678", status=12.23)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="12345678", status=[])
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="12345678", status={})

    def test_status_mendatory(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        with self.assertRaises(Exception):
            api.vehicle_status(radioid="12345678")
    
    def test_position_format(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.vehicle_status(radioid="12345678", status=2, position="47.627720, 9.356430")
        self.assertEqual({"latitude":47.627720, "longitude":9.356430}, api._body["position"])
    
    def test_position_type(self):
        api = feuersoftware.PublicAPI(token="A"*560)
        api.vehicle_status(radioid="12345678", status=2, position=123)
        self.assertNotIn("position", api._body)
        api.vehicle_status(radioid="12345678", status=2, position=123.34)
        self.assertNotIn("position", api._body)
        api.vehicle_status(radioid="12345678", status=2, position=[])
        self.assertNotIn("position", api._body)
        api.vehicle_status(radioid="12345678", status=2, position={})
        self.assertNotIn("position", api._body)

