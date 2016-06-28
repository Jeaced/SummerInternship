# Here we can see how orders are handled because Nikita was too dumb
# to implement this using pure serializers and models. Enjoy your kostil.

"""
Class which represents order with with items
"""
class OrderWithItems():

    def __init__(self, order, items):
        """
        Params:
        order - order object from models
        items - list of objects with fields: id and amount
        amount"""
        self.id = order.id
        self.date = order.date
        self.total_price = order.total_price
        self.payment_method = order.payment_method
        self.user = order.user
        self.items = items

"""
Id amount pair class
"""
class ItemAmount():

    def __init__(self, item_id, amount):
        self.id = item_id
        self.amount = amount
