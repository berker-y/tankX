import threading
import websocket
import json


class ArbitrageBot:
    def __init__(self):
        self.prices = {}
        self.last_highest_profit = 0
        self.ws = None
        self.app_running = True
        self.required_pairs = ['BTCUSDT', 'ETHUSDT', 'BTCEUR', 'USDTTRY', 'BTCTRY', 'ETHBTC', 'SOLUSDT', 'JUPUSDT',
                               'JUPTRY',
                               'WIFUSDT', 'BNBUSDT', 'XRPUSDT'
            , 'RVNUSDT', 'OAXUSDT', 'FETUSDT', 'YGGUSDT', 'JUPUSDT', 'FTMUSDT', 'LTCUSDT', 'REIUSDT', 'ARBUSDT',
                               'COSUSDT',
                               'FILUSDT', 'BCHUSDT'
            , 'ALTUSDT', 'ICPUSDT', 'SUIUSDT', 'ADAUSDT', 'APTUSDT', 'WLDUSDT', 'ZRXUSDT', 'MOBUSDT', 'KMDUSDT',
                               'TRXUSDT',
                               'UNIUSDT', 'RSRUSDT'
            , 'MKRUSDT', 'INJUSDT', 'ETCUSDT', 'ZILUSDT', 'STXUSDT', 'RVNTRY', 'COSTRY', 'WIFTRY', 'ACATRY', 'FETTRY',
                               'ETHTRY',
                               'SOLTRY', 'XRPTRY'
            , 'AMPTRY', 'ARBTRY', 'JUPTRY', 'TRBTRY', 'RAYTRY', 'TRXTRY', 'FTMTRY', 'BNBTRY', 'XVGTRY', 'ZILTRY',
                               'APTTRY',
                               'CHZTRY', 'JTOTRY', 'MAVTRY'
            , 'APETRY', 'CKBTRY', 'GMTTRY', 'ICPTRY', 'XECTRY', 'INJTRY', 'XAITRY', 'ALTTRY', 'TIATRY', 'SUITRY',
                               'STXTRY',
                               'ADATRY', 'HOTTRY'
            , 'GRTTRY', 'ACHTRY', 'WLDTRY', 'LRCTRY', 'TLMTRY', 'MKRTRY', 'FILTRY', 'ENJTRY', 'BSWTRY', 'GALTRY',
                               'VICTRY',
                               'LTCTRY', 'ASRTRY', 'ENSTRY'
            , 'SOLBTC', 'BNBBTC', 'RVNBTC', 'WIFBTC', 'LTCBTC', 'FETBTC', 'OAXBTC', 'XRPBTC', 'ADXBTC', 'ADABTC',
                               'BCHBTC',
                               'FTMBTC', 'YGGBTC', 'STXBTC'
            , 'TRXBTC', 'COSBTC', 'ZRXBTC', 'KMDBTC', 'ETCBTC', 'ZILBTC', 'SUIBTC', 'APTBTC', 'ICPBTC', 'WLDBTC',
                               'INJBTC',
                               'FILBTC', 'DGBBTC', 'DOTBTC'
            , 'SEIBTC', 'VETBTC', 'NKNBTC', 'ALTBTC', 'CHZBTC', 'MOBBTC', 'ZECBTC', 'PHABTC', 'UNIBTC', 'TIABTC',
                               'ARBBTC', 'ONEBTC'
            , 'XLMBTC', 'MDXBTC', 'CFXBTC', 'XVSBTC', 'WANBTC', 'LTOBTC', 'SYSBTC', 'MKRBTC', 'LRCBTC', 'REQBTC',
                               'EOSBTC',
                               'ACHBTC', 'TRUBTC', 'LDOBTC', 'BNBETH', 'SOLBNB', 'FETBNB', 'BNBBRL', 'BCHBNB', 'XRPBNB',
                               'LTCBNB',
                               'TRXBNB', 'CTKBNB', 'ALTBNB',
                               'SUIBNB', 'XVSBNB', 'RAYBNB', 'VETBNB', 'INJBNB', 'ADABNB', 'ICPBNB', 'STXBNB', 'FTMBNB',
                               'BNBDAI',
                               'FILBNB', 'DOTBNB'
                               ]

    def on_open(self, ws):
        print("WebSocket connection opened")
        ws.send(json.dumps({
            'method': 'SUBSCRIBE',
            'params': [f"{symbol.lower()}@bookTicker" for symbol in self.required_pairs],
            'id': 1
        }))

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if 's' in data:
                symbol = data['s']
                self.prices[symbol] = {'bid': float(data['b']), 'ask': float(data['a'])}
            self.calculate_arbitrage()
        except Exception as e:
            print(f"Error processing message: {message}, error: {e}")

    def on_error(self, ws, error):
        print(f"Error: {error}")
        self.connect_websocket()  # Reconnect on error

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")

    def calculate_arbitrage(self):
        try:
            missing_pairs = [pair for pair in self.required_pairs if pair not in self.prices]
            if missing_pairs:
                print("Data for missing pairs are not yet available:", missing_pairs)
                return

            base_currencies = set()
            quote_currencies = set()
            for pair in self.required_pairs:
                if 'USDT' in pair:
                    parts = pair.split('USDT')
                    base = 'USDT' if parts[0] == '' else parts[0]
                    quote = 'USDT' if parts[1] == '' else parts[1]
                else:
                    base, quote = pair[:3], pair[3:]

                base_currencies.add(base)
                quote_currencies.add(quote)

            for base in base_currencies:
                for quote in quote_currencies:
                    if base != quote and base + quote in self.required_pairs:
                        for mid in base_currencies - {base, quote}:
                            if base + mid in self.required_pairs and mid + quote in self.required_pairs:
                                start_amount = 1
                                first_pair = base + mid
                                second_pair = mid + quote
                                third_pair = base + quote

                                amount = start_amount * self.prices[first_pair]['bid']
                                amount *= self.prices[second_pair]['bid']
                                amount /= self.prices[third_pair]['ask']
                                profit = amount - start_amount

                                if profit > self.last_highest_profit:
                                    self.last_highest_profit = profit
                                    print(f"Arbitrage Opportunity Found: {base} -> {mid} -> {quote} -> {base}")
                                    print(f"Beginning: {start_amount:.8f} {base}")
                                    print(f"Conclusion: {amount:.8f} {base}")
                                    print(f"Profit: {profit:.8f}")

        except KeyError as e:
            print(f"The expected data has not arrived yet: {e}")

    def connect_websocket(self):
        self.ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def start(self):
        self.connect_websocket()
        while self.app_running:
            command = input("Enter 'r' to reset the highest profit or 'q' to quit: \n").lower()
            if command == 'r':
                self.last_highest_profit = 0
                print("Arbitrage profit opportunity has been reset.")
            elif command == 'q':
                self.app_running = False
                self.ws.close()
                break


if __name__ == "__main__":
    bot = ArbitrageBot()
    bot.start()
