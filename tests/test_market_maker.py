import unittest
from unittest.mock import Mock

from market_maker import MarketMaker

class MarketMakerTestCase(unittest.TestCase):

    def test_init_market(self):
        exchange = Mock()
        mm = MarketMaker(exchange)
        pass
