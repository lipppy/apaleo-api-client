from dataclasses import dataclass, field

from apaleoapi.apaleo.core.v1.contracts.inventory.common import Address, BankAccount


@dataclass
class CreateAddress(Address):
    pass


@dataclass
class CreateProperty:
    code: str
    name: dict[str, str]
    company_name: str
    commercial_register_entry: str
    tax_id: str
    location: CreateAddress
    time_zone: str
    default_check_in_time: str
    default_check_out_time: str
    currency_code: str

    property_template_id: str | None = None
    description: dict[str, str | None] | None = None
    managing_directors: str | None = None
    bank_account: BankAccount | None = None
    payment_terms: dict[str, str | None] = field(default_factory=dict)
