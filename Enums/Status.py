from enum import Enum


class Status(Enum):
    NEW = 'New'
    TO_PROVIDER = 'ToProvider'
    FILLED = 'Filled'
    PARTIAL_FILLED = 'PartialFilled'
    REJECTED = 'Rejected'
