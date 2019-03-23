from enum import Enum


class LinearCongruentialGeneratorParameters(Enum):
    SEED = 'seed'
    MULTIPLIER = 'multiplier'
    MODULUS = 'modulus'
    INCREMENT = 'increment'
