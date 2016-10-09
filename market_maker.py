from exchange import Exchange, Order
from exchange_client import ExchangeClient

class MarketMaker(object):

    def __init__(self, exchange):
        self.exchange = exchange

        exchange.on('out', self._handle_out)

    def init_market(self, security, max_bid, min_ask):
        """Setup the initial order book."""
        spread = min_ask - max_bid
        # TODO(igm): support something other than uniform distribution

        # for every step, we will put in 100 limit orders.
        step = int(spread / 5)

        for x in xrange(10):
            bid = Order(
                security, "buy", 100, max_bid - x * step,
            )
            self.exchange.place_order(bid)
            ask = Order(
                security, "sell", 100, min_ask + x * step,
            )
            self.exchange.place_order(ask)

    def _handle_out(self, out):
        order = self.exchange.orders[out['order_id']]
        book = self.exchange.book

def main():
    client = ExchangeClient()
    client.handshake()

    exchange = Exchange(client)
    mm = MarketMaker(exchange)
    mm.init_market("IAN", 5100, 5200)

main()
