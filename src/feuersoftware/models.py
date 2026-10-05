from datetime import date, datetime
from enum import IntEnum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class AddressModel(BaseModel):
    Street: str | None = Field(default=None, max_length=255)
    HouseNumber: str | None = Field(default=None, max_length=255)
    ZipCode: str | None = Field(default=None, max_length=255)
    City: str | None = Field(default=None, min_length=1, max_length=255)
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
    Source: str | None = None


class CreateOperationModel(BaseModel):
    Start: datetime  # required
    Keyword: str = Field(..., min_length=1, max_length=255)  # required
    End: datetime | None = None
    Status: int | None = None
    Priority: int | None = None
    AlarmEnabled: bool | None = None
    Address: AddressModel | None = None
    Reporter: ReporterModel | None = None
    Position: PositionModel | None = None
    Facts: str | None = Field(default=None, max_length=2000)
    Ric: str | None = Field(default=None, max_length=4000)
    Number: str | None = Field(default=None, max_length=255)
    Source: str | None = Field(default=None, max_length=255)
    Properties: list[PropertyModel] | None = None
    AlarmedVehicles: list[AlarmedVehicleModel] | None = None
    AssignedVehicles: list[AssignedVehicleModel] | None = None

    @field_validator("Status")
    @classmethod
    def check_status(cls, v: int) -> int:
        if v is not None and v not in {0, 1, 2, 3}:
            raise ValueError("Status must be one of [0, 1, 2, 3]")
        return v

    @field_validator("Priority")
    @classmethod
    def check_priority(cls, v: int) -> int:
        if v is not None and v not in {0, 1, 2, 3}:
            raise ValueError("Priority must be one of [0, 1, 2, 3]")
        return v


class SetVehicleStatusModel(BaseModel):
    Status: int | None = None
    Position: PositionModel | None = None
    StatusTimestamp: datetime | None = None
    PositionTimestamp: datetime | None = None
    Source: str | None = Field(default=None, max_length=255)


# ============================================================================
# ENUMS
# ============================================================================


class AvailabilityStatus(IntEnum):
    Available = 0
    LimitedAvailable = 1
    NotAvailable = 2


class AvailabilitySource(IntEnum):
    None_ = 0
    Manual = 1
    Pager = 2
    Auto = 3
    Scheduled = 4
    ScheduledRecurring = 5
    UserApi = 6


class DefectReportStatus(IntEnum):
    Reported = 0
    Reviewed = 1
    InProgress = 2
    Resolved = 3
    Rejected = 4
    Paused = 5


class DefectReportPriority(IntEnum):
    Low = 0
    Medium = 1
    High = 2


class NewsCategory(IntEnum):
    Announcement = 0
    TrafficObstruction = 1
    FasNotification = 2


class NewsType(IntEnum):
    SiteNews = 0
    OrganizationNews = 1


class SiteInfoType(IntEnum):
    PhoneNumber = 0
    EmailAddress = 1
    WebReference = 2
    DocumentReference = 3
    Text = 4


class UserOperationStatus(IntEnum):
    NotSet = 0
    Coming = 1
    NotComing = 2
    ComingLater = 3


class VehiclePropertyType(IntEnum):
    String = 0
    Integer = 1
    Double = 2
    Boolean = 3
    DateTime = 4


class VehicleUserPosition(IntEnum):
    None_ = 0
    Leader = 1
    Driver = 2


# ============================================================================
# SHARED
# ============================================================================


class SiteBriefModel(BaseModel):
    Id: int
    Name: str = Field(..., min_length=1, max_length=255)


class UserBriefModel(BaseModel):
    Id: str | None = Field(default=None, max_length=128)
    FirstName: str | None = Field(default=None, max_length=255)
    LastName: str | None = Field(default=None, max_length=255)
    Email: str = Field(..., min_length=1, max_length=255)
    UserName: str = Field(..., min_length=1, max_length=255)
    PagerIssi: str | None = Field(default=None, max_length=255)


# ============================================================================
# ALARMGROUP
# ============================================================================


class AlarmGroupModel(BaseModel):
    Id: int | None = None
    Name: str = Field(..., min_length=1, max_length=255)
    Users: list[UserBriefModel]
    Site: SiteBriefModel | None = None


# ============================================================================
# DEFECT REPORT
# ============================================================================


class CreateDefectReportModel(BaseModel):
    SiteId: int
    Status: DefectReportStatus
    ShortDescription: str = Field(..., min_length=1, max_length=255)
    DetailedDescription: str = Field(..., min_length=1, max_length=2000)
    Priority: DefectReportPriority | None = None
    ResponsibleUserId: str | None = None
    VehicleId: int | None = None
    ReporterId: str | None = None
    Odometer: float | None = None
    CategoryId: int | None = None
    CategoryInformation: str | None = Field(default=None, max_length=255)


class EditDefectReportModel(BaseModel):
    ShortDescription: str = Field(..., min_length=1, max_length=255)
    DetailedDescription: str = Field(..., min_length=1, max_length=2000)
    Priority: DefectReportPriority | None = None
    Status: DefectReportStatus
    ResponsibleUserId: str | None = None
    VehicleId: int | None = None
    UserId: str | None = None
    Odometer: float | None = None
    CategoryInformation: str | None = Field(default=None, max_length=255)


class UploadFile(BaseModel):
    Name: str = Field(..., max_length=255)
    Size: int | None = None
    Description: str | None = Field(default=None, max_length=255)
    MimeType: str | None = None


class CreateDefectReportCategoryModel(BaseModel):
    Name: str = Field(..., min_length=1, max_length=255)
    OrganizationId: int | None = None
    SiteId: int | None = None


class EditDefectReportCategoryModel(BaseModel):
    Name: str = Field(..., min_length=1, max_length=255)


# ============================================================================
# DIAGNOSTICS
# ============================================================================


class DiagnosticUploadRequestModel(BaseModel):
    Message: str | None = None
    MonitorName: str | None = None
    MonitorVersion: str | None = None
    OsInfo: str | None = None
    OsVersion: str | None = None
    AdditionalData: Any = None


# ============================================================================
# INFOBOARD
# ============================================================================


class CreateSiteInfoModel(BaseModel):
    InfoGroupId: int
    Description: str = Field(..., min_length=1, max_length=2000)
    InfoType: SiteInfoType
    Value: str = Field(..., min_length=1, max_length=2000)


class CreateSiteInfoGroupPublicAppModel(BaseModel):
    SiteId: int | None = None
    Name: str = Field(..., min_length=1, max_length=255)


# ============================================================================
# NEWS
# ============================================================================


class UpdateNewsModel(BaseModel):
    Title: str = Field(..., min_length=1, max_length=255)
    Content: str = Field(..., min_length=1, max_length=4000)
    Start: date
    End: date
    Groups: list[str] | None = None
    MailingLists: list[str] | None = None
    SendNotificationsImmediately: bool | None = None
    AdditionalInformation: dict | None = None


class CreateNewsModel(UpdateNewsModel):
    Category: NewsCategory | None = None
    Site: str | None = Field(default=None, max_length=255)


# ============================================================================
# OPERATION
# ============================================================================


class CreateOperationMessageModel(BaseModel):
    MessageText: str = Field(..., min_length=1, max_length=2000)
    TimeStamp: datetime | None = None
    Source: str = Field(..., min_length=1, max_length=255)
    SenderName: str | None = Field(default=None, max_length=255)
    ReceiverName: str | None = Field(default=None, max_length=255)


class UpdateVehicleAssignmentCrewModel(BaseModel):
    Crew: int | None = None
    RespiratorCarriers: int | None = None
    Source: str | None = None


class TimeUntilArrivalModel(BaseModel):
    Duration: int | None = None  # seconds
    Distance: int | None = None  # meters
    TimeStamp: datetime | None = None


class UserOperationStatusModel(BaseModel):
    OperationId: int | None = None
    UserName: str | None = None
    UserId: str | None = None
    PagerIssi: str | None = None
    Status: UserOperationStatus
    Source: str | None = Field(default=None, max_length=255)
    TimeUntilArrival: TimeUntilArrivalModel | None = None


class OperationDocumentationModel(BaseModel):
    SituationOnArrival: str | None = Field(default=None, max_length=2000)
    Activity: str | None = Field(default=None, max_length=2000)
    Leader: str | None = Field(default=None, max_length=255)
    Owner: str | None = Field(default=None, max_length=255)
    Injured: str | None = Field(default=None, max_length=255)
    Initiator: str | None = Field(default=None, max_length=255)
    UsedMaterials: str | None = Field(default=None, max_length=2000)
    ToBeDoneAfterOperation: str | None = Field(default=None, max_length=2000)
    Recorder: str | None = Field(default=None, max_length=255)
    Comments: str | None = Field(default=None, max_length=2000)


class CreateUserAssignmentModel(BaseModel):
    UserId: str | None = None
    UserName: str | None = None
    Position: VehicleUserPosition | None = None
    IsRespiratorCarrier: bool | None = None


# ============================================================================
# USER
# ============================================================================


class BluetoothBeaconModel(BaseModel):
    Id: int | None = None
    BeaconId: UUID | None = None
    Model: str | None = None
    Manufacturer: str | None = None


class UserFunctionModel(BaseModel):
    Id: int | None = None
    Name: str | None = None
    Abbreviation: str | None = None


class FunctionModel(BaseModel):
    Id: int
    Name: str | None = Field(default=None, max_length=255)
    Abbreviation: str | None = Field(default=None, max_length=255)


class GroupNameModel(BaseModel):
    Id: int
    Name: str | None = Field(default=None, max_length=255)


class RoleAssignmentModel(BaseModel):
    RoleName: str = Field(..., min_length=1)


class UpdateUserModel(BaseModel):
    FirstName: str | None = Field(default=None, max_length=255)
    LastName: str | None = Field(default=None, max_length=255)
    Email: str = Field(..., min_length=1, max_length=255)
    UserName: str = Field(..., min_length=1, max_length=255)
    PagerIssi: str | None = Field(default=None, max_length=255)
    Address: AddressModel | None = None
    PhoneNumber: str | None = None
    LandlineNumber: str | None = None
    BluetoothBeacons: list[BluetoothBeaconModel] | None = None
    Sites: list[SiteBriefModel] | None = None
    Functions: list[UserFunctionModel] | None = None


class InviteUserModel(BaseModel):
    Email: str = Field(..., min_length=1, max_length=255)
    FirstName: str | None = Field(default=None, max_length=255)
    LastName: str | None = Field(default=None, max_length=255)
    Address: AddressModel | None = None
    PhoneNumber: str | None = None
    LandlineNumber: str | None = None
    DisableAvailability: bool | None = None
    PagerIssi: str | None = Field(default=None, max_length=255)
    Sites: list[SiteBriefModel] | None = None
    Roles: list[RoleAssignmentModel] | None = None
    Groups: list[GroupNameModel] | None = None
    AlarmGroups: list[GroupNameModel] | None = None
    Functions: list[FunctionModel] | None = None


class JsonPatchOperation(BaseModel):
    op: Literal["add", "remove", "replace"]
    path: str = Field(..., min_length=1)
    value: str | None = None


class UserAvailabilityModel(BaseModel):
    Status: AvailabilityStatus
    Until: datetime | None = None
    Source: AvailabilitySource | None = None
    Info: str | None = None


# ============================================================================
# VEHICLE
# ============================================================================


class CreateVehicleAvailabilityModel(BaseModel):
    VehicleId: int | None = None
    Status: AvailabilityStatus | None = None
    Info: str = Field(..., min_length=1, max_length=255)
    Start: datetime | None = None
    End: datetime | None = None
    MailingListIds: list[int] | None = None


class CreateVehicleCvmModuleModel(BaseModel):
    SerialNumber: str = Field(..., min_length=1, max_length=255)
    Description: str = Field(..., min_length=1, max_length=255)
    OverrideDescription: bool


class CreateVehiclePropertyModel(BaseModel):
    Key: str = Field(..., min_length=1, max_length=255)
    Value: str | None = Field(default=None, max_length=255)
    Unit: str | None = Field(default=None, max_length=255)
    Source: str | None = Field(default=None, max_length=255)
    GroupingKey: str | None = Field(default=None, max_length=255)
    Type: VehiclePropertyType | None = None
