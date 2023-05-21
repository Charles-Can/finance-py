"""
    Author: Charles Candelaria
    Date: 05/20/2023
    Functionality: StockPrice Class
"""
from datetime import datetime


class StockPrice:
    def __init__(self, symbol='', date='', open='-', high='-', low='-', close='-', volume=0):
        self.id = None
        self.symbol = symbol
        """Stock symbol"""
        self.date = date
        """date string d-b-y"""
        self.open = open
        """Opening price"""
        self.high = high
        """Peak price"""
        self.low = low
        """Lowest price"""
        self.close = close
        """closing price"""
        self.volume = volume

    @property
    def recorded_date(self):
        """date as datetime""" 
        try:
            return datetime.strptime(self.date, '%d-%b-%y')
        except Exception as e:
            print(
                f'StockPrice:: failed to parse date for price: [{self.id}]\n{str(e)}')
            return datetime.today()
