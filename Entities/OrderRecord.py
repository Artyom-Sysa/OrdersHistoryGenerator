from Enums.Status import Status
from Entities.GeneralOrderInformation import GeneralOrderInformation


class OrderRecord(GeneralOrderInformation):
    def __init__(self, general_order_info, ms_timestamp, status):
        """
        :param general_order_info: instance of GeneralOrderInformation class
        :param status: Status enum value
        :param ms_timestamp: order status set time in millisecond with ms_timestamp format
        """

        super().__init__(general_order_info.id,
                         general_order_info.direction,
                         general_order_info.status_sequence,
                         general_order_info.currency_pair_name,
                         general_order_info.currency_pair_value,
                         general_order_info.init_currency_pair_value,
                         general_order_info.init_volume,
                         general_order_info.fill_currency_pair_value,
                         general_order_info.fill_volume,
                         general_order_info.statuses_in_blue_zone,
                         general_order_info.tags,
                         general_order_info.description)
        self.status = status
        self.ms_timestamp = ms_timestamp

        if status in [Status.NEW, Status.TO_PROVIDER, Status.REJECTED]:
            self.fill_volume = 0
            self.fill_currency_pair_value = 0

    def __str__(self):
        return 'ID: {},DIRECTION: {}, STATUS SEQUENCE: {}, CURRENCY PAIR NAME: {}, CURRENCY PAIR VALUE: {}, INIT CURRENCY PAIR VALUE {}, INIT VOLUME: {}, FILL CURRENCY PAIR VALUE: {}, FILL VOLUME: {}, STATUSES IN BLUE ZONE: {}, TAGS: {}, DESCRIPTIOM: {}, STATUS: {}, MS_TIMESTAMP: {}'.format(
            self.id,
            self.direction.value,
            self.status_sequence.value,
            self.currency_pair_name,
            self.currency_pair_value,
            self.init_currency_pair_value,
            self.init_volume,
            self.fill_currency_pair_value,
            self.fill_volume,
            self.statuses_in_blue_zone,
            self.tags,
            self.description,
            self.status.value,
            self.ms_timestamp
        )
