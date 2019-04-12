import os

from Decorators.Decorators import singleton
from Enums.ExchangeType import ExchangeType
from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams


@singleton
class Configuration:
    def __init__(self):
        '''
        self.setting - dictionary which filled with default values
        After loading configurations, they will be filled in this dictionary
        '''
        self.settings = {
            ValuesNames.GENERAL_SECTION_NAME: {
                ValuesNames.ORDERS_AMOUNT: 2000,
                ValuesNames.ORDERS_IN_FIRST_BLUE_ZONE: 3,
                ValuesNames.RED_ZONE_ORDERS_PERCENT: 15,
                ValuesNames.GREEN_ZONE_ORDERS_PERCENT: 60,
                ValuesNames.BLUE_ZONE_ORDERS_PERCENT: 25,
                ValuesNames.BATCH_SIZE: 100,
                ValuesNames.CURRENCY_DEVIATION_PERCENT: 5,
                ValuesNames.ORDER_HISTORY_WRITE_FILE_PATH: os.path.join('.', 'Resources', 'Result.csv'),
                ValuesNames.CURRENCY_PAIRS_FILE_PATH: os.path.join('.', 'Resources', 'CurrencyPairs.txt'),
                ValuesNames.TAGS_FILE_PATH: os.path.join('.', 'Resources', 'Tags.txt'),
                ValuesNames.DEFAULT_SETTING_FILE_PATH: os.path.join('.', 'Resources', 'settings.ini')
            },
            ValuesNames.LOGGER_SECTION_NAME: {
                ValuesNames.LOGGING_CONF_FILE_PATH: os.path.join('.', 'Resources', 'logging.conf'),
            },
            ValuesNames.MYSQL_SECTION_NAME: {
                ValuesNames.MYSQL_HOST: '127.0.0.1',
                ValuesNames.MYSQL_PORT: '3306',
                ValuesNames.MYSQL_USER: 'root',
                ValuesNames.MYSQL_PASSWORD: '',
                ValuesNames.MYSQL_DB_NAME: 'orders_history'
            },
            ValuesNames.RMQ_SECTION_NAME: {
                ValuesNames.RMQ_HOST: '127.0.0.1',
                ValuesNames.RMQ_PORT: 5672,
                ValuesNames.RMQ_VIRTUAL_HOST: '/',
                ValuesNames.RMQ_USER: 'guest',
                ValuesNames.RMQ_PASSWORD: 'guest',
                ValuesNames.RMQ_EXCHANGE_NAME: 'orders_records',
                ValuesNames.RMQ_EXCHANGE_TYPE: ExchangeType.TOPIC.value,
                ValuesNames.RMQ_EXCHANGE_RED_RECORDS_ROUTING_KEY: 'r.order.red-zone.order-history-generator',
                ValuesNames.RMQ_EXCHANGE_BLUE_RECORDS_ROUTING_KEY: 'r.order.blue-zone.order-history-generator',
                ValuesNames.RMQ_EXCHANGE_GREEN_RECORDS_ROUTING_KEY: 'r.order.green-zone.order-history-generator',
            },
            ValuesNames.PERIODS_SIZE_GENERATOR: {
                LCGParams.SEED.value: 5,
                LCGParams.MULTIPLIER.value: 3,
                LCGParams.MODULUS.value: 10,
                LCGParams.INCREMENT.value: 8
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
                LCGParams.MODULUS.value: 500000000000,
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

        self.currency_pairs = []
        self.tags = []
        self.min_orders_volumes = None
        self.orders_volumes_for_generation = []
        self.not_used_orders_amount = 0
        self.is_current_date_in_trading_period = False
        self.start_date = None
        self.avg_value_of_ids = 0


class ValuesNames:
    ORDERS_AMOUNT = 'orders_amount'
    ORDERS_IN_FIRST_BLUE_ZONE = 'orders_in_first_blue_zone'
    RED_ZONE_ORDERS_PERCENT = 'red_zone_orders_percent'
    GREEN_ZONE_ORDERS_PERCENT = 'green_zone_orders_percent'
    BLUE_ZONE_ORDERS_PERCENT = 'blue_zone_orders_percent'
    CURRENCY_DEVIATION_PERCENT = 'currency_deviation_percent'
    LOGGING_FOLDER_PATH = 'logging_folder_path'
    LOGGING_CONF_FILE_PATH = 'logging_configurations_file_path'
    LOGGER_FORMAT = 'logger_format'
    LOGGER_DATE_FORMAT = 'logger_date_format'
    LOGGER_LEVEL = 'logger_level'
    ORDER_HISTORY_WRITE_FILE_PATH = 'order_history_write_file_path'
    CURRENCY_PAIRS_FILE_PATH = 'currency_pairs_file_path'
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

    PERIODS_SIZE_GENERATOR = "PERIODS_SIZE_GENERATOR"

    CURRENCY_PAIR_NAME = "currency pair name"
    CURRENCY_PAIR_VALUE = "currency pair value"

    ID = 'id'
    DIRECTION = "direction"
    INIT_PX = "init px"
    INIT_VOLUME = "init volume"
    FILL_PX = "fill px"
    FILL_VOLUME = "fill volume"
    TAGS = "tags"
    DESCRIPTIONS = "decriptions"

    TOTAL_ORDERS_VOLUME = 'ORDER_TOTAL_VOLUME'
    RED_ZONE_VOLUME = 'RED_ZONE_VOLUME'
    BLUE_ZONE_VOLUME = 'BLUE_ZONE_VOLUME'
    GREEN_ZONE_VOLUME = 'GREEN_ZONE_VOLUME'

    BATCH_SIZE = 'batch_size'

    RMQ_SECTION_NAME = 'RABBITMQ'

    RMQ_HOST = 'rabbitmq_host'
    RMQ_PORT = 'rabbitmq_port'
    RMQ_VIRTUAL_HOST = 'rabbitmq_virtual_host'
    RMQ_USER = 'rabbitmq_user'
    RMQ_PASSWORD = 'rabbitmq_password'
    RMQ_EXCHANGE_NAME = 'rabbitmq_exchange_name'
    RMQ_EXCHANGE_TYPE = 'rabbitmq_exchange_type'
    RMQ_EXCHANGE_RED_RECORDS_ROUTING_KEY = 'rabbitmq_red_records_routing_key'
    RMQ_EXCHANGE_BLUE_RECORDS_ROUTING_KEY = 'rabbitmq_blue_records_routing_key'
    RMQ_EXCHANGE_GREEN_RECORDS_ROUTING_KEY = 'rabbitmq_gree_records_routing_key'

    MYSQL_INSERT_QUERY = 'INSERT INTO `orders_history`.`history`(`order_id`, `direction_id`, `currency_pair`, `init_px`, `fill_px`, `init_vol`, `fill_vol`,`status_id`, `datetime`, `tags`, `description`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

    MYSQL_GET_REPORT_QUERY = """
        SELECT 
            (
                COUNT(order_id) / 
                (
                    SELECT 
                        CEIL(ABS((MIN(`datetime`) - MAX(`datetime`)) DIV 86400000) / 7) 
                    FROM 
                        history
                )
            ) AS avg_value, 
            IF(
                (
                    SELECT 
                        COUNT(order_id) 
                    FROM 
                        history inner_h 
                    WHERE 
                        inner_h.order_id = h.order_id
                ) = 3, 2, 
                            IF(
                                (
                                    SELECT 
                                        COUNT(order_id) 
                                    FROM 
                                        history inner_h 
                                    WHERE 
                                        inner_h.order_id = h.order_id AND status_id = 1
                                ) = 1, 3, 1
                            )
            ) AS zone_id 
        FROM (
                SELECT
                    DISTINCT order_id 
                FROM 
                    history
            ) h 
        GROUP BY zone_id
        UNION
            SELECT 
                COUNT(DISTINCT order_id), 
                'Total orders in database' 
            FROM 
                history
        UNION
            SELECT 
                COUNT(*), 
                'Total records in database' 
            FROM 
            history
    """

    MYSQL_SECTION_NAME = 'MYSQL'
    MYSQL_HOST = 'mysql_host'
    MYSQL_PORT = 'mysql_port'
    MYSQL_USER = 'mysql_user'
    MYSQL_PASSWORD = 'mysql_password'
    MYSQL_DB_NAME = 'mysql_db_name'
