import unittest
from unittest.mock import Mock

from exchange import Order
from market_maker import MarketMaker

class MarketMakerTestCase(unittest.TestCase):

    def test_init_market(self):
        exchange = Mock()
        mm = MarketMaker(exchange)
        mm.init_market('AAPL', 100, 110)
        expected = [
            ("AAPL", "buy", 100, 98),
            ("AAPL", "sell", 100, 112),
            ("AAPL", "buy", 100, 96),
            ("AAPL", "sell", 100, 114),
            ("AAPL", "buy", 100, 94),
            ("AAPL", "sell", 100, 116),
            ("AAPL", "buy", 100, 92),
            ("AAPL", "sell", 100, 118),
            ("AAPL", "buy", 100, 90),
            ("AAPL", "sell", 100, 120),
            ("AAPL", "buy", 100, 88),
            ("AAPL", "sell", 100, 122),
            ("AAPL", "buy", 100, 86),
            ("AAPL", "sell", 100, 124),
            ("AAPL", "buy", 100, 84),
            ("AAPL", "sell", 100, 126),
            ("AAPL", "buy", 100, 82),
            ("AAPL", "sell", 100, 128),
            ("AAPL", "buy", 100, 80),
            ("AAPL", "sell", 100, 130),
        ]
        exchange.place_order.call_args_list == expected
        pass
