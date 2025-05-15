from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class AddressModel(BaseModel):
    Street: str | None = Field(default=None, max_length=255)
    HouseNumber: str | None = Field(default=None, max_length=255)
    ZipCode: str | None = Field(default=None, max_length=255)
    City: str = Field(..., min_length=1, max_length=255)
    District: str | None = Field(default=None, max_length=255)


class ReporterModel(BaseModel):
    Name: str | None = Field(default=None, max_length=255)
    PhoneNumber: str | None = Field(default=None, max_length=255)


class PositionModel(BaseModel):
    Latitude: float | None = None
    Longitude: float | None = None


class PropertyModel(BaseModel):
    Key: str = Field(..., min_length=1, max_length=255)
    Value: str | None = Field(default=None, max_length=2000)
    Priority: int = 0


class AlarmedVehicleModel(BaseModel):
    Id: int | None = None
    RadioIdentifier: str | None = None


class AssignedVehicleModel(BaseModel):
    Name: str | None = Field(default=None, max_length=255)
    VehicleId: int | None = None
    RadioId: str | None = Field(default=None, max_length=255)
    Assigned: datetime | None = None
    Alerted: datetime | None = None
    Finished: datetime | None = None
    Status1: datetime | None = None
    Status2: datetime | None = None
    Status3: datetime | None = None
    Status4: datetime | None = None
    Status7: datetime | None = None
    Status8: datetime | None = None


class CreateOperationModel(BaseModel):
    @field_validator("Status")
    def check_status(cls, v: int) -> int:
        if v is not None and v not in {0, 1, 2, 3}:
            raise ValueError("Status must be one of [0, 1, 2, 3]")
        return v

    Start: datetime  # required
    Keyword: str = Field(..., min_length=1, max_length=255)  # required

    End: datetime | None = None
    Status: int | None = None
    AlarmEnabled: bool | None = None
    Address: AddressModel | None = None
    Reporter: ReporterModel | None = None
    Position: PositionModel | None = None
    Facts: str | None = Field(default=None, max_length=255)
    Ric: str | None = Field(default=None, max_length=4000)
    Number: str | None = Field(default=None, max_length=255)
    Source: str | None = Field(default=None, max_length=255)
    Properties: list[PropertyModel] | None = None
    AlarmedVehicles: list[AlarmedVehicleModel] | None = None
    AssignedVehicles: list[AssignedVehicleModel] | None = None


class SetVehicleStatusModel(BaseModel):
    Status: int | None = None
    Position: PositionModel | None = None
    StatusTimestamp: datetime | None = None
    PositionTimestamp: datetime | None = None
    Source: str | None = Field(default=None, max_length=255)
