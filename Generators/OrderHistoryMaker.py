from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Generators.OrderRecordsBuilder import OrderRecordsBuilder
from Generators.GeneralOrderInformationBuilder import GeneralOrderInformationBuilder
from Generators.PseudorandomNumberGeneratorImplementation.IdGenerator import IdGenerator
from Generators.PseudorandomNumberGeneratorImplementation.LinearCongruentialGenerator import \
    LinearCongruentialGenerator as LCG

from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger


class OrderHistoryMaker:
    def __init__(self):
        self.configs = Configuration()
        self.records_builder = OrderRecordsBuilder()
        self.order_builder = GeneralOrderInformationBuilder()

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

        Logger.info(__file__, 'Order history making started')

        self.__generate_green_orders()
        self.__generate_red_blue_orders()

        Logger.info(__file__, 'Order history making finished')

    def __get_record_by_order_in_green_zone(self, period):
        '''
        Generate GeneralOrderHistory for green zone
        :param period: period index for generation
        :return: GeneralOrderHistory instance for green zone period
        '''

        return self.records_builder.set_general_order_info(
            self.__generate_general_order_information()
        ).build_order_records_in_green_zone(period)

    def __get_record_by_order_in_blue_red_zone(self, period_start, period_end):
        '''
        Generate GeneralOrderHistory for blue-red zone
        :param period_start: index of start order period
        :param period_end: index of finish order period
        :return: GeneralOrderHistory instance for blue-red zone period
        '''

        return self.records_builder.set_general_order_info(
            self.__generate_general_order_information()
        ).build_order_records_in_blue_red_zone(period_start, period_end)

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

        for i in range(total_green_volume + 1):
            Logger.debug(__file__, f'Generation {i + 1} green order history started')

            if period_counter <= period_limit:
                period_counter += 1
            else:
                period_counter = 0
                period += 1
                period_limit = self.configs.orders_volumes_for_generation[period - 1][Values.GREEN_ZONE_VOLUME]

            for record in self.__get_record_by_order_in_green_zone(period):
                Logger.debug(__file__, 'Generated record for {} green order history: {}'.format(i + 1, record))
                print(record)

            Logger.info(__file__, f'Generation {i + 1} green order history finished')
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

        for i in range(total_green_volume + 1, total_orders_amount):
            Logger.debug(__file__, f'Started generation {i - total_green_volume} order history in blue-red zone')

            for record in self.__get_record_by_order_in_blue_red_zone(period_start, period_finish):
                Logger.debug(__file__,
                             'Generated record for {} blue-red order history: {}'.format(i - total_green_volume + 1,
                                                                                         record))
                print(record)

            Logger.info(__file__, f'Generation {i - total_green_volume} order history in blue-red zone finished')

            if period_start_counter < period_start_limit:
                period_start_counter += 1
            else:
                period_start += 1
                period_start_limit = self.configs.orders_volumes_for_generation[period_start][Values.BLUE_ZONE_VOLUME] \
                    if period_start < len(
                    self.configs.orders_volumes_for_generation) else self.configs.not_used_orders_amount

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
