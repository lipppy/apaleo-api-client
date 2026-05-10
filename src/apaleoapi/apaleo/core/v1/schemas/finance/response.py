"""
Pydantic schemas for Apaleo Finance API endpoints.
Generated from Apaleo Finance API Swagger documentation.

API doc: https://api.apaleo.com/swagger/index.html?urls.primaryName=Finance+V1
"""

from datetime import date as date_aliased
from enum import StrEnum
from typing import Any

from pydantic import AwareDatetime, EmailStr, Field

from apaleoapi.apaleo.common.schemas.base import (
    ExtendedBaseModel,
)
from apaleoapi.apaleo.core.v1.enums.finance import (
    Action,
    Command,
    CreateInvoiceAction,
    Method,
    ReasonCode,
    ReferenceType,
    ServiceType,
    VatType,
)


class AddedChargeModel(ExtendedBaseModel):
    id: str = Field(...)
    fee_charge_ids: list[str] | None = Field(None, alias="feeChargeIds")


class AddressModel(ExtendedBaseModel):
    address_line1: str = Field(..., alias="addressLine1", min_length=1)
    address_line2: str | None = Field(None, alias="addressLine2")
    postal_code: str = Field(..., alias="postalCode", min_length=1)
    city: str = Field(..., min_length=1)
    region_code: str | None = Field(None, alias="regionCode")
    country_code: str = Field(..., alias="countryCode")


class AmountModel(ExtendedBaseModel):
    gross_amount: float = Field(..., alias="grossAmount")
    net_amount: float = Field(..., alias="netAmount")
    vat_type: VatType = Field(..., alias="vatType")
    vat_percent: float = Field(..., alias="vatPercent")
    currency: str


class BankAccountModel(ExtendedBaseModel):
    iban: str | None = None
    bic: str | None = None
    bank: str | None = None


class BulkAllowanceCreatedItemModel(ExtendedBaseModel):
    id: str = Field(...)
    source_charge_id: str = Field(..., alias="sourceChargeId")


class BulkAllowanceCreatedModel(ExtendedBaseModel):
    items: list[BulkAllowanceCreatedItemModel] = Field(...)


class BulkMoveItemRequest(ExtendedBaseModel):
    source_folio_id: str = Field(..., alias="sourceFolioId")
    target_folio_id: str = Field(..., alias="targetFolioId")
    charge_ids: list[str] | None = Field(None, alias="chargeIds")


class BulkMoveRequest(ExtendedBaseModel):
    items: list[BulkMoveItemRequest] = Field(...)
    reason: str = Field(..., min_length=1)


class CancelInvoiceRequest(ExtendedBaseModel):
    reason_code: ReasonCode = Field(..., alias="reasonCode")


class Type(StrEnum):
    direct = "Direct"
    time_slice = "TimeSlice"
    included_service = "IncludedService"
    extra_service = "ExtraService"
    city_tax = "CityTax"
    no_show_fee = "NoShowFee"
    cancellation_fee = "CancellationFee"
    service_fee = "ServiceFee"
    tax = "Tax"
    second_city_tax = "SecondCityTax"


class CommercialInfoModel(ExtendedBaseModel):
    register_entry: str = Field(..., alias="registerEntry", min_length=1)
    tax_id: str = Field(..., alias="taxId", min_length=1)
    managing_directors: str | None = Field(None, alias="managingDirectors")


class CorrectFolioRequest(ExtendedBaseModel):
    reason: str = Field(..., min_length=1)
    charge_ids: list[str] | None = Field(None, alias="chargeIds")
    allowance_ids: list[str] | None = Field(None, alias="allowanceIds")
    transitory_charge_ids: list[str] | None = Field(None, alias="transitoryChargeIds")


class CountModel(ExtendedBaseModel):
    count: int


class AccountOwner(StrEnum):
    guest = "Guest"
    booker = "Booker"


class ServiceType2(StrEnum):
    other = "Other"
    accommodation = "Accommodation"
    food_and_beverages = "FoodAndBeverages"
    city_tax = "CityTax"
    second_city_tax = "SecondCityTax"


class ReferenceType1(StrEnum):
    psp_reference = "PspReference"
    authorization_id = "AuthorizationId"


class Type1(StrEnum):
    guest = "Guest"
    external = "External"


class CreateInvoiceRequest(ExtendedBaseModel):
    folio_id: str = Field(..., alias="folioId")
    language_code: str = Field(..., alias="languageCode")


class Type2(StrEnum):
    invoice_already_exists = "InvoiceAlreadyExists"
    not_all_charges_posted = "NotAllChargesPosted"
    debitor_details_missing = "DebitorDetailsMissing"
    invoice_has_pending_payments = "InvoiceHasPendingPayments"
    no_company_found = "NoCompanyFound"
    company_cannot_check_out_on_ar = "CompanyCannotCheckOutOnAr"
    is_house_folio = "IsHouseFolio"
    cannot_create_company_invoice_for_external = "CannotCreateCompanyInvoiceForExternal"
    check_out_on_ar_is_not_allowed = "CheckOutOnArIsNotAllowed"
    is_empty_folio = "IsEmptyFolio"
    cash_payment_limit_exceeded = "CashPaymentLimitExceeded"
    folio_state = "FolioState"


class CreateInvoiceWarningModel(ExtendedBaseModel):
    type: Type2 = Field(...)
    message: str | None = Field(None)


class CreatedSubResourceIdModel(ExtendedBaseModel):
    id: str


class CurrencyListModel(ExtendedBaseModel):
    iso_currencies: list[str] = Field(..., alias="isoCurrencies")


class EmbeddedCompanyModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str | None = Field(None)
    name: str | None = Field(None)
    can_check_out_on_ar: bool | None = Field(None, alias="canCheckOutOnAr")


class EmbeddedFolioModel(ExtendedBaseModel):
    id: str = Field(...)
    debitor: str | None = Field(None)


class EmbeddedInvoiceModel(ExtendedBaseModel):
    id: str = Field(...)


class EmbeddedPropertyModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str | None = Field(None)
    name: str | None = Field(None)
    description: str | None = Field(None)


class EmbeddedReservationModel(ExtendedBaseModel):
    id: str = Field(...)
    booking_id: str = Field(..., alias="bookingId")


class Type3(StrEnum):
    revenues = "Revenues"
    payments = "Payments"
    liabilities = "Liabilities"
    receivables = "Receivables"
    vat = "Vat"
    house = "House"
    accounts_receivable = "AccountsReceivable"
    city_taxes = "CityTaxes"
    transitory_items = "TransitoryItems"
    vat_on_liabilities = "VatOnLiabilities"
    loss_of_accounts_receivable = "LossOfAccountsReceivable"
    second_city_tax = "SecondCityTax"


class ExportAccountModel(ExtendedBaseModel):
    name: str = Field(..., min_length=1)
    number: str = Field(..., min_length=1)
    parent_number: str | None = Field(None, alias="parentNumber")
    type: Type3 = Field(...)


class ExternalReference(ExtendedBaseModel):
    merchant_reference: str = Field(..., alias="merchantReference", min_length=1)
    psp_reference: str = Field(..., alias="pspReference", min_length=1)


class FolioCreatedModel(ExtendedBaseModel):
    id: str = Field(...)


class Type5(StrEnum):
    booker = "Booker"
    primary_guest = "PrimaryGuest"
    company = "Company"
    additional_guest = "AdditionalGuest"
    property = "Property"


class Title(StrEnum):
    mr = "Mr"
    ms = "Ms"
    dr = "Dr"
    prof = "Prof"
    mrs = "Mrs"
    other = "Other"


class FolioWarning(StrEnum):
    incomplete_billing_address = "IncompleteBillingAddress"
    incomplete_billing_details = "IncompleteBillingDetails"


class AllowedAction(StrEnum):
    add_charge = "AddCharge"
    add_deposit_item = "AddDepositItem"
    add_allowance = "AddAllowance"
    add_cancellation_fee = "AddCancellationFee"
    add_no_show_fee = "AddNoShowFee"
    add_payment = "AddPayment"
    add_refund = "AddRefund"
    checkout_on_ar = "CheckoutOnAr"
    close = "Close"
    post_open_charges = "PostOpenCharges"
    correct_folio = "CorrectFolio"
    change_address = "ChangeAddress"
    change_address_with_simple_debitor = "ChangeAddressWithSimpleDebitor"
    delete = "Delete"
    reopen = "Reopen"
    create_invoice = "CreateInvoice"
    create_advance_invoice = "CreateAdvanceInvoice"
    cancel_last_invoice = "CancelLastInvoice"
    create_invoice_with_simple_debitor = "CreateInvoiceWithSimpleDebitor"
    create_prepayment_notice = "CreatePrepaymentNotice"
    create_pro_forma_invoice = "CreateProFormaInvoice"
    create_deposit_receipt = "CreateDepositReceipt"
    preview_invoice = "PreviewInvoice"


class Status(StrEnum):
    open = "Open"
    closed = "Closed"
    closed_with_invoice = "ClosedWithInvoice"


class Method2(StrEnum):
    cash = "Cash"
    bank_transfer = "BankTransfer"
    credit_card = "CreditCard"
    invoice = "Invoice"
    amex = "Amex"
    visa_credit = "VisaCredit"
    visa_debit = "VisaDebit"
    master_card = "MasterCard"
    master_card_debit = "MasterCardDebit"
    maestro = "Maestro"
    giro_card = "GiroCard"
    discover_card = "DiscoverCard"
    diners = "Diners"
    jcb = "Jcb"
    booking_com = "BookingCom"
    v_pay = "VPay"
    pay_pal = "PayPal"
    postcard = "Postcard"
    reka = "Reka"
    twint = "Twint"
    lunchcheck = "Lunchcheck"
    voucher = "Voucher"
    china_union_pay = "ChinaUnionPay"
    other = "Other"
    cheque = "Cheque"
    airbnb = "Airbnb"
    holiday_check = "HolidayCheck"
    psp_cash = "PspCash"
    psp_debit = "PspDebit"
    psp_banking = "PspBanking"
    psp_open_invoice = "PspOpenInvoice"
    psp_wallet = "PspWallet"
    representation = "Representation"
    i_deal = "IDeal"


class Status2(StrEnum):
    pending = "Pending"
    success = "Success"
    failure = "Failure"
    canceled = "Canceled"


class FailureCode(StrEnum):
    failed = "Failed"
    timed_out = "TimedOut"


class Type8(StrEnum):
    custom = "Custom"
    terminal = "Terminal"
    payment_account = "PaymentAccount"
    authorization = "Authorization"
    payment_link = "PaymentLink"
    pre_authorization = "PreAuthorization"


class InvoiceCreatedModel(ExtendedBaseModel):
    id: str = Field(...)


class Type9(StrEnum):
    initial = "Initial"
    cancellation = "Cancellation"
    correction = "Correction"
    advance = "Advance"
    advance_cancellation = "AdvanceCancellation"
    advance_correction = "AdvanceCorrection"
    proforma = "Proforma"


class Status3(StrEnum):
    fully_paid = "FullyPaid"
    unpaid = "Unpaid"
    written_off = "WrittenOff"


class AllowedAction2(StrEnum):
    correct_address = "CorrectAddress"
    correct_charges = "CorrectCharges"
    mark_as_paid = "MarkAsPaid"
    cancel = "Cancel"
    write_off = "WriteOff"


class Network(StrEnum):
    peppol = "Peppol"


class InvoiceNetworkIdentityModel(ExtendedBaseModel):
    network: Network = Field(...)
    id: str = Field(..., min_length=1)


class InvoiceSenderModel(ExtendedBaseModel):
    name: str = Field(..., min_length=1)
    address: AddressModel | None = None


class MessageItemCollection(ExtendedBaseModel):
    messages: list[str] | None = None


class MonetaryValueModel(ExtendedBaseModel):
    amount: float
    currency: str


class MoveAllChargesRequest(ExtendedBaseModel):
    target_folio_id: str = Field(..., alias="targetFolioId")
    reason: str = Field(..., min_length=1)


class MoveChargesRequest(ExtendedBaseModel):
    target_folio_id: str = Field(..., alias="targetFolioId")
    reason: str = Field(..., min_length=1)
    charge_ids: list[str] | None = Field(None, alias="chargeIds")
    allowance_ids: list[str] | None = Field(None, alias="allowanceIds")
    transitory_charge_ids: list[str] | None = Field(None, alias="transitoryChargeIds")


class MovePaymentsRequest(ExtendedBaseModel):
    target_folio_id: str = Field(..., alias="targetFolioId")
    reason: str = Field(..., min_length=1)
    payment_ids: list[str] = Field(..., alias="paymentIds")


class NonStrictAddressModel(ExtendedBaseModel):
    address_line1: str | None = Field(None, alias="addressLine1")
    address_line2: str | None = Field(None, alias="addressLine2")
    postal_code: str | None = Field(None, alias="postalCode")
    city: str | None = None
    region_code: str | None = Field(None, alias="regionCode")
    country_code: str | None = Field(None, alias="countryCode")


class Operation(ExtendedBaseModel):
    value: Any | None = None
    path: str | None = None
    op: str | None = None
    from_: str | None = Field(None, alias="from")


class PayInvoiceRequest(ExtendedBaseModel):
    payment_method: Method = Field(..., alias="paymentMethod")
    receipt: str = Field(..., min_length=1)


class PaymentCreatedModel(CreatedSubResourceIdModel):
    pass


class PaymentMethodListModel(ExtendedBaseModel):
    payment_methods: list[Method] = Field(..., alias="paymentMethods")


class PaymentModel(ExtendedBaseModel):
    id: str = Field(...)
    method: Method2 = Field(...)
    amount: MonetaryValueModel
    external_reference: ExternalReference | None = Field(None, alias="externalReference")
    receipt: str | None = Field(None)
    payment_date: AwareDatetime | None = Field(None, alias="paymentDate")
    moved_from: EmbeddedFolioModel | None = Field(None, alias="movedFrom")
    moved_to: EmbeddedFolioModel | None = Field(None, alias="movedTo")
    moved_reason: str | None = Field(None, alias="movedReason")
    source_payment_id: str | None = Field(None, alias="sourcePaymentId")
    business_date: date_aliased = Field(..., alias="businessDate", examples=["2020-10-10"])


class PaymentPaidChargesRequest(ExtendedBaseModel):
    charge_id: str = Field(..., alias="chargeId")
    amount: float = Field(...)


class PendingPaymentModel(ExtendedBaseModel):
    id: str = Field(...)
    amount: MonetaryValueModel
    terminal_id: str | None = Field(None, alias="terminalId")


class PreciseMonetaryValueModel(MonetaryValueModel):
    pass


class Type11(StrEnum):
    custom = "Custom"
    reservation = "Reservation"
    invoice = "Invoice"
    psp_reference = "PspReference"


class ReceiptModel(ExtendedBaseModel):
    type: Type11 | None = Field(None)
    number: str = Field(..., min_length=1)


class RefundCreatedModel(CreatedSubResourceIdModel):
    pass


class RefundModel(ExtendedBaseModel):
    id: str = Field(...)
    method: Method2 = Field(...)
    amount: MonetaryValueModel
    external_reference: ExternalReference | None = Field(None, alias="externalReference")
    receipt: str | None = Field(None)
    refund_date: AwareDatetime = Field(..., alias="refundDate")
    source_payment_id: str | None = Field(None, alias="sourcePaymentId")
    status: Status2 = Field(...)
    failure_reason: str | None = Field(None, alias="failureReason")
    failure_code: FailureCode | None = Field(None, alias="failureCode")
    moved_from: EmbeddedFolioModel | None = Field(None, alias="movedFrom")
    moved_to: EmbeddedFolioModel | None = Field(None, alias="movedTo")
    moved_reason: str | None = Field(None, alias="movedReason")
    business_date: date_aliased = Field(..., alias="businessDate", examples=["2020-10-10"])
    reason: str | None = Field(None)


class ServiceTypeListModel(ExtendedBaseModel):
    service_types: list[ServiceType] = Field(..., alias="serviceTypes")


class Type13(StrEnum):
    by_percent = "ByPercent"
    by_amount = "ByAmount"


class SplitChargeRequest(ExtendedBaseModel):
    percent: float | None = Field(None)
    amount: MonetaryValueModel | None = None
    type: Type13 = Field(...)


class SplitChargeResult(ExtendedBaseModel):
    allowance_id: str = Field(..., alias="allowanceId")
    first_charge_id: str = Field(..., alias="firstChargeId")
    second_charge_id: str = Field(..., alias="secondChargeId")


class SplitPaymentRequest(ExtendedBaseModel):
    percent: float | None = Field(None)
    amount: MonetaryValueModel | None = None
    type: Type13 = Field(...)


class SplitPaymentResult(ExtendedBaseModel):
    refund_id: str | None = Field(None, alias="refundId")
    first_payment_id: str | None = Field(None, alias="firstPaymentId")
    second_payment_id: str | None = Field(None, alias="secondPaymentId")


class StayInfoModel(ExtendedBaseModel):
    guest_name: str = Field(..., alias="guestName", min_length=1)
    arrival_date: date_aliased = Field(..., alias="arrivalDate", examples=["2020-10-10"])
    departure_date: date_aliased = Field(..., alias="departureDate", examples=["2020-10-10"])
    reservation_id: str = Field(..., alias="reservationId", min_length=1)
    room_number: str | None = Field(None, alias="roomNumber")


class TaxAmountModel(ExtendedBaseModel):
    type: VatType = Field(...)
    percent: float = Field(...)
    amount: float = Field(...)


class TaxDetailModel(ExtendedBaseModel):
    vat_type: VatType = Field(..., alias="vatType")
    vat_percent: float = Field(..., alias="vatPercent")
    net: MonetaryValueModel
    tax: MonetaryValueModel


class TransitoryChargeModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1)
    amount: MonetaryValueModel
    service_type: ServiceType | None = Field(None, alias="serviceType")
    service_date: date_aliased = Field(..., alias="serviceDate", examples=["2020-10-10"])
    created: AwareDatetime = Field(...)
    receipt: str | None = Field(None)
    moved_from: EmbeddedFolioModel | None = Field(None, alias="movedFrom")
    moved_to: EmbeddedFolioModel | None = Field(None, alias="movedTo")
    moved_reason: str | None = Field(None, alias="movedReason")
    quantity: int = Field(...)


class VatItemModel(ExtendedBaseModel):
    type: VatType = Field(...)
    percent: float = Field(...)


class VatListModel(ExtendedBaseModel):
    vat_types: list[VatItemModel] | None = Field(None, alias="vatTypes")


class Code(StrEnum):
    cancel_not_allowed_for_payment_not_in_status_pending = (
        "CancelNotAllowedForPaymentNotInStatusPending"
    )
    cancel_not_allowed_for_payment_not_of_payment_link_type = (
        "CancelNotAllowedForPaymentNotOfPaymentLinkType"
    )
    online_refund_not_allowed_for_restricted_payment_method_or_acquirer = (
        "OnlineRefundNotAllowedForRestrictedPaymentMethodOrAcquirer"
    )
    manual_refund_not_allowed_when_online_refund_is_possible = (
        "ManualRefundNotAllowedWhenOnlineRefundIsPossible"
    )
    cancel_not_allowed_for_incomplete_payment_link = "CancelNotAllowedForIncompletePaymentLink"


class ActionReasonModelNotAllowedPaymentActionReason(ExtendedBaseModel):
    code: Code
    message: str = Field(..., min_length=1)


class AccountingTransactionModel(ExtendedBaseModel):
    timestamp: AwareDatetime = Field(...)
    date: date_aliased = Field(..., examples=["2020-10-10"])
    debited_account: ExportAccountModel = Field(..., alias="debitedAccount")
    credited_account: ExportAccountModel = Field(..., alias="creditedAccount")
    command: Command = Field(...)
    amount: PreciseMonetaryValueModel
    receipt: ReceiptModel | None = None
    entry_number: str = Field(..., alias="entryNumber", min_length=1)
    reference: str = Field(...)
    reference_type: ReferenceType = Field(..., alias="referenceType")
    entry_group_number: str = Field(..., alias="entryGroupNumber", min_length=1)


class AccountingTransactionPairModel(ExtendedBaseModel):
    debited_account: ExportAccountModel = Field(..., alias="debitedAccount")
    credited_account: ExportAccountModel = Field(..., alias="creditedAccount")
    amount: PreciseMonetaryValueModel


class AggregateTransactionItemModel(ExtendedBaseModel):
    account: ExportAccountModel
    credited_amount: PreciseMonetaryValueModel = Field(..., alias="creditedAmount")
    debited_amount: PreciseMonetaryValueModel = Field(..., alias="debitedAmount")
    balance: PreciseMonetaryValueModel


class AggregatesTotalModel(ExtendedBaseModel):
    credited_amount: PreciseMonetaryValueModel = Field(..., alias="creditedAmount")
    debited_amount: PreciseMonetaryValueModel = Field(..., alias="debitedAmount")
    balance: PreciseMonetaryValueModel


class AllowanceModel(ExtendedBaseModel):
    id: str = Field(...)
    amount: AmountModel
    reason: str = Field(..., min_length=1)
    service_type: ServiceType = Field(..., alias="serviceType")
    service_date: date_aliased = Field(..., alias="serviceDate", examples=["2020-10-10"])
    created: AwareDatetime = Field(...)
    moved_from: EmbeddedFolioModel | None = Field(None, alias="movedFrom")
    moved_to: EmbeddedFolioModel | None = Field(None, alias="movedTo")
    moved_reason: str | None = Field(None, alias="movedReason")
    source_charge_id: str | None = Field(None, alias="sourceChargeId")
    sub_account_id: str | None = Field(None, alias="subAccountId")


class ChargeModel(ExtendedBaseModel):
    id: str = Field(...)
    service_type: ServiceType = Field(..., alias="serviceType")
    name: str = Field(..., min_length=1)
    translated_names: dict[str, str] | None = Field(None, alias="translatedNames")
    is_posted: bool = Field(..., alias="isPosted")
    service_date: date_aliased = Field(..., alias="serviceDate", examples=["2020-10-10"])
    created: AwareDatetime = Field(...)
    moved_from: EmbeddedFolioModel | None = Field(None, alias="movedFrom")
    moved_to: EmbeddedFolioModel | None = Field(None, alias="movedTo")
    moved_reason: str | None = Field(None, alias="movedReason")
    routed_from: EmbeddedFolioModel | None = Field(None, alias="routedFrom")
    routed_to: EmbeddedFolioModel | None = Field(None, alias="routedTo")
    amount: AmountModel
    receipt: str | None = Field(None)
    group_id: str | None = Field(None, alias="groupId")
    sub_account_id: str | None = Field(None, alias="subAccountId")
    quantity: int = Field(...)
    type: Type = Field(...)


class CompanyInfoModel(ExtendedBaseModel):
    name: str = Field(..., min_length=1)
    tax_id: str | None = Field(None, alias="taxId")
    additional_tax_id: str | None = Field(None, alias="additionalTaxId")
    additional_tax_id2: str | None = Field(None, alias="additionalTaxId2")
    invoice_network_identity: InvoiceNetworkIdentityModel | None = Field(
        None, alias="invoiceNetworkIdentity"
    )


class CreateAccountPaymentRequest(ExtendedBaseModel):
    account_owner: AccountOwner | None = Field(None, alias="accountOwner")
    payment_account_id: str | None = Field(None, alias="paymentAccountId")
    amount: MonetaryValueModel
    paid_charges: list[PaymentPaidChargesRequest] | None = Field(None, alias="paidCharges")


class CreateAllowanceBulkItemModel(ExtendedBaseModel):
    charge_id: str = Field(..., alias="chargeId")
    amount: MonetaryValueModel


class CreateAllowanceBulkModel(ExtendedBaseModel):
    items: list[CreateAllowanceBulkItemModel] = Field(...)
    reason: str = Field(..., min_length=1)
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])


class CreateAllowanceForChargeModel(ExtendedBaseModel):
    reason: str = Field(..., min_length=1)
    amount: MonetaryValueModel
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])


class CreateAllowanceForFolioModel(ExtendedBaseModel):
    service_type: ServiceType2 = Field(..., alias="serviceType")
    vat_type: VatType = Field(..., alias="vatType")
    sub_account_id: str | None = Field(None, alias="subAccountId")
    reason: str = Field(..., min_length=1)
    amount: MonetaryValueModel
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])


class CreateAuthorizationPaymentRequest(ExtendedBaseModel):
    transaction_reference: str = Field(..., alias="transactionReference", min_length=1)
    reference_type: ReferenceType1 | None = Field(None, alias="referenceType")
    amount: MonetaryValueModel
    paid_charges: list[PaymentPaidChargesRequest] | None = Field(None, alias="paidCharges")


class CreateChargeModel(ExtendedBaseModel):
    service_type: ServiceType2 = Field(..., alias="serviceType")
    vat_type: VatType = Field(..., alias="vatType")
    sub_account_id: str | None = Field(None, alias="subAccountId")
    name: str = Field(..., min_length=1)
    amount: MonetaryValueModel
    receipt: str | None = Field(None)
    quantity: int | None = Field(None)
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])


class CreateCustomPaymentRequest(ExtendedBaseModel):
    method: Method = Field(...)
    receipt: str | None = Field(None)
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])
    amount: MonetaryValueModel
    paid_charges: list[PaymentPaidChargesRequest] | None = Field(None, alias="paidCharges")


class CreateFolioRefundRequest(ExtendedBaseModel):
    method: Method = Field(...)
    amount: MonetaryValueModel
    receipt: str | None = Field(None)
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])
    reason: str | None = Field(None)


class CreatePaymentLinkRequest(ExtendedBaseModel):
    expires_at: AwareDatetime = Field(..., alias="expiresAt")
    country_code: str = Field(..., alias="countryCode", min_length=1)
    description: str | None = Field(None, max_length=280)
    payer_email: EmailStr | None = Field(None, alias="payerEmail")
    amount: MonetaryValueModel
    paid_charges: list[PaymentPaidChargesRequest] | None = Field(None, alias="paidCharges")


class CreatePaymentRefundRequest(ExtendedBaseModel):
    amount: MonetaryValueModel
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])
    reason: str | None = Field(None)


class CreateTerminalPaymentRequest(ExtendedBaseModel):
    terminal_id: str = Field(..., alias="terminalId", min_length=1)
    amount: MonetaryValueModel
    paid_charges: list[PaymentPaidChargesRequest] | None = Field(None, alias="paidCharges")


class CreateTransitoryChargeModel(ExtendedBaseModel):
    name: str = Field(..., min_length=1)
    amount: MonetaryValueModel
    receipt: str | None = Field(None)
    group_id: str | None = Field(None, alias="groupId")
    service_type: ServiceType2 | None = Field(None, alias="serviceType")
    quantity: int | None = Field(None)
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])


class ExportGrossTransactionItemModel(ExtendedBaseModel):
    timestamp: AwareDatetime = Field(...)
    date: date_aliased = Field(..., examples=["2020-10-10"])
    debited_account: ExportAccountModel = Field(..., alias="debitedAccount")
    credited_account: ExportAccountModel = Field(..., alias="creditedAccount")
    command: Command = Field(...)
    currency: str = Field(...)
    gross_amount: float = Field(..., alias="grossAmount")
    net_amount: float = Field(..., alias="netAmount")
    taxes: list[TaxAmountModel] | None = Field(None)
    receipt: ReceiptModel
    source_entry_number: str = Field(..., alias="sourceEntryNumber", min_length=1)
    reference: str = Field(...)
    reference_type: ReferenceType = Field(..., alias="referenceType")


class ExportGrossTransactionListModel(ExtendedBaseModel):
    transactions: list[ExportGrossTransactionItemModel] = Field(...)


class FinanceAccountModel(ExtendedBaseModel):
    account_number: str = Field(..., alias="accountNumber", min_length=1)
    name: str = Field(..., min_length=1)
    type: Type3 = Field(...)
    has_children: bool = Field(..., alias="hasChildren")
    parent_number: str | None = Field(None, alias="parentNumber")
    is_archived: bool = Field(..., alias="isArchived")
    transactions: list[AccountingTransactionModel] | None = Field(None)


class FolioDebitorModel(ExtendedBaseModel):
    type: Type5 | None = Field(None)
    title: Title | None = Field(None)
    first_name: str | None = Field(None, alias="firstName")
    name: str | None = Field(None)
    address: NonStrictAddressModel | None = None
    company: CompanyInfoModel | None = None
    personal_tax_id: str | None = Field(None, alias="personalTaxId")
    reference: str | None = Field(None, max_length=80)
    email: str | None = Field(None)
    phone: str | None = Field(None)


class FolioItemModel(ExtendedBaseModel):
    id: str = Field(...)
    created: AwareDatetime = Field(...)
    updated: AwareDatetime = Field(...)
    type: ReferenceType | None = Field(None)
    debitor: FolioDebitorModel | None = None
    closing_date: date_aliased | None = Field(None, alias="closingDate", examples=["2020-10-10"])
    is_main_folio: bool | None = Field(None, alias="isMainFolio")
    is_empty: bool | None = Field(None, alias="isEmpty")
    reservation: EmbeddedReservationModel | None = None
    booking_id: str | None = Field(None, alias="bookingId")
    company: EmbeddedCompanyModel | None = None
    balance: MonetaryValueModel
    checked_out_on_accounts_receivable: bool | None = Field(
        None, alias="checkedOutOnAccountsReceivable"
    )
    folio_warnings: list[FolioWarning] | None = Field(None, alias="folioWarnings")
    allowed_actions: list[AllowedAction] | None = Field(None, alias="allowedActions")
    related_invoices: list[EmbeddedInvoiceModel] | None = Field(None, alias="relatedInvoices")
    status: Status = Field(...)
    charges: list[ChargeModel] | None = Field(None)
    allowances: list[AllowanceModel] | None = Field(None)
    transitory_charges: list[TransitoryChargeModel] | None = Field(None, alias="transitoryCharges")
    payments: list[PaymentModel] | None = Field(None)


class FolioListModel(ExtendedBaseModel):
    folios: list[FolioItemModel] = Field(...)
    count: int = Field(...)


class FolioModel(ExtendedBaseModel):
    id: str = Field(...)
    created: AwareDatetime = Field(...)
    updated: AwareDatetime = Field(...)
    type: ReferenceType | None = Field(None)
    debitor: FolioDebitorModel | None = None
    closing_date: date_aliased | None = Field(None, alias="closingDate", examples=["2020-10-10"])
    reservation: EmbeddedReservationModel | None = None
    booking_id: str | None = Field(None, alias="bookingId")
    company: EmbeddedCompanyModel | None = None
    property: EmbeddedPropertyModel
    charges: list[ChargeModel] | None = Field(None)
    transitory_charges: list[TransitoryChargeModel] | None = Field(None, alias="transitoryCharges")
    payments: list[PaymentModel] | None = Field(None)
    pending_payments: list[PendingPaymentModel] | None = Field(None, alias="pendingPayments")
    allowances: list[AllowanceModel] | None = Field(None)
    balance: MonetaryValueModel
    checked_out_on_accounts_receivable: bool | None = Field(
        None, alias="checkedOutOnAccountsReceivable"
    )
    is_main_folio: bool | None = Field(None, alias="isMainFolio")
    is_empty: bool | None = Field(None, alias="isEmpty")
    related_folios: list[EmbeddedFolioModel] | None = Field(None, alias="relatedFolios")
    related_invoices: list[EmbeddedInvoiceModel] | None = Field(None, alias="relatedInvoices")
    folio_warnings: list[FolioWarning] | None = Field(None, alias="folioWarnings")
    allowed_actions: list[AllowedAction] | None = Field(None, alias="allowedActions")
    allowed_payment: float | None = Field(None, alias="allowedPayment")
    maximum_allowance: float | None = Field(None, alias="maximumAllowance")
    status: Status = Field(...)


class IncludedLineItemModel(ExtendedBaseModel):
    description: str | None = Field(None)
    price: MonetaryValueModel
    vat_type: VatType | None = Field(None, alias="vatType")
    vat_percent: float | None = Field(None, alias="vatPercent")


class InvoiceItemModel(ExtendedBaseModel):
    id: str = Field(...)
    number: str = Field(..., min_length=1)
    type: Type9 = Field(...)
    series: str | None = Field(None)
    language_code: str = Field(..., alias="languageCode")
    folio_id: str = Field(..., alias="folioId")
    reservation_id: str | None = Field(None, alias="reservationId")
    booking_id: str | None = Field(None, alias="bookingId")
    property_id: str = Field(..., alias="propertyId")
    related_invoice_number: str | None = Field(None, alias="relatedInvoiceNumber")
    write_off_reason: str | None = Field(None, alias="writeOffReason")
    cancellation_reason_code: ReasonCode | None = Field(None, alias="cancellationReasonCode")
    sub_total: MonetaryValueModel = Field(..., alias="subTotal")
    outstanding_payment: MonetaryValueModel | None = Field(None, alias="outstandingPayment")
    payment_settled: bool = Field(..., alias="paymentSettled")
    status: Status3 = Field(...)
    created: AwareDatetime = Field(...)
    guest_name: str | None = Field(None, alias="guestName")
    guest_company: str | None = Field(None, alias="guestCompany")
    allowed_actions: list[AllowedAction2] | None = Field(None, alias="allowedActions")
    company: EmbeddedCompanyModel | None = None


class InvoiceLineItemModel(ExtendedBaseModel):
    date: date_aliased = Field(..., examples=["2020-10-10"])
    description: str = Field(..., min_length=1)
    price: MonetaryValueModel
    vat_type: VatType | None = Field(None, alias="vatType")
    vat_percent: float | None = Field(None, alias="vatPercent")
    is_no_show_fee: bool = Field(..., alias="isNoShowFee")
    included_line_items: list[IncludedLineItemModel] | None = Field(None, alias="includedLineItems")
    guest: str | None = Field(None)
    quantity: int | None = Field(None)


class InvoiceLineItemsModel(ExtendedBaseModel):
    line_items: list[InvoiceLineItemModel] | None = Field(None, alias="lineItems")
    sub_total: MonetaryValueModel = Field(..., alias="subTotal")


class InvoiceListModel(ExtendedBaseModel):
    invoices: list[InvoiceItemModel] = Field(...)
    count: int = Field(...)


class InvoicePaymentModel(ExtendedBaseModel):
    id: str = Field(...)
    method: Method2 = Field(...)
    method_name: str = Field(..., alias="methodName", min_length=1)
    amount: MonetaryValueModel
    payment_date: AwareDatetime | None = Field(None, alias="paymentDate")
    business_date: date_aliased | None = Field(None, alias="businessDate", examples=["2020-10-10"])


class InvoiceRecipientModel(ExtendedBaseModel):
    name: str | None = None
    address: NonStrictAddressModel | None = None
    company_name: str | None = Field(None, alias="companyName")
    company_tax_id: str | None = Field(None, alias="companyTaxId")
    reference: str | None = None
    personal_tax_id: str | None = Field(None, alias="personalTaxId")


class PreviewInvoiceModel(ExtendedBaseModel):
    to: InvoiceRecipientModel | None = None
    create_invoice_action: CreateInvoiceAction = Field(..., alias="createInvoiceAction")
    create_invoice_warning: CreateInvoiceWarningModel | None = Field(
        None, alias="createInvoiceWarning"
    )
    invoice_date: date_aliased = Field(..., alias="invoiceDate", examples=["2020-10-10"])
    folio_id: str = Field(..., alias="folioId")
    from_: InvoiceSenderModel = Field(..., alias="from")
    commercial_information: CommercialInfoModel = Field(..., alias="commercialInformation")
    bank_account: BankAccountModel | None = Field(None, alias="bankAccount")
    payment_terms: str | None = Field(None, alias="paymentTerms")
    line_items: InvoiceLineItemsModel = Field(..., alias="lineItems")
    payments: list[InvoicePaymentModel] | None = Field(None)
    outstanding_payment: MonetaryValueModel | None = Field(None, alias="outstandingPayment")
    tax_details: list[TaxDetailModel] | None = Field(None, alias="taxDetails")
    total: MonetaryValueModel
    stay_info: StayInfoModel | None = Field(None, alias="stayInfo")
    property_id: str = Field(..., alias="propertyId")
    property_country_code: str = Field(..., alias="propertyCountryCode", min_length=1)
    language_code: str = Field(..., alias="languageCode", min_length=1)
    company: EmbeddedCompanyModel | None = None


class RefundListModel(ExtendedBaseModel):
    refunds: list[RefundModel] = Field(...)
    count: int = Field(...)


class SlimFinanceAccountModel(ExtendedBaseModel):
    account_number: str = Field(..., alias="accountNumber", min_length=1)
    name: str = Field(..., min_length=1)
    type: Type3 = Field(...)
    parent_number: str | None = Field(None, alias="parentNumber")
    has_children: bool = Field(..., alias="hasChildren")
    is_archived: bool = Field(..., alias="isArchived")
    vat: VatItemModel | None = None
    sub_accounts: list["SlimFinanceAccountModel"] | None = Field(None, alias="subAccounts")


class ActionModelPaymentActionNotAllowedPaymentActionReason(ExtendedBaseModel):
    action: Action
    is_allowed: bool = Field(..., alias="isAllowed")
    reasons: list[ActionReasonModelNotAllowedPaymentActionReason] | None = None


class AccountingTransactionListModel(ExtendedBaseModel):
    transactions: list[AccountingTransactionModel] = Field(...)


class AccountingTransactionPairListModel(ExtendedBaseModel):
    account_transaction_pairs: list[AccountingTransactionPairModel] = Field(
        ..., alias="accountTransactionPairs"
    )


class AggregateTransactionListModel(ExtendedBaseModel):
    aggregations: list[AggregateTransactionItemModel] = Field(...)
    total: AggregatesTotalModel


class ChartOfAccountsModel(ExtendedBaseModel):
    global_accounts: list[SlimFinanceAccountModel] = Field(..., alias="globalAccounts")
    guest_accounts: list[SlimFinanceAccountModel] = Field(..., alias="guestAccounts")
    external_accounts: list[SlimFinanceAccountModel] = Field(..., alias="externalAccounts")
    booking_accounts: list[SlimFinanceAccountModel] = Field(..., alias="bookingAccounts")


class CreateFolioModel(ExtendedBaseModel):
    reservation_id: str | None = Field(None, alias="reservationId")
    company_id: str | None = Field(None, alias="companyId")
    debitor: FolioDebitorModel
    type: Type1 | None = Field(None)
    property_id: str | None = Field(None, alias="propertyId")
    code: str | None = Field(None)


class FinanceAccountListModel(ExtendedBaseModel):
    accounts: list[SlimFinanceAccountModel] = Field(...)
    count: int = Field(...)


class FolioPaymentModel(ExtendedBaseModel):
    id: str = Field(...)
    method: Method2 | None = Field(None)
    amount: MonetaryValueModel
    external_reference: ExternalReference | None = Field(None, alias="externalReference")
    receipt: str | None = Field(None)
    payment_date: AwareDatetime = Field(..., alias="paymentDate")
    moved_from: EmbeddedFolioModel | None = Field(None, alias="movedFrom")
    moved_to: EmbeddedFolioModel | None = Field(None, alias="movedTo")
    moved_reason: str | None = Field(None, alias="movedReason")
    source_payment_id: str | None = Field(None, alias="sourcePaymentId")
    status: Status2 = Field(...)
    failure_reason: str | None = Field(None, alias="failureReason")
    failure_code: FailureCode | None = Field(None, alias="failureCode")
    type: Type8 = Field(...)
    expires_at: AwareDatetime | None = Field(None, alias="expiresAt")
    description: str | None = Field(None)
    url: str | None = Field(None)
    actions: list[ActionModelPaymentActionNotAllowedPaymentActionReason] | None = Field(None)
    business_date: date_aliased = Field(..., alias="businessDate", examples=["2020-10-10"])


class InvoiceModel(ExtendedBaseModel):
    id: str = Field(...)
    number: str = Field(..., min_length=1)
    type: Type9 = Field(...)
    series: str | None = Field(None)
    to: InvoiceRecipientModel
    payment_settled: bool = Field(..., alias="paymentSettled")
    status: Status3 = Field(...)
    created: AwareDatetime = Field(...)
    related_invoice_number: str | None = Field(None, alias="relatedInvoiceNumber")
    write_off_reason: str | None = Field(None, alias="writeOffReason")
    cancellation_reason_code: ReasonCode | None = Field(None, alias="cancellationReasonCode")
    allowed_actions: list[AllowedAction2] | None = Field(None, alias="allowedActions")
    invoice_date: date_aliased = Field(..., alias="invoiceDate", examples=["2020-10-10"])
    folio_id: str = Field(..., alias="folioId")
    from_: InvoiceSenderModel = Field(..., alias="from")
    commercial_information: CommercialInfoModel = Field(..., alias="commercialInformation")
    bank_account: BankAccountModel | None = Field(None, alias="bankAccount")
    payment_terms: str | None = Field(None, alias="paymentTerms")
    line_items: InvoiceLineItemsModel = Field(..., alias="lineItems")
    payments: list[InvoicePaymentModel] | None = Field(None)
    outstanding_payment: MonetaryValueModel | None = Field(None, alias="outstandingPayment")
    tax_details: list[TaxDetailModel] | None = Field(None, alias="taxDetails")
    total: MonetaryValueModel
    stay_info: StayInfoModel | None = Field(None, alias="stayInfo")
    property_id: str = Field(..., alias="propertyId")
    property_country_code: str = Field(..., alias="propertyCountryCode", min_length=1)
    language_code: str = Field(..., alias="languageCode", min_length=1)
    company: EmbeddedCompanyModel | None = None


class PaymentListModel(ExtendedBaseModel):
    payments: list[FolioPaymentModel] = Field(...)
    count: int = Field(...)


SlimFinanceAccountModel.model_rebuild()
