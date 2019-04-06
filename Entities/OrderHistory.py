from Decorators.Decorators import singleton


@singleton
class OrderHistory:
    def __init__(self):
        self.orders = dict()
        self.records = []

    def clear_history(self):
        self.orders.clear()
        self.records.clear()