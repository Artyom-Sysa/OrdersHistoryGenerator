from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
import numbers
import os


class Utils:
    '''
    Linear Congruential Generators parameters(constants) names
    List would be filled by value after first call of function get_LCG_params_values,
    each next call this function data wouldn't rewrite values - it would get data from this list
    '''
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

    @classmethod
    def is_number(cls, value):
        '''
        Determines if value is number

        :param value: value for checking
        :return: boolean value of checking and number or None otherwise
        '''

        if isinstance(value, numbers.Number):
            return True, value
        else:
            try:
                int_cast = int(value, 0)
                return True, int_cast
            except:
                try:
                    float_cast = float(value)
                    return True, float_cast
                except:
                    return False, None

    @classmethod
    def is_dictionary_contains_all_number_values(cls, dictionary):
        '''
        Determines if all dictionary values is number and try convert it to number if it possible

        :param dictionary: dictionary to check
        :return: boolean value of checking
        '''

        for key in dictionary:
            is_number, value = cls.is_number(dictionary[key])

            if is_number:
                if value != dictionary[key]:
                    dictionary[key] = value
            else:
                return False
        return True

    @staticmethod
    def get_project_root_path():
        '''
        Get path of project root folder

        :return: path of project root folder
        '''

        return os.path.dirname(os.path.dirname(__file__))

    @staticmethod
    def is_file_exists(file_path):
        '''
        Check if file with path exists

        :param file_path: file path for checking
        :return: boolean value of existing file
        '''

        return os.path.exists(file_path)
