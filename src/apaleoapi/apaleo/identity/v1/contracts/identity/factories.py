from polyfactory.factories import DataclassFactory

from apaleoapi.apaleo.identity.v1.contracts.identity.responses import (
    InvitationList,
    InvitedUserToAccountResponse,
    RoleList,
    User,
    UsersList,
)


class RoleListFakerFactory(DataclassFactory[RoleList]):
    __model__ = RoleList


class UserFakerFactory(DataclassFactory[User]):
    __model__ = User


class UsersListFakerFactory(DataclassFactory[UsersList]):
    __model__ = UsersList


class InvitationListFakerFactory(DataclassFactory[InvitationList]):
    __model__ = InvitationList


class InvitedUserToAccountResponseFakerFactory(DataclassFactory[InvitedUserToAccountResponse]):
    __model__ = InvitedUserToAccountResponse
