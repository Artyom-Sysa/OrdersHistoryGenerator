from Decorators.Decorators import singleton
import os
from Utils.Utils import Utils
from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams


@singleton
class Configuration:
    def __init__(self):
        self.settings = {
            ValuesNames.GENERAL_SECTION_NAME: {
                ValuesNames.ORDERS_AMOUNT: 2000,
                ValuesNames.ORDERS_IN_FIRST_BLUE_ZONE: 3,
                ValuesNames.RED_ZONE_ORDERS_PERCENT: 15,
                ValuesNames.GREEN_ZONE_ORDERS_PERCENT: 60,
                ValuesNames.BLUE_ZONE_ORDERS_PERCENT: 25,
                ValuesNames.CURRENCY_DEVIATION_PERCENT: 5,
                ValuesNames.ORDER_HISTORY_WRITE_FILE_PATH: os.path.join(Utils.get_project_root_path(), 'Resources',
                                                                        'Result.csv'),
                ValuesNames.CURRENCY_PAIRS_FILE_PATH: os.path.join(Utils.get_project_root_path(), 'Resources',
                                                                   'CurrencyPairs.txt'),
                ValuesNames.TAGS_FILE_PATH: os.path.join(Utils.get_project_root_path(), 'Resources', 'Tags.txt'),
                ValuesNames.DEFAULT_SETTING_FILE_PATH: os.path.join(Utils.get_project_root_path(), 'Resources',
                                                                    'settings.ini')
            },
            ValuesNames.LOGGER_SECTION_NAME: {
                ValuesNames.LOGGING_FOLDER_PATH: os.path.join(Utils.get_project_root_path(), 'Logs'),
                ValuesNames.LOGGER_FORMAT: '%(levelname)s	%(asctime)s.%(msecs)d   %(name)s : %(message)s',
                ValuesNames.LOGGER_DATE_FORMAT: '%d-%m-%Y %H:%M:%S',
                ValuesNames.LOGGER_LEVEL: 'DEBUG'
            },
            ValuesNames.ID_GENERATOR: {
                ValuesNames.MWC1616_X: 23,
                ValuesNames.MWC1616_Y: 2,
                ValuesNames.MWC1616_CARRY: 65535,
                ValuesNames.MWC1616_A: 18000,
                ValuesNames.MWC1616_B: 30903,
            },
            ValuesNames.CURRENCY_PAIR_GENERATOR: {
                LCGParams.SEED.value: 666,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 16,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.TAGS_GENERATOR_1: {
                LCGParams.SEED.value: 0,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 17,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.TAGS_GENERATOR_2: {
                LCGParams.SEED.value: 3,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 17,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.TAGS_GENERATOR_3: {
                LCGParams.SEED.value: 6,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 17,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.TAGS_GENERATOR_4: {
                LCGParams.SEED.value: 111,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 17,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.TAGS_GENERATOR_5: {
                LCGParams.SEED.value: 12,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 17,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.INIT_VOLUME_GENERATOR: {
                LCGParams.SEED.value: 666,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 5000,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.PARTIAL_FILLED_PERCENT_GENERATOR: {
                LCGParams.SEED.value: 123,
                LCGParams.MULTIPLIER.value: 84589,
                LCGParams.MODULUS.value: 98,
                LCGParams.INCREMENT.value: 45989
            },
            ValuesNames.STATUS_SEQUENCE_GENERATOR: {
                LCGParams.SEED.value: 123,
                LCGParams.MULTIPLIER.value: 106,
                LCGParams.MODULUS.value: 100,
                LCGParams.INCREMENT.value: 1283
            },
            ValuesNames.FIRST_STATUS_DATE_OFFSET_GENERATOR: {
                LCGParams.SEED.value: 32,
                LCGParams.MULTIPLIER.value: 106123,
                LCGParams.MODULUS.value: 100,
                LCGParams.INCREMENT.value: 1283
            },
            ValuesNames.SECOND_STATUS_DATE_OFFSET_GENERATOR: {
                LCGParams.SEED.value: 64,
                LCGParams.MULTIPLIER.value: 106123,
                LCGParams.MODULUS.value: 100,
                LCGParams.INCREMENT.value: 1283
            },
            ValuesNames.THIRD_STATUS_DATE_OFFSET_GENERATOR: {
                LCGParams.SEED.value: 128,
                LCGParams.MULTIPLIER.value: 106123,
                LCGParams.MODULUS.value: 100,
                LCGParams.INCREMENT.value: 1283
            },
            ValuesNames.BLUE_STATUSES_AMOUNT_GENERATOR: {
                LCGParams.SEED.value: 256,
                LCGParams.MULTIPLIER.value: 106123,
                LCGParams.MODULUS.value: 200,
                LCGParams.INCREMENT.value: 1283
            },
            ValuesNames.FIRST_STATUS_POSSIBLE_TIME_GENERATOR: {
                LCGParams.SEED.value: 512,
                LCGParams.MULTIPLIER.value: 106123,
                LCGParams.MODULUS.value: 86399999,
                LCGParams.INCREMENT.value: 1283
            },
            ValuesNames.SECOND_STATUS_POSSIBLE_TIME_GENERATOR: {
                LCGParams.SEED.value: 1024,
                LCGParams.MULTIPLIER.value: 106123,
                LCGParams.MODULUS.value: 86399999,
                LCGParams.INCREMENT.value: 1283
            },
            ValuesNames.THIRD_STATUS_POSSIBLE_TIME_GENERATOR: {
                LCGParams.SEED.value: 2048,
                LCGParams.MULTIPLIER.value: 106123,
                LCGParams.MODULUS.value: 86399999,
                LCGParams.INCREMENT.value: 1283
            }
        }

        self.settings[ValuesNames.INIT_PX_PERCENT_DEVIATION_GENERATOR] = {
            LCGParams.SEED.value: 1,
            LCGParams.MULTIPLIER.value: 84589,
            LCGParams.MODULUS.value: self.settings[ValuesNames.GENERAL_SECTION_NAME][
                                         ValuesNames.CURRENCY_DEVIATION_PERCENT] * 200,
            LCGParams.INCREMENT.value: 45989
        }
        self.settings[ValuesNames.FILL_PX_PERCENT_DEVIATION_GENERATOR] = {
            LCGParams.SEED.value: 523,
            LCGParams.MULTIPLIER.value: 84589,
            LCGParams.MODULUS.value: self.settings[ValuesNames.GENERAL_SECTION_NAME][
                                         ValuesNames.CURRENCY_DEVIATION_PERCENT] * 200,
            LCGParams.INCREMENT.value: 45989
        }


class ValuesNames:
    ORDERS_AMOUNT = 'orders_amount'
    ORDERS_IN_FIRST_BLUE_ZONE = 'orders_in_first_blue_zone'
    RED_ZONE_ORDERS_PERCENT = 'red_zone_orders_percent'
    GREEN_ZONE_ORDERS_PERCENT = 'green_zone_orders_percent'
    BLUE_ZONE_ORDERS_PERCENT = 'blue_zone_orders_percent'
    CURRENCY_DEVIATION_PERCENT = 'currency_deviation_percent'
    LOGGING_FOLDER_PATH = 'logging_folder_path'
    LOGGER_FORMAT = 'logger_format'
    LOGGER_DATE_FORMAT = 'logger_date_format'
    LOGGER_LEVEL = 'logger_level'
    ORDER_HISTORY_WRITE_FILE_PATH = 'order_history_write_file_path'
    CURRENCY_PAIRS_FILE_PATH = 'order_history_write_file_path'
    TAGS_FILE_PATH = 'tags_file_path'
    DEFAULT_SETTING_FILE_PATH = 'default_setting_file_path'

    GENERAL_SECTION_NAME = 'GENERAL'
    LOGGER_SECTION_NAME = 'LOGGER'

    MWC1616_X = "MVC1616_x_seed"
    MWC1616_Y = "MVC1616_y_seed"
    MWC1616_CARRY = "MVC1616_carry"
    MWC1616_A = "MVC1616_a"
    MWC1616_B = "MVC1616_b"
    MWC1616_SEED = "MVC1616_seed"

    ID_GEN_VALUE = "id_generator_values"

    TAG_GEN_VALUE_1 = "tag_generator_values_1"
    TAG_GEN_VALUE_2 = "tag_generator_values_2"
    TAG_GEN_VALUE_3 = "tag_generator_values_3"
    TAG_GEN_VALUE_4 = "tag_generator_values_4"
    TAG_GEN_VALUE_5 = "tag_generator_values_5"

    INIT_VOLUME_GEN_VALUE = "init_volume_generator_values"
    PARTIAL_FILLED_PERCENT_GEN_VALUE = "partial_filled_percent_generator_values"

    STATUS_SEQUENCE_NUMBER_GEN_VALUE = "status_sequence_number_generator_values"
    FIRST_STATUS_DATE_OFFSET_GEN_VALUE = "first_status_date_offset_generator_values"
    SECOND_STATUS_DATE_OFFSET_GEN_VALUE = "second_status_date_offset_generator_values"
    THIRD_STATUS_DATE_OFFSET_GEN_VALUE = "third_status_date_offset_generator_values"

    FIRST_STATUS_POSSIBLE_TIME_GEN_VALUE = "first_status_possible_time_generator_values"
    SECOND_STATUS_POSSIBLE_TIME_GEN_VALUE = "second_status_possible_time_generator_values"
    THIRD_STATUS_POSSIBLE_TIME_GEN_VALUE = "third_status_possible_time_generator_values"

    BLUE_ZONE_STATUSES_AMOUNT_GEN_VALUE = "blue_zone_statuses_amount_generator_values"

    CURRENCY_PAIR_AMOUNT_GEN_VALUE = "currency_pair_generator_values"
    INIT_PX_DEVIATION_GEN_VALUE = "init_px_deviation_generator_values"
    FILL_PX_DEVIATION_GEN_VALUE = "fill_px_deviation_generator_values"

    ID_GENERATOR = "ID_GENERATOR"
    CURRENCY_PAIR_GENERATOR = "CURRENCY_PAIR_GENERATOR"
    INIT_PX_PERCENT_DEVIATION_GENERATOR = "INIT_PX_PERCENT_DEVIATION_GENERATOR"
    FILL_PX_PERCENT_DEVIATION_GENERATOR = "FILL_PX_PERCENT_DEVIATION_GENERATOR"
    TAGS_GENERATOR_1 = "TAGS_GENERATOR_1"
    TAGS_GENERATOR_2 = "TAGS_GENERATOR_2"
    TAGS_GENERATOR_3 = "TAGS_GENERATOR_3"
    TAGS_GENERATOR_4 = "TAGS_GENERATOR_4"
    TAGS_GENERATOR_5 = "TAGS_GENERATOR_5"

    INIT_VOLUME_GENERATOR = "INIT_VOLUME_GENERATOR"

    PARTIAL_FILLED_PERCENT_GENERATOR = "PARTIAL_FILLED_PERCENT_GENERATOR"
    STATUS_SEQUENCE_GENERATOR = "STATUS_SEQUENCE_GENERATOR"
    FIRST_STATUS_DATE_OFFSET_GENERATOR = "FIRST_STATUS_DATE_OFFSET_GENERATOR"
    SECOND_STATUS_DATE_OFFSET_GENERATOR = "SECOND_STATUS_DATE_OFFSET_GENERATOR"
    THIRD_STATUS_DATE_OFFSET_GENERATOR = "THIRD_STATUS_DATE_OFFSET_GENERATOR"

    BLUE_STATUSES_AMOUNT_GENERATOR = "BLUE_STATUSES_AMOUNT_GENERATOR"

    FIRST_STATUS_POSSIBLE_TIME_GENERATOR = "FIRST_STATUS_POSSIBLE_TIME_GENERATOR"
    SECOND_STATUS_POSSIBLE_TIME_GENERATOR = "SECOND_STATUS_POSSIBLE_TIME_GENERATOR"
    THIRD_STATUS_POSSIBLE_TIME_GENERATOR = "THIRD_STATUS_POSSIBLE_TIME_GENERATOR"
