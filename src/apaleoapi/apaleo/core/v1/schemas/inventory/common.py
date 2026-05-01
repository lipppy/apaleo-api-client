from pydantic import Field

from apaleoapi.apaleo.common.schemas.base import ExtendedBaseModel


class AddressModel(ExtendedBaseModel):
    address_line1: str = Field(..., alias="addressLine1", min_length=1)
    address_line2: str | None = Field(None, alias="addressLine2")
    postal_code: str = Field(..., alias="postalCode", min_length=1)
    city: str = Field(..., min_length=1)
    region_code: str | None = Field(None, alias="regionCode")
    country_code: str = Field(..., alias="countryCode")


class BankAccountModel(ExtendedBaseModel):
    iban: str | None = None
    bic: str | None = None
    bank: str | None = None
