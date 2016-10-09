import uuid

def parse_message(message):
    if message['type'] == 'book':
        return Book(message)
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


class Book(object):

    def __init__(self, data):
        self.timestamp = data['timestamp']
        self.book = data['book']

    def min_ask(self, security):
        asks = self.book[security]['asks']
        if not asks:
            return None
        return min([price for price, _ in asks])


    def max_bid(self, security):
        bids = self.book[security]['bids']
        if not bids:
            return None
        return max([pq[0] for pq in bids])


    def spread(self, security):
        """Calculates the spread of a security."""
        min_ask = self.min_ask(security)
        max_bid = self.max_bid(security)
        if min_ask is None or max_bid is None:
            return None
        return min_ask - max_bid


class Exchange(object):

    def __init__(self, client):
        self.client = client
        self.orders = {}

        # Subscribers to different message types
        self.subscribers = {}

        client.on_message(self._handle_message)
        self.on('book', self._handle_book)

    def place_order(self, security, direction, amount, price=None):
        order = Order(security, direction, amount, price)
        self.orders[order.order_id] = order
        # Place order using exchange client
        if order.is_limit():
            self.client.limit(order.order_id, order.security, order.direction, order.price, order.quantity)
        else:
            self.client.market(order.order_id, order.security, order.direction, order.quantity)

    def on(self, message_type, cb):
        if not message_type in self.subscribers:
            self.subscribers[message_type] = []
        self.subscribers[message_type].append(cb)

    def _handle_message(self, message):
        """Handles incoming messages."""
        t = message['type']
        if not t in self.subscribers:
            return
        subs = self.subscribers[t]
        for sub in subs:
            sub(parse_message(message))

    def _handle_book(self, book):
        self.book = book
