# Constants for department names or codes
from enum import Enum

class DepartmentType(str, Enum):
    WATER = "WATER"
    ELECTRICITY = "ELECTRICITY"
    ROADS = "ROADS"
    SANITATION = "SANITATION"
    HEALTH = "HEALTH"
    OTHER = "OTHER"
