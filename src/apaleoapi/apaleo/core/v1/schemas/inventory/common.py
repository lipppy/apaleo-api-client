from pydantic import Field

from apaleoapi.apaleo.common.schemas.base import ExtendedBaseModel


class BankAccountModel(ExtendedBaseModel):
    iban: str | None = Field(None)
    bic: str | None = Field(None)
    bank: str | None = Field(None)
