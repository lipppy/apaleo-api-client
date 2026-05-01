from dataclasses import dataclass


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
