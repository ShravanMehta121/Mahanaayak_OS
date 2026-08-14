from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    TEAM_MEMBER = "TEAM_MEMBER"
