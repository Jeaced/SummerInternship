"""
Logic for handling orders

Basic idea is that Order class here represents endpoint of the api.
It is serialized and deserialized to and from json,
then transformed into corresponding database models.
"""
from api.models import OrderDetail, OrderContent


class Order(object):
    def __init__(self, order_id, date, total_price, payment_method, user_id, items):
        self.id = order_id
        self.date = date
        self.total_price = total_price
        self.payment_method = payment_method
        self.user = user_id
        self.items = items


class ItemAmount(object):
    """
    Class is constructed as a pair of item id and amount.
    """

    def __init__(self, item_id, amount):
        self.id = item_id
        self.amount = amount


def _get_order_from_order_detail(order_detail, items):
    """
    :param order_detail - OrderDetail model instance
    :param items - list of ItemAmount objects
    :return Order instance
    """
    # TODO: fix model so user cannot be null
    user_id = 0 if order_detail.user is None else order_detail.user.id

    return Order(order_detail.id,
                 order_detail.date,
                 order_detail.total_price,
                 order_detail.payment_method,
                 user_id,
                 items
                 )


def _get_contents_by_id(order_contents, id):
    """
    :param order_contents - list of OrderContent model objects
    :param id: primary key of order
    :return: all OrderContent objects related to order with id.
    """
    contents = list()
    for order_content in order_contents:
        if order_content.order_id.id == id:
            contents.append(order_content)

    return contents


def _get_order_items(order_contents, id):
    """
    :param order_contents: see _get_contents_by_id
    :param id: see _get_contents_by_id
    :return: list of ItemAmount objects for that order
    """
    contents = _get_contents_by_id(order_contents, id)
    items = list()
    for content in contents:
        items.append(ItemAmount(content.item_id.id, content.amount))

    return items


def get_orders():
    """
    :return: All orders with items as instances of Order class
    """
    orders = OrderDetail.objects.all()
    order_contents = OrderContent.objects.all()

    orders_with_items = list()
    for order in orders:
        items = _get_order_items(order_contents, order.id)
        orders_with_items.append(_get_order_from_order_detail(order, items))

    return orders_with_items
