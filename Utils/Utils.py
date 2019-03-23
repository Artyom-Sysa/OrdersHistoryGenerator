from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams


class Utils:
    __LCGParamsValues = []

    @classmethod
    def get_list_of_enum_values(cls, enum):
        '''
        Generate list enum elements values

        :param enum: enum for extraction elements keys
        :return: list with enum elements values
        '''

        result = []

        for member_name in list(vars(enum)['_member_names_']):
            result.append(vars(enum)['_member_map_'][member_name].value)

        return result

    @classmethod
    def get_LCG_params_values(cls):
        '''
        Generate and save list with Linear Congruential Generators parameters names

        :return: list with Linear Congruential Generators parameters names
        '''

        if len(cls.__LCGParamsValues) == 0:
            cls.__LCGParamsValues = cls.get_list_of_enum_values(LCGParams)
        return cls.__LCGParamsValues

    @staticmethod
    def is_dictionary_contains_all_keys(dictionary, keys_list):
        '''
        Determines the equality of lists values and dict keys

        :param dictionary: dictionary that contains keys
        :param keys_list: list of comparable keys
        :return: boolean value of equality
        '''

        return sorted(keys_list) == sorted(list(dictionary.keys()))
