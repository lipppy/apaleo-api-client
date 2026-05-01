from pydantic import Field

from apaleoapi.apaleo.common.schemas.base import ExtendedBaseModel
from apaleoapi.apaleo.core.v1.schemas.inventory.common import AddressModel, BankAccountModel


class CreateAddressModel(AddressModel):
    address_line1: str = Field(..., alias="addressLine1", min_length=1)
    address_line2: str | None = Field(None, alias="addressLine2")
    postal_code: str = Field(..., alias="postalCode", min_length=1)
    city: str = Field(..., min_length=1)
    region_code: str | None = Field(None, alias="regionCode", max_length=6, min_length=2)
    country_code: str = Field(..., alias="countryCode", max_length=2, min_length=2)


class CreatePropertyModel(ExtendedBaseModel):
    code: str = Field(..., max_length=10, min_length=3, pattern="^[a-zA-Z0-9_]*$")
    name: dict[str, str] = Field(...)
    company_name: str = Field(..., alias="companyName", min_length=1)
    managing_directors: str | None = Field(None, alias="managingDirectors")
    commercial_register_entry: str = Field(..., alias="commercialRegisterEntry", min_length=1)
    tax_id: str = Field(..., alias="taxId", min_length=1)
    description: dict[str, str] | None = Field(None)
    location: CreateAddressModel
    bank_account: BankAccountModel | None = Field(None, alias="bankAccount")
    payment_terms: dict[str, str] = Field(..., alias="paymentTerms")
    time_zone: str = Field(..., alias="timeZone", min_length=1)
    default_check_in_time: str = Field(..., alias="defaultCheckInTime")
    default_check_out_time: str = Field(..., alias="defaultCheckOutTime")
    currency_code: str = Field(..., alias="currencyCode")
