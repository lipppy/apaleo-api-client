from enum import Enum


class ChannelCode(str, Enum):
    DIRECT = "Direct"
    BOOKING_COM = "BookingCom"
    IBE = "Ibe"
    CHANNEL_MANAGER = "ChannelManager"
    EXPEDIA = "Expedia"
    HOMELIKE = "Homelike"
    HRS = "Hrs"
    ALTO_VITA = "AltoVita"
    DES_VU = "DesVu"


class MinGuaranteeType(str, Enum):
    PM6_HOLD = "PM6Hold"
    CREDIT_CARD = "CreditCard"
    PREPAYMENT = "Prepayment"
    COMPANY = "Company"


class PriceCalculationMode(str, Enum):
    TRUNCATE = "Truncate"
    ROUND = "Round"


class UnitGroupType(str, Enum):
    BED_ROOM = "BedRoom"
    MEETING_ROOM = "MeetingRoom"
    EVENT_SPACE = "EventSpace"
    PARKING_LOT = "ParkingLot"
    OTHER = "Other"


class TimeSliceTemplate(str, Enum):
    DAY_USE = "DayUse"
    OVER_NIGHT = "OverNight"


class VatType(str, Enum):
    NULL = "Null"
    VERY_REDUCED = "VeryReduced"
    REDUCED = "Reduced"
    NORMAL = "Normal"
    WITHOUT = "Without"
    SPECIAL = "Special"
    REDUCED_COVID19 = "ReducedCovid19"
    NORMAL_COVID19 = "NormalCovid19"
    MIXED = "Mixed"


class ServiceType(str, Enum):
    OTHER = "Other"
    ACCOMMODATION = "Accommodation"
    FOOD_AND_BEVERAGES = "FoodAndBeverages"


class SurchargeType(str, Enum):
    ABSOLUTE = "Absolute"
    PERCENT = "Percent"


class PricingRuleType(str, Enum):
    ABSOLUTE = "Absolute"
    PERCENT = "Percent"


class PricingUnit(str, Enum):
    ROOM = "Room"
    PERSON = "Person"
