from Decorators.Decorators import singleton


@singleton
class OrderHistory:
    def __init__(self):
        self.orders = dict()
        self.red_records = list()
        self.green_records = list()
        self.blue_records = list()

    def clear_history(self):
        self.orders.clear()
        self.red_records.clear()
        self.blue_records.clear()
        self.green_records.clear()
