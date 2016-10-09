import json

class ExchangeClient(object):
    """
    Client for exchange.
    """
    def __init__(self):
        pass

    def handshake(self):
        pass

    def market(self, order_id, security, direction, quantity):
        pass

    def limit(self, order_id, security, direction, price, quantity):
        pass

    def cancel(self, order_id):
        pass

    def _handle_message(self, msg):
        data = json.loads(msg)
        # TODO(igm): handle message

    def on(self, msg_type, cb):
        pass
