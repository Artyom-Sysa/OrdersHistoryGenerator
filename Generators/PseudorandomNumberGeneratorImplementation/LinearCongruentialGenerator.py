from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
from Generators.PseudorandomNumberGenerator import PseudorandomNumberGenerator
from Utils.Utils import Utils


class LinearCongruentialGenerator(PseudorandomNumberGenerator):
    __generators = dict()

    @classmethod
    def get_next(cls, lcg_name):
        '''
        Generate next value of passed LCG with passed name

        :param lcg_name: name of linear congruential generator
        :return: generated lcg value if lcg_name exists in generators parameters dictionary or None otherwise
        '''

        if lcg_name in cls.__generators:
            generator = cls.__generators[lcg_name]

            multiplier = generator[LCGParams.MULTIPLIER.value]
            seed = generator[LCGParams.SEED.value]
            increment = generator[LCGParams.INCREMENT.value]
            modulus = generator[LCGParams.MODULUS.value]

            cls.__generators[lcg_name][LCGParams.SEED.value] = (multiplier * seed + increment) % modulus

            return cls.__generators[lcg_name][LCGParams.SEED.value]
        return None

    @classmethod
    def set_seed(cls, linear_congruential_generator_name, **kwargs):
        pass

    @classmethod
    def set_linear_congruential_generator(cls, generator_name, generator_values_dict):
        '''
        Set passed lcg dictionary with generator parameters

        :param generator_name: name of linear congruential generator
        :param generator_values_dict: dictionary which LC generator params: seed, multiplier, increment, modulus
        :return: boolean value of success set lcg params
        '''

        if Utils.is_dictionary_contains_all_keys(generator_values_dict, Utils.get_LCG_params_values()):
            cls.__generators[generator_name] = generator_values_dict
            return True
        return False
