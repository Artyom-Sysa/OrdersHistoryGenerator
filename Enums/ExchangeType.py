import enum


class ExchangeType(enum.Enum):
    DIRECT = 'direct'
    TOPIC = 'topic'
    FANOUT = 'fanout'
