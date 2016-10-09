import unittest
from unittest.mock import Mock, MagicMock

from exchange import Order, Book
from market_maker import MarketMaker

class MarketMakerTestCase(unittest.TestCase):

    def test_init_market(self):
        exchange = Mock()
        mm = MarketMaker(exchange)
        mm.init_market('AAPL', 100, 110)
        expected = [
            (("AAPL", "buy", 100, 100),),
            (("AAPL", "buy", 100, 98),),
            (("AAPL", "buy", 100, 96),),
            (("AAPL", "buy", 100, 94),),
            (("AAPL", "buy", 100, 92),),
            (("AAPL", "buy", 100, 90),),
            (("AAPL", "buy", 100, 88),),
            (("AAPL", "buy", 100, 86),),
            (("AAPL", "buy", 100, 84),),
            (("AAPL", "buy", 100, 82),),
            (("AAPL", "sell", 100, 110),),
            (("AAPL", "sell", 100, 112),),
            (("AAPL", "sell", 100, 114),),
            (("AAPL", "sell", 100, 116),),
            (("AAPL", "sell", 100, 118),),
            (("AAPL", "sell", 100, 120),),
            (("AAPL", "sell", 100, 122),),
            (("AAPL", "sell", 100, 124),),
            (("AAPL", "sell", 100, 126),),
            (("AAPL", "sell", 100, 128),),
        ]
        assert exchange.place_order.call_args_list == expected

    def test_handle_out(self):
        exchange = MagicMock(
            book=Book({
                'timestamp': 0,
                'book': {
                    'AAPL': {
                        'asks': [
                            (120, 10),
                            (110, 10),
                        ],
                        'bids': [
                            (90, 10),
                        ],
                    }
                },
            }),
            orders={
                'buy': Order(
                    'AAPL', 'buy', 10, 100,
                ),
            },
        )

        mm = MarketMaker(exchange)
        mm.spread_pcts['AAPL'] = 0.08
        mm._handle_out({
            'order_id': 'buy',
        })

        assert exchange.place_order.call_count == 1
        first_call = exchange.place_order.call_args_list[0]

        max_bid = first_call[0][3]
        spread = (110 - max_bid) / max_bid

        # check spread is actually 8%
        self.assertAlmostEqual(spread, 0.08)
