from exchange import Exchange, Order
from exchange_client import ExchangeClient

class MarketMaker(object):

    def __init__(self, exchange):
        self.exchange = exchange

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

def main():
    client = ExchangeClient()
    client.handshake()

    exchange = Exchange(client)
    mm = MarketMaker(exchange)
    mm.init_market("IAN", 5100, 5200)

main()
