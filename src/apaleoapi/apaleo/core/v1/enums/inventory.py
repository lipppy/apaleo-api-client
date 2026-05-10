from enum import Enum


class Action(str, Enum):
    DELETE = "Delete"
    ARCHIVE = "Archive"
    SET_LIVE = "SetLive"
    RESET = "Reset"


class Code(str, Enum):
    DELETE_NOT_ALLOWED_FOR_PROPERTY_NOT_IN_STATUS_TEST = (
        "DeleteNotAllowedForPropertyNotInStatusTest"
    )
    ARCHIVE_NOT_ALLOWED_FOR_PROPERTY_NOT_IN_STATUS_LIVE = (
        "ArchiveNotAllowedForPropertyNotInStatusLive"
    )
    ARCHIVE_NOT_ALLOWED_FOR_PROPERTY_WHICH_IS_ALREADY_ARCHIVED = (
        "ArchiveNotAllowedForPropertyWhichIsAlreadyArchived"
    )
    SET_TO_LIVE_NOT_ALLOWED_FOR_PROPERTY_NOT_IN_STATUS_TEST = (
        "SetToLiveNotAllowedForPropertyNotInStatusTest"
    )
    SET_TO_LIVE_NOT_ALLOWED_FOR_PROPERTY_IN_NON_LIVE_ACCOUNT = (
        "SetToLiveNotAllowedForPropertyInNonLiveAccount"
    )
    RESET_NOT_ALLOWED_FOR_PROPERTY_NOT_IN_STATUS_TEST = "ResetNotAllowedForPropertyNotInStatusTest"


class Condition(str, Enum):
    CLEAN = "Clean"
    CLEAN_TO_BE_INSPECTED = "CleanToBeInspected"
    DIRTY = "Dirty"


class Status(str, Enum):
    """Property status enum."""

    LIVE = "Live"
    TEST = "Test"


class UnitGroupType(str, Enum):
    BED_ROOM = "BedRoom"
    MEETING_ROOM = "MeetingRoom"
    EVENT_SPACE = "EventSpace"
    PARKING_LOT = "ParkingLot"


class UnitGroupExtendedType(str, Enum):
    BED_ROOM = "BedRoom"
    MEETING_ROOM = "MeetingRoom"
    EVENT_SPACE = "EventSpace"
    PARKING_LOT = "ParkingLot"
    OTHER = "Other"


class UnitMaintenanceType(str, Enum):
    OUT_OF_SERVICE = "OutOfService"
    OUT_OF_ORDER = "OutOfOrder"
    OUT_OF_INVENTORY = "OutOfInventory"
