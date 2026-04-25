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


class UserModelDefaultFactory(ModelFactory[UserModel]):
    __model__ = UserModel
    __use_defaults__ = True


class UsersListModelDefaultFactory(ModelFactory[UsersListModel]):
    __model__ = UsersListModel
    __use_defaults__ = True


class InvitationListModelDefaultFactory(ModelFactory[InvitationListModel]):
    __model__ = InvitationListModel
    __use_defaults__ = True


class InvitedUserToAccountResponseModelDefaultFactory(
    ModelFactory[InvitedUserToAccountResponseModel]
):
    __model__ = InvitedUserToAccountResponseModel
    __use_defaults__ = True
