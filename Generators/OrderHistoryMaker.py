import datetime
import re

from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Entities.OrderHistory import OrderHistory
from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
from Generators.GeneralOrderInformationBuilder import GeneralOrderInformationBuilder
from Generators.OrderRecordsBuilder import OrderRecordsBuilder
from Generators.PseudorandomNumberGenerator.Implementation.IdGenerator import IdGenerator
from Generators.PseudorandomNumberGenerator.Implementation.LinearCongruentialGenerator import \
    LinearCongruentialGenerator as LCG
from Service.LoggerService.Implementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger
from Utils.Utils import Utils
from Enums.Zone import Zone
from Entities.StatisticsDataStorage import StatisticsDataStorage

from Service.FileService.Implementation.CsvFileService import CsvFileService
from Enums.Status import Status
from Service.MessageBrokerService.Implementation.RmqService import RmqService
from Enums.ExchangeType import ExchangeType
import Entities.Protobuf.OrderInformation_pb2 as OrderInformation
import Entities.Protobuf.Direction_pb2
import pprint
from Enums.Direction import Direction
import Entities.Protobuf.Direction_pb2
import Entities.Protobuf.Status_pb2
from Service.DbService.Implementation.MySqlService import MySqlService


class OrderHistoryMaker:
    def __init__(self):
        self.configs = Configuration()
        self.records_builder = OrderRecordsBuilder()
        self.order_builder = GeneralOrderInformationBuilder()
        self.history = OrderHistory()

        self.readed_green_records = None
        self.readed_red_records = None
        self.readed_blue_records = None

    def __count_volume_by_color(self, color):
        '''
        Calculate total zone orders volume
        :param color: zone color
        :return: total zone orders volume
        '''

        total_volume = 0
        for volume in self.configs.orders_volumes_for_generation:
            total_volume += volume[color]
        return total_volume

    def execute_generation(self):
        '''
        Execute generation orders history
        '''

        self.history.clear_history()

        Logger.info(__file__, 'Order history making started')

        self.__generate_green_orders()
        self.__generate_red_blue_orders()

    def __get_order_in_green_zone(self, id, status_sequence, period):
        '''
        Generate GeneralOrderHistory for green zone
        :param period: period index for generation
        :return: GeneralOrderHistory instance for green zone period
        '''

        return self.records_builder.build_order_records_in_green_zone(id, status_sequence, period)

    def __get_order_in_blue_red_zone(self, id, status_sequence, statuses_in_blue_zone_, period_start, period_end):
        '''
        Generate GeneralOrderHistory for blue-red zone
        :param period_start: index of start order period
        :param period_end: index of finish order period
        :return: GeneralOrderHistory instance for blue-red zone period
        '''

        return self.records_builder.build_order_records_in_blue_red_zone(id, status_sequence, statuses_in_blue_zone_,
                                                                         period_start, period_end)

    def __generate_general_order_information(self):
        '''
        Return GeneralOrderInformation instance with generators values
        :return: GeneralOrderInformation instance
        '''

        return self.order_builder. \
            set_id(IdGenerator.get_next()). \
            set_status_sequence(LCG.get_next(Values.STATUS_SEQUENCE_GENERATOR)). \
            set_currency_pair_by_value(LCG.get_next(Values.CURRENCY_PAIR_GENERATOR)). \
            set_currency_pair_init_value_by_deviation_percent(LCG.get_next(Values.INIT_PX_PERCENT_DEVIATION_GENERATOR)). \
            set_init_volume(LCG.get_next(Values.INIT_VOLUME_GENERATOR)). \
            set_currency_pair_fill_value_by_deviation_percent(LCG.get_next(Values.FILL_PX_PERCENT_DEVIATION_GENERATOR)). \
            set_fill_volume_deviation_percent(LCG.get_next(Values.PARTIAL_FILLED_PERCENT_GENERATOR)). \
            set_fill_volume(). \
            set_statuses_in_blue_zone_by_value(LCG.get_next(Values.BLUE_STATUSES_AMOUNT_GENERATOR)). \
            set_tags_with_description(LCG.get_next(Values.TAGS_GENERATOR_1),
                                      LCG.get_next(Values.TAGS_GENERATOR_2),
                                      LCG.get_next(Values.TAGS_GENERATOR_3),
                                      LCG.get_next(Values.TAGS_GENERATOR_4),
                                      LCG.get_next(Values.TAGS_GENERATOR_5)). \
            build()

    def __generate_green_orders(self):
        '''
        Generate green zone orders records with generators configurations
        '''

        Logger.info(__file__, 'Started generation order history in green zone')

        total_green_volume = int(self.__count_volume_by_color(Values.GREEN_ZONE_VOLUME)) - 1
        period = 1
        period_limit = self.configs.orders_volumes_for_generation[period][Values.GREEN_ZONE_VOLUME]
        period_counter = 0

        previous_time = datetime.datetime.now()

        for i in range(total_green_volume + 1):
            Logger.debug(__file__, f'Generation {i + 1} green order history started')

            if period_counter <= period_limit:
                period_counter += 1
            else:
                period_counter = 0
                period += 1
                period_limit = self.configs.orders_volumes_for_generation[period - 1][Values.GREEN_ZONE_VOLUME]

            order = self.__generate_general_order_information()
            self.history.orders[order.id] = order
            self.history.green_records.extend(self.__get_order_in_green_zone(order.id, order.status_sequence, period))

            if len(self.history.orders) % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] == 0:
                self.__add_time_statistic('Order history generation',
                                          (datetime.datetime.now() - previous_time).total_seconds() * 1000)
                previous_time = datetime.datetime.now()

            Logger.debug(__file__, f'Generation {i + 1} green order history finished')
        Logger.info(__file__, 'Generation green zone orders history finished')

    def __generate_red_blue_orders(self):
        '''
        Generate blue-red zone orders records with generators configurations
        '''

        Logger.info(__file__, 'Started generation order history in blue-red zone')

        period_start = -1
        period_finish = 0
        period_start_limit = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_IN_FIRST_BLUE_ZONE]
        period_start_counter = 1
        period_finish_limit = self.configs.orders_volumes_for_generation[period_finish][Values.RED_ZONE_VOLUME]
        period_finish_counter = 1
        finished_counter = 1
        finished_limit = self.__count_volume_by_color(Values.RED_ZONE_VOLUME)
        total_orders_amount = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]

        total_green_volume = int(self.__count_volume_by_color(Values.GREEN_ZONE_VOLUME)) - 1

        previous_time = datetime.datetime.now()

        for i in range(total_green_volume + 1, total_orders_amount):
            Logger.debug(__file__, f'Started generation {i - total_green_volume} order history in blue-red zone')

            order = self.__generate_general_order_information()
            self.history.orders[order.id] = order

            for record in self.__get_order_in_blue_red_zone(order.id,
                                                            order.status_sequence,
                                                            order.statuses_in_blue_zone,
                                                            period_start,
                                                            period_finish):
                if record.zone == Zone.RED:
                    self.history.red_records.append(record)
                if record.zone == Zone.BLUE:
                    self.history.blue_records.append(record)
                if record.zone == Zone.GREEN:
                    self.history.green_records.append(record)

            if len(self.history.orders) % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] == 0:
                self.__add_time_statistic('Order history generation',
                                          (datetime.datetime.now() - previous_time).total_seconds() * 1000)
                previous_time = datetime.datetime.now()

            Logger.debug(__file__, f'Generation {i - total_green_volume} order history in blue-red zone finished')

            if period_start_counter < period_start_limit:
                period_start_counter += 1
            else:
                period_start += 1
                period_start_limit = self.configs.orders_volumes_for_generation[period_start][Values.BLUE_ZONE_VOLUME] \
                    if period_start < len(self.configs.orders_volumes_for_generation) \
                    else self.configs.not_used_orders_amount

                if period_start == len(self.configs.orders_volumes_for_generation):
                    period_start = 0

                period_start_counter = 1

            if finished_counter < finished_limit:
                finished_counter += 1

                if period_finish_counter < period_finish_limit:
                    period_finish_counter += 1
                else:
                    period_finish += 1
                    period_finish_limit = self.configs.orders_volumes_for_generation[period_finish][
                        Values.RED_ZONE_VOLUME]
                    period_finish_counter = 1
            else:
                period_finish = -1

        Logger.info(__file__, 'Generation blue-red zone orders history finished')

        if len(self.history.orders) % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] != 0:
            self.__add_time_statistic('Order history generation',
                                      (datetime.datetime.now() - previous_time).total_seconds() * 1000)

    def __load_currency_pairs_from_file(self):
        '''
        Load currency pairs from file by path in config object
        '''

        Logger.info(__file__, 'Start loading currency pairs from file {}'.format(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH]))

        try:
            with open(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH], "r") as file:
                for line in file.readlines():
                    if re.fullmatch(r'[a-zA-Z]{3}\/[a-zA-Z]{3};[0-9]+([\.|\,][0-9]{0,5})', line.replace('\n', '')):
                        parts = line.split(";")
                        self.configs.currency_pairs.append({
                            Values.CURRENCY_PAIR_NAME: parts[0],
                            Values.CURRENCY_PAIR_VALUE: float(parts[1].replace("\n", '').replace(',', '.'))
                        })

                self.configs.settings[Values.CURRENCY_PAIR_GENERATOR][LCGParams.MODULUS.value] = len(
                    self.configs.currency_pairs)

            Logger.info(__file__, 'Loading currency pairs from file {} finished'.format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH]))

            Logger.debug(__file__, 'Loaded {} currency pairs: {}'.format(len(self.configs.currency_pairs),
                                                                         self.configs.currency_pairs))
        except:
            Logger.error(__file__, "Loading currency pairs from file {} failed".format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH]))

    def __load_tags_from_file(self):
        '''
        Load tags from file by path in config object
        '''

        Logger.info(__file__, 'Start loading tags from file {}'.format(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH]))

        try:
            with open(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH], "r") as file:
                for line in file.readlines():
                    if re.fullmatch('[a-zA-Z]{0,10}', line.replace('\n', '')):
                        self.configs.tags.append(line.replace("\n", ''))

            Logger.info(__file__, 'Loading tags from file {} finished'.format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH]))

            Logger.debug(__file__, 'Loaded {} tags: {}'.format(len(self.configs.tags), ', '.join(self.configs.tags)))

            self.configs.settings[Values.TAGS_GENERATOR_1][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_2][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_3][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_4][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_5][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
        except:
            Logger.error(__file__, "Loading tags from file {} failed".format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH]))

    def __calculate_orders_period_volumes(self):
        '''
        Calculate orders volumes list than equal to percentage of zones:
        red = 15%, green = 60% and blue = 25%
        '''

        red_zone_percent = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.RED_ZONE_ORDERS_PERCENT]
        green_zone_percent = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.GREEN_ZONE_ORDERS_PERCENT]
        blue_zone_percent = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BLUE_ZONE_ORDERS_PERCENT]

        Logger.info(__file__,
                    'Started calculating of orders volumes to period with zones percentes: red = {}, green ={}, blue ={}'.format(
                        red_zone_percent, green_zone_percent, blue_zone_percent
                    ))

        for i in range(1, self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT] + 1):
            first_percent = Utils.calculate_percent_from_value(i, red_zone_percent)
            second_percent = Utils.calculate_percent_from_value(i, green_zone_percent)
            third_percent = Utils.calculate_percent_from_value(i, blue_zone_percent)

            if Utils.is_int(first_percent) and Utils.is_int(second_percent) and Utils.is_int(third_percent):
                self.configs.orders_volumes.append({
                    Values.TOTAL_ORDERS_VOLUME: i,
                    Values.RED_ZONE_VOLUME: first_percent,
                    Values.GREEN_ZONE_VOLUME: second_percent,
                    Values.BLUE_ZONE_VOLUME: third_percent
                })

        Logger.info(__file__, 'Calculating of orders volumes to period with zones percentes finished')
        Logger.debug(__file__, 'Calculated orders volumes: {}'.format(self.configs.orders_volumes))

    def __calculate_orders_volumes_for_generations(self):
        '''
        Calculate orders volumes list for generation
        '''

        Logger.info(__file__, 'Starting calculating orders volumes for generating {} orders'.format(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]
        ))

        in_blue_zone = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_IN_FIRST_BLUE_ZONE]
        not_used = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT] - in_blue_zone

        found = True
        limit = len(self.configs.orders_volumes) - 1

        while found:
            i = limit
            found_volume = False

            while i >= 0 and not found_volume:
                volume = self.configs.orders_volumes[i]
                needed_orders = volume[Values.BLUE_ZONE_VOLUME] + volume[Values.GREEN_ZONE_VOLUME]

                if not_used > 0 and needed_orders <= not_used and volume[Values.RED_ZONE_VOLUME] <= in_blue_zone:
                    in_blue_zone = in_blue_zone - volume[Values.RED_ZONE_VOLUME] + volume[Values.BLUE_ZONE_VOLUME]

                    self.configs.orders_volumes_for_generation.append(volume)

                    not_used -= needed_orders
                    found_volume = True
                else:
                    i -= 1

            if i < 0 and not found_volume:
                found = False

        self.configs.not_used_orders_amount = not_used + in_blue_zone

        Logger.info(__file__, "Calculating orders volumes for each period finished")
        Logger.debug(__file__, 'Calculated {} orders volumes for generations: {}'.format(
            len(self.configs.orders_volumes_for_generation),
            self.configs.orders_volumes_for_generation))

    def __calculate_first_generation_period_start_date(self):
        '''
        Calculate start date of first generation perid
        '''

        Logger.info(__file__, 'Starting calculating start date of first period for generation orders')

        current_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        day_of_week = current_date.weekday() + 1

        self.configs.is_current_date_in_trading_period = day_of_week in (1, 2, 5)

        days_to_last_period = day_of_week + 7 - 5 if day_of_week < 5 else day_of_week - 5
        days_to_start_period = days_to_last_period + (7 * (len(self.configs.orders_volumes_for_generation)))
        self.configs.start_date = current_date + datetime.timedelta(days=-days_to_start_period)

        Logger.info(__file__,
                    'Calculating start date of first period for generation orders finished. Start at {}'.format(
                        self.configs.start_date))

    def prepare_configurations_for_generation(self):
        '''
        Call all function for prepare to generation ordera
        '''

        self.__load_currency_pairs_from_file()
        self.__load_tags_from_file()
        self.__calculate_orders_period_volumes()
        self.__calculate_orders_volumes_for_generations()
        self.__calculate_first_generation_period_start_date()
        self.__calculate_avg_values_of_id()
        self.__register_lcg_generators()

    def __calculate_avg_values_of_id(self):
        '''
        Calculate id's avg value. Need for calc order direction
        '''

        id_sum = 0
        amount = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]

        x = self.configs.settings[Values.ID_GENERATOR][Values.MWC1616_X]
        y = self.configs.settings[Values.ID_GENERATOR][Values.MWC1616_Y]

        for i in range(amount):
            id_sum += IdGenerator().get_next()

        IdGenerator.set_seed(x, y)

        self.configs.avg_value_of_ids = id_sum / amount

    def __register_lcg_generators(self):
        '''
        Register all generators setting to LCG generator
        '''

        for section in self.configs.settings:
            if 'GENERATOR' in section:
                LCG.set_linear_congruential_generator(section, self.configs.settings[section])

    def write_to_file(self):
        '''
        Writing orders records history to file
        '''

        path = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDER_HISTORY_WRITE_FILE_PATH]
        Utils.remove_file_if_exists(path)

        file_service = CsvFileService(path)

        self.__write_list(file_service, self.history.green_records, 'Green records writing to file')
        self.__write_list(file_service, self.history.red_records, 'Red records writing to file')
        self.__write_list(file_service, self.history.blue_records, 'Blue records writing to file')

        file_service.close()

    def clear_history(self):
        self.history.clear_history()

    def __write_list(self, file_service, list, name_stat):

        previous_time = datetime.datetime.now()
        counter = 0
        data = []

        for record in list:
            order = self.history.orders[record.order_id].to_list()

            data.append([
                order[Values.ID],
                order[Values.DIRECTION],
                order[Values.CURRENCY_PAIR_NAME],
                order[Values.INIT_PX],
                order[Values.INIT_VOLUME],
                order[Values.FILL_PX] if record.status in [Status.FILLED, Status.PARTIAL_FILLED] else 0,
                order[Values.FILL_VOLUME] if record.status in [Status.FILLED, Status.PARTIAL_FILLED] else 0,
                record.timestamp_millis,
                record.status.value,
                order[Values.TAGS],
                order[Values.DESCRIPTIONS],
                record.zone.value
            ])

            counter += 1
            if counter % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] == 0:
                file_service.write(data, 'a')
                self.__add_time_statistic(name_stat,
                                          (datetime.datetime.now() - previous_time).total_seconds() * 1000)
                data = []
                previous_time = datetime.datetime.now()

        if len(data) > 0:
            file_service.write(data, 'a')
            self.__add_time_statistic(name_stat,
                                      (datetime.datetime.now() - previous_time).total_seconds() * 1000)

    def read_from_file(self):
        file_service = CsvFileService(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDER_HISTORY_WRITE_FILE_PATH])

        start = datetime.datetime.now()

        for row in file_service.read():
            self.__add_row_to_list(row)

        self.__add_time_statistic('Read and sort records by zones',
                                  (datetime.datetime.now() - start).total_seconds() * 1000)

    @staticmethod
    def __add_time_statistic(name, value):
        if name not in StatisticsDataStorage.statistics:
            StatisticsDataStorage.statistics[name] = []
        StatisticsDataStorage.statistics[name].append(value)

    def __add_row_to_list(self, row):
        zone = row[11]
        if Zone.GREEN.value == zone:
            if self.readed_green_records is None:
                self.readed_green_records = []
            self.readed_green_records.append(row)
        if Zone.BLUE.value == zone:
            if self.readed_blue_records is None:
                self.readed_blue_records = []
            self.readed_blue_records.append(row)
        if Zone.RED.value == zone:
            if self.readed_red_records is None:
                self.readed_red_records = []
            self.readed_red_records.append(row)

    def send_readed_records_to_rmq(self):
        rmq_settings = self.configs.settings[Values.RMQ_SECTION_NAME]

        rmq = RmqService()
        rmq.open_connection(host=rmq_settings[Values.RMQ_HOST], port=rmq_settings[Values.RMQ_PORT],
                            virtual_host=rmq_settings[Values.RMQ_VIRTUAL_HOST], user=rmq_settings[Values.RMQ_USER],
                            password=rmq_settings[Values.RMQ_PASSWORD])

        rmq.exchange_delete(exchange_name=rmq_settings[Values.RMQ_EXCHANGE_NAME])

        rmq.declare_exchange(exchange_name=rmq_settings[Values.RMQ_EXCHANGE_NAME], exchange_type=ExchangeType.TOPIC)

        rmq.declare_queue(queue_name=Zone.RED.value)
        rmq.declare_queue(queue_name=Zone.BLUE.value)
        rmq.declare_queue(queue_name=Zone.GREEN.value)

        rmq.queue_bind(Zone.RED.value, rmq_settings[Values.RMQ_EXCHANGE_NAME],
                       rmq_settings[Values.RMQ_EXCHANGE_RED_RECORDS_ROUTING_KEY])
        rmq.queue_bind(Zone.BLUE.value, rmq_settings[Values.RMQ_EXCHANGE_NAME],
                       rmq_settings[Values.RMQ_EXCHANGE_BLUE_RECORDS_ROUTING_KEY])
        rmq.queue_bind(Zone.GREEN.value, rmq_settings[Values.RMQ_EXCHANGE_NAME],
                       rmq_settings[Values.RMQ_EXCHANGE_GREEN_RECORDS_ROUTING_KEY])

        self.__send_list_to_rmq(rmq, self.readed_red_records, rmq_settings[Values.RMQ_EXCHANGE_RED_RECORDS_ROUTING_KEY],
                                'Send RabbitMQ red zone records')
        self.__send_list_to_rmq(rmq, self.readed_blue_records,
                                rmq_settings[Values.RMQ_EXCHANGE_BLUE_RECORDS_ROUTING_KEY],
                                'Send RabbitMQ blue zone records')
        self.__send_list_to_rmq(rmq, self.readed_green_records,
                                rmq_settings[Values.RMQ_EXCHANGE_GREEN_RECORDS_ROUTING_KEY],
                                'Send RabbitMQ green zone records')

    def send_readed_records_to_mysql(self):
        mysql_settings = self.configs.settings[Values.MYSQL_SECTION_NAME]

        mysql = MySqlService(user=mysql_settings[Values.MYSQL_USER], password=mysql_settings[Values.MYSQL_PASSWORD],
                             host=mysql_settings[Values.MYSQL_HOST], port=mysql_settings[Values.MYSQL_PORT],
                             database=mysql_settings[Values.MYSQL_DB_NAME])

        self.__send_list_to_mysql(mysql, self.readed_red_records, 'Send red zones records to MySql')
        self.__send_list_to_mysql(mysql, self.readed_blue_records, 'Send blue zones records to MySql')
        self.__send_list_to_mysql(mysql, self.readed_green_records, 'Send green zones records to MySql')


    def __send_list_to_mysql(self, mysql, list, name_stat):
        previous_time = datetime.datetime.now()
        counter = 0

        data = []

        for record in list:
            data.append((record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7],
                         record[8], record[9], record[10], record[11]))

            counter += 1
            if counter % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] == 0:
                mysql.execute_multiple(Values.MYSQL_INSERT_QUERY, data)
                data.clear()
                self.__add_time_statistic(name_stat,
                                          (datetime.datetime.now() - previous_time).total_seconds() * 1000)
                previous_time = datetime.datetime.now()

        if counter % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] != 0:
            mysql.execute_multiple(Values.MYSQL_INSERT_QUERY, data)
            data.clear()
            self.__add_time_statistic(name_stat,
                                      (datetime.datetime.now() - previous_time).total_seconds() * 1000)

    def __order_record_to_proto(self, order):
        result = OrderInformation.OrderInformation()
        result.id = int(order[0])
        result.direction = Entities.Protobuf.Direction_pb2.BUY \
            if order[1] == Direction.BUY.value else Entities.Protobuf.Direction_pb2.SELL
        result.currency_pair_name = order[2]
        result.init_currency_pair_value = float(order[3])
        result.init_volume = int(order[4])
        result.fill_currency_pair_value = float(order[5])
        result.fill_volume = int(order[6])
        result.timestamp_millis = int(order[7])

        if order[8] == Status.NEW.value:
            result.status = Entities.Protobuf.Status_pb2.STATUS_NEW
        if order[8] == Status.TO_PROVIDER.value:
            result.status = Entities.Protobuf.Status_pb2.STATUS_TO_PROVIDER
        if order[8] == Status.PARTIAL_FILLED.value:
            result.status = Entities.Protobuf.Status_pb2.STATUS_PARTIAL_FILLED
        if order[8] == Status.REJECTED.value:
            result.status = Entities.Protobuf.Status_pb2.STATUS_REJECTED
        if order[8] == Status.FILLED.value:
            result.status = Entities.Protobuf.Status_pb2.STATUS_FILLED

        result.tags = order[9]
        result.description = order[10]

        return result

    def __send_list_to_rmq(self, rmq, list, key, name_stat):
        previous_time = datetime.datetime.now()
        counter = 0

        for record in list:
            rmq.publish(self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_NAME], key,
                        self.__order_record_to_proto(record).SerializeToString())
            counter += 1
            if counter % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] == 0:
                self.__add_time_statistic(name_stat,
                                          (datetime.datetime.now() - previous_time).total_seconds() * 1000)
                previous_time = datetime.datetime.now()

        if counter % self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE] != 0:
            self.__add_time_statistic(name_stat,
                                      (datetime.datetime.now() - previous_time).total_seconds() * 1000)
