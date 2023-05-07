"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: Stock investment Class
"""
from datetime import datetime

from .investment import Investment


class Stock(Investment):
    """Represents a stock investment"""

    # backing variables
    _current_value = 0
    _shares = 0
    _purchase_price = 0

    def __init__(self, symbol='', shares=0, purchase_price=0, current_value=0, purchase_date=''):
        super().__init__()
        self.symbol = symbol
        """Stock symbol"""
        self.shares = shares
        self.purchase_price = purchase_price
        self.current_value = current_value
        self.purchase_date = purchase_date
        """Purchase date MM/DD/YYYY"""

    @property
    def current_value(self):
        """current stock value. Not computed"""
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = float(value)

    @property
    def shares(self):
        """Number of shares"""
        return self._shares

    @shares.setter
    def shares(self, value):
        self._shares = int(value)

    @property
    def purchase_price(self):
        """Recorded purchase price"""
        return self._purchase_price

    @purchase_price.setter
    def purchase_price(self, value):
        self._purchase_price = float(value)

    @property
    def earnings(self):
        """Calculated earnings"""
        return (self.current_value - self.purchase_price) * self.shares

    @property
    def yearly_earnings_percent(self):
        """Calculated yearly earning percentage since purchase"""
        ONE_YEAR_IN_DAYS = 365
        today = datetime.today()
        date_purchased = None
        percentage = 0
        try:
            # attempt date parse
            month, day, year = self.purchase_date.split('/')
            date_purchased = datetime(int(year), int(month), int(day))
        except:
            # generate error message
            investor = self.investor_id or 'Unknown'
            symbol = self.symbol or 'Unknown'
            print(
                f'Failed to calculate yearly earnings percent for {investor}::{symbol} invalid purchase date')
        else:
            # calculate percentage
            years = (today - date_purchased).days / ONE_YEAR_IN_DAYS
            percentage = (
                ((self.current_value - self.purchase_price) / self.purchase_price) / years) * 100

        return percentage
