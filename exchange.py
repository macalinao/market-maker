import uuid

def parse_message(message):
    return message

class Order(object):

    def __init__(self, security, direction, quantity, price=None):
        self.order_id = str(uuid.uuid4())
        self.security = security
        self.direction = direction
        self.quantity = quantity
        self.price = price

    def is_limit(self):
        return self.price is not None

class Exchange(object):

    def __init__(self, client):
        self.client = client
        self.orders = {}

        # Subscribers to different message types
        self.subscribers = {}

        client.on_message(self._handle_message)

    def place_order(self, order):
        self.orders[order.order_id] = order
        # Place order using exchange client
        if order.is_limit():
            self.client.limit(order.order_id, order.security, order.direction, order.price, order.quantity)
        else:
            self.client.market(order.order_id, order.security, order.direction, order.quantity)

    def _handle_message(self, message):
        """Handles incoming messages."""
        t = message['type']
        if not t in self.subscribers:
            return
        subs = self.subscribers[t]
        for sub in subs:
            sub(parse_message(message))
