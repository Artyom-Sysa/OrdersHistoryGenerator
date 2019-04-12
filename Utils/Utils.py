from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
import numbers
import os
import datetime


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
        :return: boolean value of checking and number or value otherwise
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
                    return False, value

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

    @staticmethod
    def get_file_name(path):
        '''
        Return only file name without extension

        :param path: file path
        :return: name file only
        '''
        return os.path.basename(path).split('.')[0]

    @staticmethod
    def get_current_date_with_format():
        '''
        :return: current date with format
        '''
        return datetime.datetime.today().strftime('%d-%m-%Y %H-%M-%S-%f')

    @staticmethod
    def create_folder_if_not_exists(folder_path):
        '''
        Create folder by path if it not exists
        '''
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        except:
            pass

    @staticmethod
    def calculate_percent_from_value(value, percent):
        '''
        Calculate percent from value
        '''
        return percent * value / 100

    @staticmethod
    def is_int(value):
        '''
        Check if value is int by comparing value and value than cast to int

        :param value: value for checking
        :return: boolean value of checking
        '''
        return value == int(value)

    @staticmethod
    def calculate_sequence_interval_value(sequence_gen_value, compr):
        if sequence_gen_value < compr / 3:
            return 0
        elif sequence_gen_value > compr * 2 / 3:
            return 1
        else:
            return 2

    @staticmethod
    def remove_file_if_exists(path):
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            pass

    @staticmethod
    def get_abs_path_with_project_root_path(path):
        '''
        Get path of project root folder

        :return: path of project root folder
        '''
        print(path)
        print(os.path.join(os.path.dirname(os.path.dirname(__file__)), path))

        return os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

    @classmethod
    def get_db_report_date(cls):
        from Service.LoggerService.Implementation.DefaultPythonLoggingService import \
            DefaultPythonLoggingService as Logger
        from Config.Configurations import Configuration
        from Config.Configurations import ValuesNames as Values
        from Service.DbService.Implementation.MySqlService import MySqlService
        from Entities.StatisticsDataStorage import StatisticsDataStorage

        Logger.info(__file__, 'Getting statistic from db started')
        mysql_settings = Configuration().settings[Values.MYSQL_SECTION_NAME]

        mysql = MySqlService(user=mysql_settings[Values.MYSQL_USER],
                             password=mysql_settings[Values.MYSQL_PASSWORD],
                             host=mysql_settings[Values.MYSQL_HOST], port=mysql_settings[Values.MYSQL_PORT],
                             database=mysql_settings[Values.MYSQL_DB_NAME])
        try:
            mysql.open_connection()

            for (value, name) in mysql.execute(Values.MYSQL_GET_REPORT_QUERY, select=True):
                if name == '1':
                    name = 'Red zone orders avg amount'
                if name == '2':
                    name = 'Green zone orders avg amount'
                if name == '3':
                    name = 'Blue zone orders avg amount'

                StatisticsDataStorage.statistics[name] = value
            Logger.info(__file__, 'Database service configurated')

        except AttributeError as er:
            Logger.error(__file__, er.args)
            Logger.info(__file__, 'Sending records to MySQL aborted')
        Logger.info(__file__, 'Getting statistic from db finished')
