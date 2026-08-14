import pytest
from pydantic import ValidationError

from feuersoftware.models import (
    AddressModel,
    AlarmedVehicleModel,
    AssignedVehicleModel,
    CreateOperationModel,
    PositionModel,
    PropertyModel,
    ReporterModel,
    SetVehicleStatusModel,
)

# ============================================================================
# CreateOperationModel
# ============================================================================


def test_create_operation_model_requires_start_and_keyword():
    with pytest.raises(ValidationError):
        CreateOperationModel()


def test_create_operation_model_minimal_valid():
    model = CreateOperationModel(Start="2025-05-15T12:19:48.909Z", Keyword="Probealarm")
    assert model.Keyword == "Probealarm"
    assert model.End is None
    assert model.Status is None


@pytest.mark.parametrize("status", [0, 1, 2, 3])
def test_create_operation_model_accepts_valid_status(status):
    model = CreateOperationModel(
        Start="2025-05-15T12:19:48.909Z", Keyword="Test", Status=status
    )
    assert model.Status == status


def test_create_operation_model_accepts_none_status():
    model = CreateOperationModel(Start="2025-05-15T12:19:48.909Z", Keyword="Test")
    assert model.Status is None


@pytest.mark.parametrize("status", [-1, 4, 99])
def test_create_operation_model_rejects_invalid_status(status):
    """
    Regression test covering CHANGE #12 (adding @classmethod to the
    field_validator): the validator must still actually run and reject
    out-of-range Status values after that change.
    """
    with pytest.raises(ValidationError) as exc_info:
        CreateOperationModel(
            Start="2025-05-15T12:19:48.909Z", Keyword="Test", Status=status
        )
    assert "Status must be one of [0, 1, 2, 3]" in str(exc_info.value)


def test_create_operation_model_keyword_cannot_be_empty():
    with pytest.raises(ValidationError):
        CreateOperationModel(Start="2025-05-15T12:19:48.909Z", Keyword="")


def test_create_operation_model_with_full_nested_payload():
    model = CreateOperationModel(
        Start="2025-05-15T12:19:48.909Z",
        End="2025-05-15T13:00:00.000Z",
        Status=0,
        AlarmEnabled=True,
        Keyword="Brandmeldeanlage",
        Address={
            "Street": "Musterstrasse",
            "HouseNumber": "23",
            "ZipCode": "12345",
            "City": "Musterhausen",
            "District": "Musterteil",
        },
        Reporter={"Name": "Max Mustermann", "PhoneNumber": "0123456789"},
        Position={"Latitude": 48.6928957, "Longitude": 9.1928973},
        Facts="Rauchentwicklung im Keller",
        Ric="1234567",
        Number="20250429001",
        Source="ILS",
        Properties=[{"Key": "Sirene", "Value": "Ja", "Priority": 1}],
        AlarmedVehicles=[{"Id": 1, "RadioIdentifier": "florian1"}],
        AssignedVehicles=[
            {"Name": "LF20", "VehicleId": 1, "Status1": "2025-05-15T12:20:00.000Z"}
        ],
    )

    assert model.Address.City == "Musterhausen"
    assert model.Reporter.Name == "Max Mustermann"
    assert model.Position.Latitude == pytest.approx(48.6928957)
    assert model.Properties[0].Key == "Sirene"
    assert model.AlarmedVehicles[0].RadioIdentifier == "florian1"
    assert model.AssignedVehicles[0].Name == "LF20"


def test_create_operation_model_rejects_invalid_datetime():
    with pytest.raises(ValidationError):
        CreateOperationModel(Start="not-a-date", Keyword="Test")


def test_create_operation_model_facts_max_length():
    with pytest.raises(ValidationError):
        CreateOperationModel(
            Start="2025-05-15T12:19:48.909Z",
            Keyword="Test",
            Facts="x" * 256,
        )


# ============================================================================
# SetVehicleStatusModel
# ============================================================================


def test_set_vehicle_status_model_all_fields_optional():
    model = SetVehicleStatusModel()
    assert model.Status is None
    assert model.Position is None
    assert model.StatusTimestamp is None


def test_set_vehicle_status_model_valid_payload():
    model = SetVehicleStatusModel(
        Status=3,
        Position={"Latitude": 47.59902386911071, "Longitude": 8.334801219413004},
        StatusTimestamp="2025-05-15T12:24:08.905Z",
        PositionTimestamp="2025-05-15T12:24:08.905Z",
        Source="ILS",
    )
    assert model.Status == 3
    assert model.Position.Latitude == pytest.approx(47.59902386911071)
    assert model.Source == "ILS"


def test_set_vehicle_status_model_rejects_invalid_datetime():
    with pytest.raises(ValidationError):
        SetVehicleStatusModel(StatusTimestamp="not-a-date")


# ============================================================================
# Smaller nested models
# ============================================================================


def test_address_model_all_fields_optional():
    model = AddressModel()
    assert model.Street is None
    assert model.City is None


def test_address_model_city_min_length():
    with pytest.raises(ValidationError):
        AddressModel(City="")


def test_reporter_model_defaults():
    model = ReporterModel()
    assert model.Name is None
    assert model.PhoneNumber is None


def test_position_model_defaults():
    model = PositionModel()
    assert model.Latitude is None
    assert model.Longitude is None


def test_property_model_requires_key():
    with pytest.raises(ValidationError):
        PropertyModel(Value="something")


def test_property_model_default_priority():
    model = PropertyModel(Key="Sirene")
    assert model.Priority == 0


def test_alarmed_vehicle_model_defaults():
    model = AlarmedVehicleModel()
    assert model.Id is None
    assert model.RadioIdentifier is None


def test_assigned_vehicle_model_defaults():
    model = AssignedVehicleModel()
    assert model.Name is None
    assert model.VehicleId is None
    assert model.Assigned is None
