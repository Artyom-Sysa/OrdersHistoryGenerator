from enum import IntEnum


class Status(IntEnum):
    NEW = 1
    TO_PROVIDER = 2
    FILLED = 3
    PARTIAL_FILLED = 4
    REJECTED = 5
