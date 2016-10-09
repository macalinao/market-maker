from exchange import Exchange
from exchange_client import ExchangeClient
from market_maker import MarketMaker

def main():
    client = ExchangeClient('god')
    client.handshake()

    exchange = Exchange(client)
    mm = MarketMaker(exchange)

main()
