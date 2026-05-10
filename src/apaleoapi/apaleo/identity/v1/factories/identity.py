from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory

from apaleoapi.apaleo.identity.v1.schemas.identity.response import (
    InvitationListModel,
    InvitedUserToAccountResponseModel,
    RoleListModel,
    UserModel,
    UsersListModel,
)


class RoleListModelDefaultFactory(ModelFactory[RoleListModel]):
    __model__ = RoleListModel
    __use_defaults__ = True


class RoleListModelFakerFactory(ModelFactory[RoleListModel]):
    __model__ = RoleListModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class UserModelDefaultFactory(ModelFactory[UserModel]):
    __model__ = UserModel
    __use_defaults__ = True


class UserModelFakerFactory(ModelFactory[UserModel]):
    __model__ = UserModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class UsersListModelDefaultFactory(ModelFactory[UsersListModel]):
    __model__ = UsersListModel
    __use_defaults__ = True


class UsersListModelFakerFactory(ModelFactory[UsersListModel]):
    __model__ = UsersListModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class InvitationListModelDefaultFactory(ModelFactory[InvitationListModel]):
    __model__ = InvitationListModel
    __use_defaults__ = True


class InvitationListModelFakerFactory(ModelFactory[InvitationListModel]):
    __model__ = InvitationListModel
    __faker__ = Faker(locale=["en_US", "de_DE"])


class InvitedUserToAccountResponseModelDefaultFactory(
    ModelFactory[InvitedUserToAccountResponseModel]
):
    __model__ = InvitedUserToAccountResponseModel
    __use_defaults__ = True


class InvitedUserToAccountResponseModelFakerFactory(
    ModelFactory[InvitedUserToAccountResponseModel]
):
    __model__ = InvitedUserToAccountResponseModel
    __faker__ = Faker(locale=["en_US", "de_DE"])
