from exchange_client import ExchangeClient

class MarketMaker(object):

    def __init__(self, client):
        self.client = client

    def init_market(self, security, max_bid, min_ask):
        """Setup the initial order book."""
        spread = min_ask - max_bid
        # TODO(igm): support something other than uniform distribution

        # for every step, we will put in 100 limit orders.
        step = spread / 5

        for x in xrange(10):
            bid_id = "init-bid-{0}".format(x)
            price = max_bid - x * step
            self.client.limit(bid_id, security, "buy", price, 100)

            ask_id = "init-ask-{0}".format(x)
            price = min_ask + x * step
            self.client.limit(ask_id, security, "sell", price, 100)

def main():
    client = ExchangeClient()
    client.handshake()

    mm = MarketMaker(client)

main()
