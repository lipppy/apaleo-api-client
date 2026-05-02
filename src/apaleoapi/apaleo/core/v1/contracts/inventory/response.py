from dataclasses import dataclass, field
from datetime import datetime

from apaleoapi.apaleo.core.v1.contracts.inventory.common import Address, BankAccount


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
class CountryList:
    items: list[str]
    count: int


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
