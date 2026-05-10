"""
Pydantic schemas for Apaleo Inventory API endpoints.
Generated from Apaleo Inventory API Swagger documentation.

API doc: https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1
"""

from pydantic import AwareDatetime, Field

from apaleoapi.apaleo.common.schemas.base import (
    ExtendedBaseModel,
    ListBaseModel,
    ListStringBaseModel,
)
from apaleoapi.apaleo.core.v1.enums.inventory import (
    Action,
    Code,
    Condition,
    Status,
    UnitGroupExtendedType,
    UnitGroupType,
    UnitMaintenanceType,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.common import BankAccountModel


class ActionReasonModel(ExtendedBaseModel):
    code: Code
    message: str = Field(..., min_length=1)


class ActionModel(ExtendedBaseModel):
    action: Action
    is_allowed: bool = Field(..., alias="isAllowed")
    reasons: list[ActionReasonModel] | None = None


class AddressModel(ExtendedBaseModel):
    address_line1: str = Field(..., alias="addressLine1", min_length=1)
    address_line2: str | None = Field(None, alias="addressLine2")
    postal_code: str = Field(..., alias="postalCode", min_length=1)
    city: str = Field(..., min_length=1)
    region_code: str | None = Field(None, alias="regionCode")
    country_code: str = Field(..., alias="countryCode")


class CountryListModel(ListStringBaseModel):
    items: list[str] = Field(
        default_factory=list,
        alias="countryCodes",
    )


class PropertyCreatedModel(ExtendedBaseModel):
    id: str = Field(...)


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
    status: Status = Field(...)
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
    status: Status = Field(...)
    is_archived: bool = Field(..., alias="isArchived")
    actions: list[ActionModel] | None = Field(None)


###############################


class BulkUnitsCreatedModel(ExtendedBaseModel):
    ids: list[str] = Field(...)


class ConnectedUnitGroupModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    member_count: int = Field(..., alias="memberCount")
    max_persons: int | None = Field(None, alias="maxPersons")


class ConnectedUnitModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    unit_group_id: str = Field(..., alias="unitGroupId")
    condition: Condition = Field(...)
    max_persons: int = Field(..., alias="maxPersons")


class CreateAddressModel(ExtendedBaseModel):
    address_line1: str = Field(..., alias="addressLine1", min_length=1)
    address_line2: str | None = Field(None, alias="addressLine2")
    postal_code: str = Field(..., alias="postalCode", min_length=1)
    city: str = Field(..., min_length=1)
    region_code: str | None = Field(None, alias="regionCode", max_length=6, min_length=2)
    country_code: str = Field(..., alias="countryCode", max_length=2, min_length=2)


class CreateConnectedUnitGroupModel(ExtendedBaseModel):
    unit_group_id: str = Field(..., alias="unitGroupId")
    member_count: int = Field(..., alias="memberCount", ge=1, le=2147483647)


class CreateConnectedUnitModel(ExtendedBaseModel):
    unit_id: str = Field(..., alias="unitId")


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


class CreateUnitAttributeDefinitionModel(ExtendedBaseModel):
    name: str = Field(..., max_length=50, min_length=1)
    description: str | None = Field(None)


class CreateUnitAttributeModel(ExtendedBaseModel):
    id: str = Field(...)


class CreateUnitGroupModel(ExtendedBaseModel):
    code: str = Field(
        ...,
        max_length=10,
        min_length=3,
        pattern="^[a-zA-Z0-9_]*$",
    )
    property_id: str = Field(..., alias="propertyId")
    name: dict[str, str] = Field(...)
    description: dict[str, str] = Field(...)
    max_persons: int = Field(..., alias="maxPersons", ge=1, le=2147483647)
    rank: int | None = Field(None, ge=1, le=2147483647)
    type: UnitGroupType | None = Field(None)
    connected_unit_groups: list[CreateConnectedUnitGroupModel] | None = Field(
        None, alias="connectedUnitGroups"
    )


class CreateUnitModel(ExtendedBaseModel):
    property_id: str = Field(..., alias="propertyId")
    name: str = Field(..., min_length=1)
    description: dict[str, str] = Field(...)
    unit_group_id: str | None = Field(None, alias="unitGroupId")
    max_persons: int = Field(..., alias="maxPersons", ge=1, le=2147483647)
    condition: Condition | None = Field(None)
    attributes: list[CreateUnitAttributeModel] | None = Field(None)
    connected_units: list[CreateConnectedUnitModel] | None = Field(None, alias="connectedUnits")


class EmbeddedPropertyModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str | None = Field(None)
    name: str | None = Field(None)
    description: str | None = Field(None)


class EmbeddedUnitGroupModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str | None = Field(None)
    name: str | None = Field(None)
    description: str | None = Field(None)
    type: UnitGroupExtendedType | None = Field(None)


class EmbeddedUnitModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str | None = Field(None)
    description: str | None = Field(None)
    unit_group_id: str | None = Field(None, alias="unitGroupId")


class ReplaceConnectedUnitGroupModel(CreateConnectedUnitGroupModel):
    pass


class ReplaceUnitGroupModel(ExtendedBaseModel):
    name: dict[str, str] = Field(...)
    description: dict[str, str] = Field(...)
    max_persons: int | None = Field(None, alias="maxPersons")
    rank: int | None = Field(None, ge=1, le=2147483647)
    connected_unit_groups: list[ReplaceConnectedUnitGroupModel] | None = Field(
        None, alias="connectedUnitGroups"
    )


class UnitAttributeDefinitionCreatedModel(ExtendedBaseModel):
    id: str = Field(...)


class UnitAttributeDefinitionModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1)
    description: str | None = Field(None)


class UnitAttributeModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1)
    description: str | None = Field(None)


class UnitCreatedModel(ExtendedBaseModel):
    id: str = Field(...)


class UnitGroupCreatedModel(ExtendedBaseModel):
    id: str = Field(...)


class UnitGroupItemModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    member_count: int = Field(..., alias="memberCount")
    max_persons: int | None = Field(None, alias="maxPersons")
    rank: int | None = Field(None)
    type: UnitGroupExtendedType = Field(...)
    property: EmbeddedPropertyModel
    connected_unit_groups: list[ConnectedUnitGroupModel] | None = Field(
        None, alias="connectedUnitGroups"
    )


class UnitGroupListModel(ExtendedBaseModel):
    unit_groups: list[UnitGroupItemModel] = Field(..., alias="unitGroups")
    count: int = Field(...)


class UnitGroupModel(ExtendedBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    property: EmbeddedPropertyModel
    name: dict[str, str] = Field(...)
    member_count: int = Field(..., alias="memberCount")
    description: dict[str, str] = Field(...)
    max_persons: int = Field(..., alias="maxPersons")
    rank: int | None = Field(None)
    type: UnitGroupExtendedType = Field(...)
    connected_unit_groups: list[ConnectedUnitGroupModel] | None = Field(
        None, alias="connectedUnitGroups"
    )


class UnitItemMaintenanceModel(ExtendedBaseModel):
    id: str = Field(...)
    type: UnitMaintenanceType = Field(...)


class UnitItemStatusModel(ExtendedBaseModel):
    is_occupied: bool = Field(..., alias="isOccupied")
    condition: Condition
    maintenance: UnitItemMaintenanceModel | None = None


class UnitMaintenanceModel(ExtendedBaseModel):
    id: str = Field(...)
    from_: AwareDatetime = Field(..., alias="from")
    to: AwareDatetime = Field(...)
    type: UnitMaintenanceType = Field(...)
    description: str | None = Field(None)


class UnitStatusModel(ExtendedBaseModel):
    is_occupied: bool = Field(..., alias="isOccupied")
    condition: Condition
    maintenance: UnitMaintenanceModel | None = None


class ActionReasonModelNotAllowedPropertyActionReason(ExtendedBaseModel):
    code: Code
    message: str = Field(..., min_length=1)


class BulkCreateUnitsModel(ExtendedBaseModel):
    units: list[CreateUnitModel]


class UnitAttributeDefinitionListModel(ExtendedBaseModel):
    unit_attributes: list[UnitAttributeDefinitionModel] = Field(..., alias="unitAttributes")
    count: int = Field(...)


class UnitItemModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    property: EmbeddedPropertyModel
    unit_group: EmbeddedUnitGroupModel | None = Field(None, alias="unitGroup")
    connecting_unit: EmbeddedUnitModel | None = Field(None, alias="connectingUnit")
    status: UnitItemStatusModel
    max_persons: int = Field(..., alias="maxPersons")
    created: AwareDatetime = Field(...)
    attributes: list[UnitAttributeModel] | None = Field(None)
    connected_units: list[ConnectedUnitModel] | None = Field(None, alias="connectedUnits")


class UnitListModel(ExtendedBaseModel):
    units: list[UnitItemModel] = Field(...)
    count: int = Field(...)


class UnitModel(ExtendedBaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1)
    description: dict[str, str] = Field(...)
    property: EmbeddedPropertyModel
    unit_group: EmbeddedUnitGroupModel | None = Field(None, alias="unitGroup")
    connecting_unit: EmbeddedUnitModel | None = Field(None, alias="connectingUnit")
    status: UnitStatusModel
    max_persons: int = Field(..., alias="maxPersons")
    created: AwareDatetime = Field(...)
    attributes: list[UnitAttributeModel] | None = Field(None)
    connected_units: list[ConnectedUnitModel] | None = Field(None, alias="connectedUnits")
