from enum import Enum


class StatusSequence(Enum):
    FILLED = 'FILLED'
    PARTIAL_FILLED = 'PARTIAL_FILLED'
    REJECTED = 'REJECTED'
