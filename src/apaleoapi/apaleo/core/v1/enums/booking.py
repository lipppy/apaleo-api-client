from enum import Enum


class ReservationStatus(str, Enum):
    """Reservation status enum."""

    CONFIRMED = "Confirmed"
    IN_HOUSE = "InHouse"
    CHECKED_OUT = "CheckedOut"
    CANCELED = "Canceled"
    NO_SHOW = "NoShow"


class ChannelCode(str, Enum):
    """Channel code enum."""

    DIRECT = "Direct"
    BOOKING_COM = "BookingCom"
    IBE = "Ibe"
    CHANNEL_MANAGER = "ChannelManager"
    EXPEDIA = "Expedia"
    HOMELIKE = "Homelike"
    HRS = "Hrs"
    ALTO_VITA = "AltoVita"
    DES_VU = "DesVu"


class GuaranteeType(str, Enum):
    """Guarantee type enum."""

    PM6_HOLD = "PM6Hold"
    CREDIT_CARD = "CreditCard"
    PREPAYMENT = "Prepayment"
    COMPANY = "Company"
    OTA = "Ota"


class TravelPurpose(str, Enum):
    """Travel purpose enum."""

    BUSINESS = "Business"
    LEISURE = "Leisure"


class UnitGroupType(str, Enum):
    """Unit group type enum."""

    BED_ROOM = "BedRoom"
    MEETING_ROOM = "MeetingRoom"
    EVENT_SPACE = "EventSpace"
    PARKING_LOT = "ParkingLot"
    OTHER = "Other"


class Gender(str, Enum):
    """Gender enum."""

    FEMALE = "Female"
    MALE = "Male"
    OTHER = "Other"
    UNKNOWN = "Unknown"


class Title(str, Enum):
    """Title enum."""

    MR = "Mr"
    MS = "Ms"
    DR = "Dr"
    PROF = "Prof"
    MRS = "Mrs"
    OTHER = "Other"


class IdentificationType(str, Enum):
    """Identification type enum."""

    SOCIAL_INSURANCE_NUMBER = "SocialInsuranceNumber"
    PASSPORT_NUMBER = "PassportNumber"
    ID_NUMBER = "IdNumber"
    DRIVER_LICENSE_NUMBER = "DriverLicenseNumber"
    VISA_NUMBER = "VisaNumber"
    FOREIGNER_IDENTITY_NUMBER = "ForeignerIdentityNumber"
    TAX_IDENTIFICATION_NUMBER = "TaxIdentificationNumber"
    OTHER = "Other"


class RelationshipToPrimaryGuest(str, Enum):
    """Relationship to primary guest enum."""

    GRANDPARENT = "Grandparent"
    GRANDCHILD = "Grandchild"
    GREAT_GRANDPARENT = "GreatGrandparent"
    GREAT_GRANDCHILD = "GreatGrandchild"
    PARENT = "Parent"
    CHILD = "Child"
    SIBLING = "Sibling"
    PARENT_IN_LAW = "ParentInLaw"
    CHILD_IN_LAW = "ChildInLaw"
    SIBLING_IN_LAW = "SiblingInLaw"
    SPOUSE = "Spouse"
    UNCLE_OR_AUNT = "UncleOrAunt"
    NEPHEW_OR_NIECE = "NephewOrNiece"
    GUARDIAN = "Guardian"
    OTHER = "Other"


class VatType(str, Enum):
    """VAT type enum."""

    NULL = "Null"
    VERY_REDUCED = "VeryReduced"
    REDUCED = "Reduced"
    NORMAL = "Normal"
    WITHOUT = "Without"
    SPECIAL = "Special"
    REDUCED_COVID19 = "ReducedCovid19"
    NORMAL_COVID19 = "NormalCovid19"
    MIXED = "Mixed"


class PricingUnit(str, Enum):
    """Pricing unit enum."""

    ROOM = "Room"
    PERSON = "Person"


class ValidationMessageCategory(str, Enum):
    """Validation message category enum."""

    OFFER_NOT_AVAILABLE = "OfferNotAvailable"
    AUTO_UNIT_ASSIGNMENT = "AutoUnitAssignment"


class ValidationMessageCode(str, Enum):
    """Validation message code enum."""

    UNIT_GROUP_FULLY_BOOKED = "UnitGroupFullyBooked"
    UNIT_GROUP_CAPACITY_EXCEEDED = "UnitGroupCapacityExceeded"
    RATE_PLAN_RESTRICTIONS_VIOLATED = "RatePlanRestrictionsViolated"
    RATE_PLAN_SURCHARGES_NOT_SET = "RatePlanSurchargesNotSet"
    RATE_RESTRICTIONS_VIOLATED = "RateRestrictionsViolated"
    RATE_PLAN_CHANNEL_NOT_SET = "RatePlanChannelNotSet"
    RATES_NOT_SET = "RatesNotSet"
    BLOCK_FULLY_BOOKED = "BlockFullyBooked"
    UNIT_MOVED = "UnitMoved"
    INCLUDED_SERVICES_AMOUNT_EXCEEDED_RATE_AMOUNT = "IncludedServicesAmountExceededRateAmount"
    RATE_PLAN_COMPANY_RESTRICTIONS_VIOLATED = "RatePlanCompanyRestrictionsViolated"
    SERVICE_FULLY_BOOKED = "ServiceFullyBooked"
    HURDLE_RATES_VIOLATED = "HurdleRatesViolated"
