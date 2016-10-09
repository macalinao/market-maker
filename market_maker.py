class MarketMaker(object):

    def __init__(self, exchange):
        self.exchange = exchange
        self.spread_pcts = {}

        exchange.on('out', self._handle_out)

    def init_market(self, security, max_bid, min_ask):
        """Setup the initial order book."""
        spread = float(min_ask - max_bid)
        spread_pct = spread / max_bid
        self.spread_pcts[security] = spread_pct
        # TODO(igm): support something other than uniform distribution

        # for every step, we will put in 100 limit orders.
        step = int(spread / 5)

        self.generate_orders(security, "buy", 100, max_bid, -2, 10)
        self.generate_orders(security, "sell", 100, min_ask, 2, 10)


    def generate_orders(
        self, security, direction, quantity,
        price, step, count=10,
    ):
        for x in range(count):
            self.exchange.place_order(
                security, direction, quantity, price + x * step,
            )

    def _handle_out(self, out):
        """This implements the strategy of the market maker
        where if the market maker is bought out, it tightens the
        spread back to the initial percentage."""
        order = self.exchange.orders[out['order_id']]
        security = order.security
        book = self.exchange.book

        # The current spread of the book.
        current_spread = book.spread(security)

        # The spread we wish to maintain in the next order.
        desired_spread_pct = self.spread_pcts[order.security]

        # Find ideal bid and ask
        min_ask = book.min_ask(security)
        max_bid = book.max_bid(security)
        desired_spread = None
        if min_ask:
            bid = min_ask / (1 + desired_spread_pct)
            desired_spread = min_ask - bid
        if max_bid:
            ask = max_bid * (1 + desired_spread_pct)
            desired_spread = ask - max_bid

        # step from desired spread
        desired_step = 0
        if desired_spread:
            desired_step = int(desired_spread / 5)

        # Populate empty bid or ask books
        if min_ask is None and max_bid is None:
            self.init_market(security, order.price - 5, order.price + 5)
            return
        if min_ask is None:
            self.generate_orders(
                security, "sell", 50, ask, desired_step, 10,
            )
            return
        if max_bid is None:
            self.generate_orders(
                security, "buy", 50, bid, desired_step, 10,
            )
            return

        # Don't intervene if the desired spread is greater than the existing spread
        if desired_spread > current_spread:
            return

        # Handle buy
        if order.direction == "buy":
            self.exchange.place_order(
                order.security, "buy", 50, bid,
            )

        # Handle sell
        else:
            self.exchange.place_order(
                order.security, "sell", 50, ask,
            )
