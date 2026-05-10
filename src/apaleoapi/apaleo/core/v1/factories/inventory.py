from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory

from apaleoapi.apaleo.core.v1.schemas.inventory.response import (
    CountryListModel,
    CreateAddressModel,
    CreatePropertyModel,
    PropertyListModel,
    PropertyModel,
)
from apaleoapi.apaleo.identity.v1.schemas.identity.response import PropertyCreatedModel


class CountryListModelDefaultFactory(ModelFactory[CountryListModel]):
    __model__ = CountryListModel
    __use_defaults__ = True


class CountryListModelFakerFactory(ModelFactory[CountryListModel]):
    __model__ = CountryListModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class PropertyCreatedModelDefaultFactory(ModelFactory[PropertyCreatedModel]):
    __model__ = PropertyCreatedModel
    __use_defaults__ = True


class PropertyCreatedModelFakerFactory(ModelFactory[PropertyCreatedModel]):
    __model__ = PropertyCreatedModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class PropertyListModelDefaultFactory(ModelFactory[PropertyListModel]):
    __model__ = PropertyListModel
    __use_defaults__ = True


class PropertyListModelFakerFactory(ModelFactory[PropertyListModel]):
    __model__ = PropertyListModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class PropertyModelDefaultFactory(ModelFactory[PropertyModel]):
    __model__ = PropertyModel
    __use_defaults__ = True


class PropertyModelFakerFactory(ModelFactory[PropertyModel]):
    __model__ = PropertyModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class CreateAddressModelFakerFactory(ModelFactory[CreateAddressModel]):
    __model__ = CreateAddressModel
    __faker__ = Faker(locale=["en_US", "de_DE"])

    @classmethod
    def address_line1(cls) -> str:
        return cls.__faker__.street_address()

    @classmethod
    def postal_code(cls) -> str:
        return cls.__faker__.postcode()

    @classmethod
    def city(cls) -> str:
        return cls.__faker__.city()

    @classmethod
    def country_code(cls) -> str:
        return cls.__faker__.country_code()

    @classmethod
    def address_line2(cls) -> str | None:
        return (
            cls.__faker__.secondary_address()
            if cls.__faker__.boolean(chance_of_getting_true=50)
            else None
        )

    @classmethod
    def region_code(cls) -> str | None:
        return None  # Region code is optional and can be left as None for simplicity


class CreatePropertyModelFakerFactory(ModelFactory[CreatePropertyModel]):
    __model__ = CreatePropertyModel
    __faker__ = Faker(locale=["en_US", "de_DE"])

    @classmethod
    def build_custom(cls, country_code: str) -> CreatePropertyModel:
        return cls.build(location=CreateAddressModelFakerFactory.build(country_code=country_code))

    @classmethod
    def code(cls) -> str:
        return cls.__faker__.word().upper()

    @classmethod
    def name(cls) -> dict[str, str]:
        return {"en": cls.__faker__.company(), "de": cls.__faker__.company()}

    @classmethod
    def location(cls) -> CreateAddressModel:
        return CreateAddressModelFakerFactory.build()

    @classmethod
    def time_zone(cls) -> str:
        return cls.__faker__.timezone()

    @classmethod
    def default_check_in_time(cls) -> str:
        return "15:00:00"  # Fixed check-in time for consistency in tests

    @classmethod
    def default_check_out_time(cls) -> str:
        return "11:00:00"  # Fixed check-out time for consistency in tests

    @classmethod
    def currency_code(cls) -> str:
        return cls.__faker__.currency_code()

    @classmethod
    def description(cls) -> dict[str, str | None]:
        return {"en": cls.__faker__.sentence(), "de": cls.__faker__.sentence()}

    @classmethod
    def payment_terms(cls) -> dict[str, str | None]:
        return {"en": cls.__faker__.sentence(), "de": cls.__faker__.sentence()}
