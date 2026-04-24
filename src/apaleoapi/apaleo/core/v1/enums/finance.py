from enum import Enum


class ServiceType(str, Enum):
    OTHER = "Other"
    ACCOMMODATION = "Accommodation"
    FOOD_AND_BEVERAGES = "FoodAndBeverages"
    CITY_TAX = "CityTax"
    SECONND_CITY_TAX = "SecondCityTax"


class VatType(str, Enum):
    """VAT type enum."""

    NULL = "Null"
    VERY_REDUCED = "VeryReduced"
    REDUCED = "Reduced"
    NORMAL = "Normal"
    WITHOUT = "Without"
    SPECIAL = "Special"
    SPECIAL1 = "Special1"
    SPECIAL2 = "Special2"
    REDUCED_COVID19 = "ReducedCovid19"
    NORMAL_COVID19 = "NormalCovid19"
    MIXED = "Mixed"


class FolioType(str, Enum):
    """Folio type enum."""

    GUEST = "Guest"
    EXTERNAL = "External"


class FolioDebitorType(str, Enum):
    """Folio debitor type enum."""

    BOOKER = "Booker"
    PRIMARY_GUEST = "PrimaryGuest"
    COMPANY = "Company"
    ADDITIONAL_GUEST = "AdditionalGuest"
    PROPERTY = "Property"


class Title(Enum):
    """Title enum."""

    Mr = "Mr"
    Ms = "Ms"
    Dr = "Dr"
    Prof = "Prof"
    Mrs = "Mrs"
    Other = "Other"


class Method(Enum):
    CASH = "Cash"
    BANK_TRANSFER = "BankTransfer"
    CREDIT_CARD = "CreditCard"
    AMEX = "Amex"
    VISA_CREDIT = "VisaCredit"
    VISA_DEBIT = "VisaDebit"
    MASTER_CARD = "MasterCard"
    MASTER_CARD_DEBIT = "MasterCardDebit"
    MAESTRO = "Maestro"
    GIRO_CARD = "GiroCard"
    DISCOVER_CARD = "DiscoverCard"
    DINERS = "Diners"
    JCB = "Jcb"
    BOOKING_COM = "BookingCom"
    V_PAY = "VPay"
    PAY_PAL = "PayPal"
    POSTCARD = "Postcard"
    REKA = "Reka"
    TWINT = "Twint"
    LUNCHCHECK = "Lunchcheck"
    VOUCHER = "Voucher"
    CHINA_UNION_PAY = "ChinaUnionPay"
    OTHER = "Other"
    CHEQUE = "Cheque"
    AIRBNB = "Airbnb"
    HOLIDAY_CHECK = "HolidayCheck"
    REPRESENTATION = "Representation"
    I_DEAL = "IDeal"
