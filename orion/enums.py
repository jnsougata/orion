from enum import Enum


class DBScope(int, Enum):
    READONLY = 1
    READWRITE = 2
    SUPERUSER = 3


class UseAuthBool(str, Enum):
    TRUE = "true"
    FALSE = "false"
