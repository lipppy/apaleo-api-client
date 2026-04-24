from dataclasses import dataclass, field
from datetime import datetime

from polyfactory.factories import DataclassFactory


@dataclass
class Address:
    address_line1: str
    postal_code: str
    city: str
    country_code: str

    address_line2: str | None = None
    region_code: str | None = None


@dataclass
class BankAccount:
    iban: str | None = None
    bic: str | None = None
    bank: str | None = None


@dataclass
class ActionReason:
    code: str
    message: str


@dataclass
class Action:
    action: str
    is_allowed: bool
    reasons: list[ActionReason] | None = None


@dataclass
class PropertyItem:
    id: str
    code: str
    name: str
    company_name: str
    commercial_register_entry: str
    tax_id: str
    location: Address
    time_zone: str
    currency_code: str
    created: datetime
    status: str
    is_archived: bool

    property_template_id: str | None = None
    is_template: bool = False
    description: str | None = None
    managing_directors: str | None = None
    bank_account: BankAccount | None = None
    payment_terms: dict[str, str | None] = field(default_factory=dict)
    actions: list[Action] | None = None


@dataclass
class PropertyList:
    items: list[PropertyItem]
    count: int


@dataclass
class Property:
    id: str
    code: str
    name: dict[str, str]
    company_name: str
    commercial_register_entry: str
    tax_id: str
    location: Address
    time_zone: str
    currency_code: str
    created: datetime
    status: str
    is_archived: bool

    property_template_id: str | None = None
    is_template: bool = False
    description: dict[str, str | None] | None = None
    managing_directors: str | None = None
    bank_account: BankAccount | None = None
    payment_terms: dict[str, str | None] = field(default_factory=dict)
    actions: list[Action] | None = None


@dataclass
class CountryList:
    country_codes: list[str]


# Faker Factories


class PropertyListFakerFactory(DataclassFactory[PropertyList]):
    __model__ = PropertyList


class PropertyFactory(DataclassFactory[Property]):
    __model__ = Property
