class GeneralOrderInformation:
    def __init__(self, id, direction, status_sequence, currency_pair_name, init_currency_pair_value,
                 init_volume, fill_currency_pair_value,
                 statuses_in_blue_zone, tags, description, fill_volume_percent=100):
        """
        :param id: order id
        :param direction: enum value of order direction
        :param status_sequence: enum value of order status sequence
        :param currency_pair_name: order currency pair
        :param init_currency_pair_value: initial currency pair value
        :param init_volume: initial currency pair volume
        :param fill_volume_percent: fill volume percent from initial volume
        :param fill_currency_pair_value:  fill currency pair value
        :param statuses_in_blue_zone: statuses in blue zone if order not in green zone
        :param tags: order tags string
        :param description: order description string
        """

        self.id = id
        self.direction = direction
        self.status_sequence = status_sequence
        self.currency_pair_name = currency_pair_name
        self.init_currency_pair_value = init_currency_pair_value
        self.init_volume = init_volume
        self.fill_volume_percent = fill_volume_percent
        self.fill_currency_pair_value = fill_currency_pair_value
        self.fill_volume = None
        self.statuses_in_blue_zone = statuses_in_blue_zone
        self.tags = tags
        self.description = description

    def __str__(self):
        return 'ID: {},DIRECTION: {}, STATUS SEQUENCE: {}, CURRENCY PAIR MANE {}, INIT CURRENCY PAIR VALUE {}, INIT VOLUME: {}, FILL CURRENCY PAIR VALUE: {}, FILL VOLUME PERCENT: {}, FILL VOLUME: {}, STATUSES IN BLUE ZONE: {}, TAGS: {}, DESCRIPTIOM: {}'.format(
            self.id,
            self.description.value,
            self.status_sequence,
            self.currency_pair_name,
            self.init_currency_pair_value,
            self.init_volume,
            self.fill_currency_pair_value,
            self.fill_volume_percent,
            self.fill_volume,
            self.statuses_in_blue_zone,
            self.tags,
            self.description
        )
