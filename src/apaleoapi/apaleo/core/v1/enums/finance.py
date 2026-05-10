from enum import Enum


class Action(str, Enum):
    CANCEL = "Cancel"
    ONLINE_REFUND = "OnlineRefund"
    MANUAL_REFUND = "ManualRefund"


class Command(str, Enum):
    POST_CHARGE = "PostCharge"
    POST_PAYMENT = "PostPayment"
    MOVE_LINE_ITEM = "MoveLineItem"
    POST_PREPAYMENT = "PostPrepayment"
    POST_TO_ACCOUNTS_RECEIVABLES = "PostToAccountsReceivables"
    POST_PREPAYMENT_VAT = "PostPrepaymentVat"
    POST_TO_LOSS_OF_ACCOUNTS_RECEIVABLES = "PostToLossOfAccountsReceivables"
    SYSTEM = "System"


class CreateInvoiceAction(str, Enum):
    CANNOT_CREATE_INVOICE = "CannotCreateInvoice"
    CREATES_INVOICE = "CreatesInvoice"
    CREATES_INVOICE_AND_CLOSES_FOLIO = "CreatesInvoiceAndClosesFolio"
    CREATES_AR_INVOICE_AND_CLOSES_FOLIO = "CreatesArInvoiceAndClosesFolio"


class ReasonCode(str, Enum):
    CHANGE_OF_RECIPIENT_DETAILS = "ChangeOfRecipientDetails"
    CHANGE_OF_INVOICE_RECIPIENT = "ChangeOfInvoiceRecipient"
    CHANGE_OF_PAYMENT_METHOD = "ChangeOfPaymentMethod"
    CHANGE_OF_INVOICE_TRANSACTIONS = "ChangeOfInvoiceTransactions"
    OTHER = "Other"


class ReferenceType(str, Enum):
    HOUSE = "House"
    GUEST = "Guest"
    EXTERNAL = "External"
    BOOKING = "Booking"


class ServiceType(str, Enum):
    OTHER = "Other"
    ACCOMMODATION = "Accommodation"
    FOOD_AND_BEVERAGES = "FoodAndBeverages"
    CANCELLATION_FEES = "CancellationFees"
    NO_SHOW = "NoShow"
    CITY_TAX = "CityTax"
    SECOND_CITY_TAX = "SecondCityTax"


class VatType(str, Enum):
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
