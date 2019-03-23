class OrderRecord:
    def __init__(self, general_order_info, status, ms_timestamp):
        """
        :param general_order_info: instance of GeneralOrderInformation class
        :param status: Status enum value
        :param ms_timestamp: order status set time in millisecond with ms_timestamp format
        """

        self.general_order_info = general_order_info
        self.status = status
        self.ms_timestamp = ms_timestamp

    def __str__(self):
        return "{}, STATUS: {}, MS_TIMESTAMP: {}".format(
            str(self.general_order_info),
            self.status.value,
            self.ms_timestamp
        )
