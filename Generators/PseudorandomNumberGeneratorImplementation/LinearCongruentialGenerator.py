from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
from Generators.PseudorandomNumberGenerator import PseudorandomNumberGenerator
from Utils.Utils import Utils

'''
All linear congruential generators use this formula:    
    r(n+1) = a*r(n)+c (mod m)
Where:
    r(0) is a seed.
    r(1),r(2),r(3),... are the random numbers.
    a, c, m are constants.

If one chooses the values of a, c and m with care, then the generator
produces a uniform distribution of integers from 0 to m-1

LCG numbers have poor quality. r(n) and r(n+1) are not independent, as true random numbers would be. 
LCG is not cryptographically secure. 

Among the benefits of the LCG, one can easily reproduce a sequence of numbers, 
from the same r(0). One can also reproduce such sequence with a different programming language,
because the formula is so simple.

'''
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
    def set_seed(cls, linear_congruential_generator_name, seed=None, increment=None, modulus=None, multiplier=None):
        '''
        Set passed parameters to concrete LCG setting if that LCG generator exists in generators dictionary
        Set parameters to LCG setting if at least parameter is number

        :param linear_congruential_generator_name: LCG name
        :param seed: seed parameter
        :param increment: increment parameter
        :param modulus: modulus parameter
        :param multiplier: multiplier parameter
        :return: True if at least parameter is number, False otherwise
        '''
        if linear_congruential_generator_name in cls.__generators:
            seed_is_number, seed_value = Utils.is_number(seed)
            increment_is_number, increment_value = Utils.is_number(seed)
            modulus_is_number, modulus_value = Utils.is_number(seed)
            multiplier_is_number, multiplier_value = Utils.is_number(seed)

            if seed_is_number or increment_is_number or modulus_is_number or multiplier_is_number:
                if seed_is_number:
                    cls.__generators[linear_congruential_generator_name][LCGParams.SEED.value] = seed_value

                if increment_is_number:
                    cls.__generators[linear_congruential_generator_name][LCGParams.INCREMENT.value] = increment_value

                if modulus_is_number:
                    cls.__generators[linear_congruential_generator_name][LCGParams.MODULUS.value] = modulus_value

                if multiplier_is_number:
                    cls.__generators[linear_congruential_generator_name][
                        LCGParams.MULTIPLIER.value] = multiplier_is_number

                return True
        return False

    @classmethod
    def set_linear_congruential_generator(cls, generator_name, generator_values_dict):
        '''
        Set passed lcg dictionary with generator parameters

        :param generator_name: name of linear congruential generator
        :param generator_values_dict: dictionary which LC generator params: seed, multiplier, increment, modulus
        :return: boolean value of success set lcg params
        '''

        if Utils.is_dictionary_contains_all_keys(generator_values_dict, Utils.get_LCG_params_values()):
            if Utils.is_dictionary_contains_all_number_values(generator_values_dict):
                cls.__generators[generator_name] = generator_values_dict
                return True
        return False
