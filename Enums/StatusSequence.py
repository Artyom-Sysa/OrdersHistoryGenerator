from enum import Enum


class StatusSequence(Enum):
    FILLED = 'Filled'
    PARTIAL_FILLED = 'PartialFilled'
    REJECTED = 'Rejected'
