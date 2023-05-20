from datetime import datetime

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

    @property
    def recorded_date(self):
        try:
            return datetime.strptime(self.date, '%d-%b-%y')
        except Exception as e:
            print(f'StockPrice:: failed to parse date for price: [{self.id}]\n{str(e)}')
            return datetime.today()
