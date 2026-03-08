try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum


class RoleAccessTo(StrEnum):
    ACCOUNT_ADMIN = "AccountAdmin"
    PROPERTY_ADMIN = "PropertyAdmin"
    ACCOUNTANT = "Accountant"
    REVENUE_MANAGER = "RevenueManager"
    RESERVATION_MANAGER = "ReservationManager"
    FRONT_DESK = "FrontDesk"
    FRONT_DESK_SENIOR = "FrontDeskSenior"
    HOUSEKEEPING = "Housekeeping"
    HOUSEKEEPING_MANAGER = "HousekeepingManager"
    AUDITOR = "Auditor"
    STAFF_MANAGER = "StaffManager"


class RoleInvitedTo(StrEnum):
    ACCOUNT_ADMIN = "AccountAdmin"
    PROPERTY_ADMIN = "PropertyAdmin"
    FINANCE_MANAGER = "FinanceManager"
    REVENUE_MANAGER = "RevenueManager"
    RESERVATION_OFFICE = "ReservationOffice"
    FRONT_OFFICE = "FrontOffice"
    HOUSEKEEPING = "Housekeeping"
    HOUSEKEEPING_MANAGER = "HousekeepingManager"
    AUDITOR = "Auditor"
    STAFF_MANAGER = "StaffManager"


class UserSortBy(StrEnum):
    FIRST_NAME_ASC = "firstname:asc"
    FIRST_NAME_DESC = "firstname:desc"
    LAST_NAME_ASC = "lastname:asc"
    LAST_NAME_DESC = "lastname:desc"
    EMAIL_ASC = "email:asc"
    EMAIL_DESC = "email:desc"
