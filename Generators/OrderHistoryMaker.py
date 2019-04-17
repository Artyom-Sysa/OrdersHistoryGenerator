import datetime
import pprint
import random
import re

import Entities.Protobuf.Direction_pb2
import Entities.Protobuf.Direction_pb2
import Entities.Protobuf.OrderInformation_pb2 as OrderInformation
import Entities.Protobuf.Status_pb2
import Entities.Protobuf.Zone_pb2
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Entities.OrderHistory import OrderHistory
from Entities.StatisticsDataStorage import StatisticsDataStorage
from Enums.Direction import Direction
from Enums.ExchangeType import ExchangeType
from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
from Enums.Status import Status
from Enums.Zone import Zone
from Generators.GeneralOrderInformationBuilder import GeneralOrderInformationBuilder
from Generators.OrderRecordsBuilder import OrderRecordsBuilder
from Generators.PseudorandomNumberGenerator.Implementation.IdGenerator import IdGenerator
from Generators.PseudorandomNumberGenerator.Implementation.LinearCongruentialGenerator import \
    LinearCongruentialGenerator as LCG
from Service.LoggerService.Implementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger
from Service.MessageBrokerService.Implementation.RmqService import RmqService
from Utils.Utils import Utils


class OrderHistoryMaker:
    def __init__(self, finish_event):
        self.configs = Configuration()
        self.records_builder = OrderRecordsBuilder()
        self.order_builder = GeneralOrderInformationBuilder()
        self.history = OrderHistory()
        self.fininsh_event = finish_event

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

        Logger.info(__file__, 'Generating order history started')

        self.__generate_orders()

        Logger.info(__file__, 'Generating order history finished')

        self.rmq.publish(
            self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_NAME],
            self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_GREEN_RECORDS_ROUTING_KEY],
            'stop')

        self.rmq.publish(
            self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_NAME],
            self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_RED_RECORDS_ROUTING_KEY],
            'stop')

        self.rmq.publish(
            self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_NAME],
            self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_BLUE_RECORDS_ROUTING_KEY],
            'stop')

        self.fininsh_event.set()

    def __get_order_in_zone(self, id, status_sequence, period, zone, statuses_in_unfinished_zone):
        '''
        Generate GeneralOrderHistory for green zone
        :param period: period index for generation
        :return: GeneralOrderHistory instance for green zone period
        '''

        return self.records_builder.build_order_zone(id, status_sequence, period, zone, statuses_in_unfinished_zone)

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

    def __generate_orders(self):
        '''
        Generate green zone orders records with generators configurations
        '''

        Logger.info(__file__, 'Started generation order history in green zone')

        previous_time = datetime.datetime.now()
        t = 0
        for period in range(len(self.configs.orders_volumes_for_generation)):
            zone_index = 0
            for zone in self.configs.orders_volumes_for_generation[period]:
                for i in range(int(self.configs.orders_volumes_for_generation[period][zone])):
                    order = self.__generate_general_order_information()

                    self.history.orders[order.id] = order
                    records = self.__get_order_in_zone(order.id, order.status_sequence, period, zone,
                                                       order.statuses_in_blue_zone)
                    self.history.records.extend(records)
                    self.inc_statistic('Generated orders', 1)
                    self.inc_statistic('Generated records', len(records))

                    if len(self.history.orders) % self.configs.settings[Values.GENERAL_SECTION_NAME][
                        Values.BATCH_SIZE] == 0:
                        self.add_time_statistic('Order history generation',
                                                (datetime.datetime.now() - previous_time).total_seconds() * 1000)
                        self.send_to_rmq()
                        previous_time = datetime.datetime.now()
                zone_index += 1

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

        if len(self.configs.currency_pairs) == 0:
            exit(-1)

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

        if len(self.configs.tags) == 0:
            exit(-2)

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
                self.configs.min_orders_volumes = {
                    Values.RED_ZONE_VOLUME: first_percent,
                    Values.GREEN_ZONE_VOLUME: second_percent,
                    Values.BLUE_ZONE_VOLUME: third_percent
                }
                break

        # Logger.info(__file__, 'Calculating of orders volumes to period with zones percentes finished')
        # Logger.debug(__file__, 'Calculated orders volumes: {}'.format(self.configs.orders_volumes))

    def __calculate_orders_volumes_for_generations(self):
        '''
        Calculate orders volumes list for generation
        '''

        Logger.info(__file__, 'Starting calculating orders volumes for generating {} orders'.format(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]
        ))

        min_percentage_amount = int(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT] /
            sum(self.configs.min_orders_volumes.values()))

        multiplier = LCG.get_next(Values.PERIODS_SIZE_GENERATOR)

        while min_percentage_amount > multiplier:
            self.configs.orders_volumes_for_generation.append({
                Zone.RED: self.configs.min_orders_volumes[Values.RED_ZONE_VOLUME] * multiplier,
                Zone.GREEN: self.configs.min_orders_volumes[Values.GREEN_ZONE_VOLUME] * multiplier,
                Zone.BLUE: self.configs.min_orders_volumes[Values.BLUE_ZONE_VOLUME] * multiplier
            })

            min_percentage_amount -= multiplier
            multiplier = LCG.get_next(Values.PERIODS_SIZE_GENERATOR)
        if min_percentage_amount > 0:
            self.configs.orders_volumes_for_generation.append({
                Zone.RED: self.configs.min_orders_volumes[Values.RED_ZONE_VOLUME] * min_percentage_amount,
                Zone.GREEN: self.configs.min_orders_volumes[Values.GREEN_ZONE_VOLUME] * min_percentage_amount,
                Zone.BLUE: self.configs.min_orders_volumes[Values.BLUE_ZONE_VOLUME] * min_percentage_amount
            })

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

        Logger.info(__file__, "Execute preparing to execution")

        self.__load_currency_pairs_from_file()
        self.__load_tags_from_file()
        self.__register_lcg_generators()

        self.__calculate_orders_period_volumes()
        self.__calculate_orders_volumes_for_generations()
        self.__calculate_first_generation_period_start_date()
        self.__calculate_avg_values_of_id()
        self.init_rmq()

        Logger.info(__file__, "Execute preparing finished")

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

        Logger.info(__file__, "Started registration linear congruential generators configs ")

        for section in self.configs.settings:
            if 'GENERATOR' in section:
                LCG.set_linear_congruential_generator(section, self.configs.settings[section])

        Logger.info(__file__, "Registration linear congruential generators configs finished")

    def clear_history(self):
        self.history.clear_history()

    @staticmethod
    def add_time_statistic(name, value):
        if name not in StatisticsDataStorage.statistics:
            StatisticsDataStorage.statistics[name] = []
        StatisticsDataStorage.statistics[name].append(value)

    def inc_statistic(self, name, value):
        if name not in StatisticsDataStorage.statistics:
            StatisticsDataStorage.statistics[name] = value
        else:
            StatisticsDataStorage.statistics[name] += value

    def __order_record_to_proto(self, record):
        result = OrderInformation.OrderInformation()

        order = self.history.orders[record.order_id]

        result.id = record.order_id
        result.direction = Entities.Protobuf.Direction_pb2.BUY \
            if order.direction == Direction.BUY else Entities.Protobuf.Direction_pb2.SELL
        result.currency_pair_name = order.currency_pair_name
        result.init_currency_pair_value = float(order.init_currency_pair_value)
        result.fill_currency_pair_value = float(order.fill_currency_pair_value)
        result.init_volume = order.init_volume
        result.fill_volume = order.fill_volume

        if record.status == Status.NEW:
            result.status = Entities.Protobuf.Status_pb2.STATUS_NEW
            result.fill_currency_pair_value = 0
            result.fill_volume = 0
        if record.status == Status.TO_PROVIDER:
            result.status = Entities.Protobuf.Status_pb2.STATUS_TO_PROVIDER
            result.fill_currency_pair_value = 0
            result.fill_volume = 0
        if record.status == Status.PARTIAL_FILLED:
            result.status = Entities.Protobuf.Status_pb2.STATUS_PARTIAL_FILLED
        if record.status == Status.REJECTED:
            result.status = Entities.Protobuf.Status_pb2.STATUS_REJECTED
            result.fill_currency_pair_value = 0
            result.fill_volume = 0
        if record.status == Status.FILLED:
            result.status = Entities.Protobuf.Status_pb2.STATUS_FILLED

        if record.zone == Zone.GREEN:
            result.zone = Entities.Protobuf.Zone_pb2.GREEN
        if record.zone == Zone.BLUE:
            result.zone = Entities.Protobuf.Zone_pb2.BLUE
        if record.zone == Zone.RED:
            result.zone = Entities.Protobuf.Zone_pb2.RED

        result.timestamp_millis = int(record.timestamp_millis)

        result.tags = order.tags
        result.description = order.description
        result.period = record.period

        return result

    def get_routing_key_by_zone(self, zone):
        if zone == Zone.BLUE:
            return self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_BLUE_RECORDS_ROUTING_KEY]
        if zone == Zone.RED:
            return self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_RED_RECORDS_ROUTING_KEY]
        if zone == Zone.GREEN:
            return self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_GREEN_RECORDS_ROUTING_KEY]

    def send_to_rmq(self):
        Logger.info(__file__, 'Sending ordres batch information to RabbitMQ')

        previous_time = datetime.datetime.now()

        for record in self.history.records:
            self.rmq.publish(self.configs.settings[Values.RMQ_SECTION_NAME][Values.RMQ_EXCHANGE_NAME],
                             self.get_routing_key_by_zone(record.zone),
                             self.__order_record_to_proto(record).SerializeToString())

        self.add_time_statistic('Sending records batch to RabbitMQ',
                                (datetime.datetime.now() - previous_time).total_seconds() * 1000)

        self.history.clear_history()

    def init_rmq(self):
        rmq_settings = self.configs.settings[Values.RMQ_SECTION_NAME]

        self.rmq = RmqService()

        while not self.rmq.open_connection(host=rmq_settings[Values.RMQ_HOST], port=rmq_settings[Values.RMQ_PORT],
                                           virtual_host=rmq_settings[Values.RMQ_VIRTUAL_HOST],
                                           user=rmq_settings[Values.RMQ_USER],
                                           password=rmq_settings[Values.RMQ_PASSWORD]):
            self.rmq.reconfig()

        self.rmq.exchange_delete(exchange_name=rmq_settings[Values.RMQ_EXCHANGE_NAME])

        try:
            self.rmq.declare_exchange(exchange_name=rmq_settings[Values.RMQ_EXCHANGE_NAME],
                                      exchange_type=ExchangeType(rmq_settings[Values.RMQ_EXCHANGE_TYPE]))
        except ValueError as er:
            Logger.error(__file__, er.args)
            Logger.info(__file__, 'Sending records to RabbitMQ aborted')
            return


        self.rmq.declare_queue(queue_name=Zone.RED.value, durable=bool(rmq_settings[Values.RMQ_DURABLE_QUEUES]))
        self.rmq.declare_queue(queue_name=Zone.BLUE.value, durable=bool(rmq_settings[Values.RMQ_DURABLE_QUEUES]))
        self.rmq.declare_queue(queue_name=Zone.GREEN.value, durable=bool(rmq_settings[Values.RMQ_DURABLE_QUEUES]))


        self.rmq.queue_bind(Zone.RED.value, rmq_settings[Values.RMQ_EXCHANGE_NAME],
                            rmq_settings[Values.RMQ_EXCHANGE_RED_RECORDS_ROUTING_KEY])
        self.rmq.queue_bind(Zone.BLUE.value, rmq_settings[Values.RMQ_EXCHANGE_NAME],
                            rmq_settings[Values.RMQ_EXCHANGE_BLUE_RECORDS_ROUTING_KEY])
        self.rmq.queue_bind(Zone.GREEN.value, rmq_settings[Values.RMQ_EXCHANGE_NAME],
                            rmq_settings[Values.RMQ_EXCHANGE_GREEN_RECORDS_ROUTING_KEY])

        self.rmq.queue_purge(queue_name=Zone.RED.value)
        self.rmq.queue_purge(queue_name=Zone.BLUE.value)
        self.rmq.queue_purge(queue_name=Zone.GREEN.value)
