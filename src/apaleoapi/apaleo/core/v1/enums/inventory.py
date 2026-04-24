from enum import Enum


class PropertyStatus(str, Enum):
    """Property status enum."""

    LIVE = "Live"
    TEST = "Test"


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
