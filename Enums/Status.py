from enum import Enum


class Status(Enum):
    NEW = 'NEW'
    TO_PROVIDER = 'TO_PROVIDER'
    FILLED = 'FILLED'
    PARTIAL_FILLED = 'PARTIAL_FILLED'
    REJECTED = 'REJECTED'
