from enum import IntEnum


class StatusSequence(IntEnum):
    FILLED = 0
    PARTIAL_FILLED = 1
    REJECTED = 2
