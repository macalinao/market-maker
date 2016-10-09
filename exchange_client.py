import json

class ExchangeClient(object):
    """
    Client for exchange.
    """
    name = ""

    def __init__(self, name):
        self.name = name

    def handshake(self):
        msg = json.dumps({"type": "handshake",
                          "name": self.name})
        send(msg)

    def market(self, order_id, security, direction, quantity):
        msg = json.dumps({"type": "market",
                          "order_id": order_id,
                          "security": security,
                          "direction": direction,
                          "quantity": quantity})
        send(msg)

    def limit(self, order_id, security, direction, price, quantity):
        msg = json.dumps({"type": "limit",
                          "order_id": order_id,
                          "security": security,
                          "direction": direction,
                          "price": price
                          "quantity": quantity})
        send(msg)

    def cancel(self, order_id):
        msg = json.dumps({"type": "cancel",
                          "order_id": order_id})
        send(msg)

    def send(self, msg):
        pass