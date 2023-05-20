class StockPrice:
    def __init__(self, symbol='', date='', open='-', high='-', low='-', close='-', volume=0 ):
        self.id = None
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
