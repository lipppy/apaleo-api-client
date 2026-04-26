"""
Pydantic schemas for Apaleo Inventory API endpoints.
Generated from Apaleo Inventory API Swagger documentation.

API doc: https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1
"""

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import AwareDatetime, Field

from apaleoapi.apaleo.common.schemas.base import ExtendedBaseModel, ListBaseModel
from apaleoapi.apaleo.core.v1.enums.inventory import Action, Code, PropertyStatus

# Property


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


class ActionReasonModel(ExtendedBaseModel):
    code: Code
    message: str = Field(..., min_length=1)


class ActionModel(ExtendedBaseModel):
    action: Action
    is_allowed: bool = Field(..., alias="isAllowed")
    reasons: list[ActionReasonModel] | None = None


class PropertyItemModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    property_template_id: str | None = Field(None, alias="propertyTemplateId")
    is_template: bool = Field(..., alias="isTemplate")
    name: str = Field(..., min_length=1)
    description: str | None = Field(None)
    company_name: str = Field(..., alias="companyName", min_length=1)
    managing_directors: str | None = Field(None, alias="managingDirectors")
    commercial_register_entry: str = Field(..., alias="commercialRegisterEntry", min_length=1)
    tax_id: str = Field(..., alias="taxId", min_length=1)
    location: AddressModel = Field(...)
    bank_account: BankAccountModel | None = Field(None, alias="bankAccount")
    payment_terms: dict[str, str | None] = Field(default_factory=dict, alias="paymentTerms")
    time_zone: str = Field(..., alias="timeZone", min_length=1)
    currency_code: str = Field(..., alias="currencyCode")
    created: AwareDatetime = Field(...)
    status: PropertyStatus = Field(...)
    is_archived: bool = Field(..., alias="isArchived")
    actions: list[ActionModel] | None = Field(None)


class PropertyListModel(ListBaseModel[PropertyItemModel]):
    items: list[PropertyItemModel] = Field(default_factory=list, alias="properties")


class PropertyModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    property_template_id: str | None = Field(None, alias="propertyTemplateId")
    is_template: bool = Field(..., alias="isTemplate")
    name: dict[str, str] = Field(...)
    description: dict[str, str | None] | None = Field(None)
    company_name: str = Field(..., alias="companyName", min_length=1)
    managing_directors: str | None = Field(None, alias="managingDirectors")
    commercial_register_entry: str = Field(..., alias="commercialRegisterEntry", min_length=1)
    tax_id: str = Field(..., alias="taxId", min_length=1)
    location: AddressModel
    bank_account: BankAccountModel | None = Field(None, alias="bankAccount")
    payment_terms: dict[str, str | None] = Field(default_factory=dict, alias="paymentTerms")
    time_zone: str = Field(..., alias="timeZone", min_length=1)
    currency_code: str = Field(..., alias="currencyCode")
    created: AwareDatetime = Field(...)
    status: PropertyStatus = Field(...)
    is_archived: bool = Field(..., alias="isArchived")
    actions: list[ActionModel] | None = Field(None)


# Types


class CountryListModel(ExtendedBaseModel):
    country_codes: list[str] = Field(
        default_factory=list,
        alias="countryCodes",
    )


# Default Factories


class PropertyListModelDefaultFactory(ModelFactory[PropertyListModel]):
    __model__ = PropertyListModel
    __use_defaults__ = True
