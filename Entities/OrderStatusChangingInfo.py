class OrderStatusChangingInfo:
    def __init__(self, order_id, timestamp_millis, status, zone, period):
        '''
        Set params of order status changing information

        :param order_id: id of order
        :param timestamp_millis: milliseconds timestamp of order status changing
        :param zone: order status changing zone
        '''

        self.order_id = order_id
        self.timestamp_millis = timestamp_millis
        self.status = status
        self.zone = zone
        self.period = period

    def __str__(self):
        return 'ORDER ID: {}, TIMESTAMP: {}, STATUS: {}, ZONE: {}'.format(self.order_id,
                                                                          self.timestamp_millis,
                                                                          self.status.value,
                                                                          self.zone.value)
