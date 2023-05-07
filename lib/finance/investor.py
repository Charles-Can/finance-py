"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: Investor Class
"""
from uuid import uuid1

from ..utils.printer import Printer


class Investor:
    """Represents an Investor"""

    def __init__(self, name='', address='', phone_number=''):
        self.id = uuid1()
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.__stocks = []
        self.__bonds = []

    @property
    def stocks_count(self):
        """Count of stocks recorded by this investor"""
        return len(self.__stocks)

    @stocks_count.setter
    def stocks_count(self, _):
        # Computed property, cannot be set
        print('warn:: cannot set stocks count. computed value')

    @property
    def bonds_count(self):
        """Count of bonds recorded by this investor"""
        return len(self.__bonds)

    @bonds_count.setter
    def bonds_count(self, _):
        # Computed property, cannot be set
        print('warn:: cannot set bonds count. computed value')

    def generate_stocks_report(self):
        """Generates a stock report"""

        # initialize report size and headers
        printer = Printer() \
            .set_report_name(f'Stock Ownership for {self.name.title()}') \
            .set_headers(['Stock', 'Share #', 'Earnings/Loss', 'Yearly Earning/Loss']) \
            .set_column_width(20)

        # iterate stocks & add them to the report
        for stock in self.__stocks:
            printer.add_row([
                stock.symbol,
                stock.shares,
                f'${stock.earnings:,.2f}',
                f'{stock.yearly_earnings_percent:.2f}%'
            ])

        # generate report
        return printer.generate_table()

    def record_stock_purchase(self, stock):
        """Adds stock to investor stock investments"""

        # associates stock with investor
        stock.investor_id = self.id
        # add stock to stocks list
        self.__stocks.append(stock)

    def generate_bonds_report(self):
        """Generates a bond report"""

        # initialize report size and headers
        printer = Printer() \
            .set_report_name(f'Bond Ownership for {self.name.title()}') \
            .set_headers(['Bond', 'Quantity', 'Purchase Price', 'Current Price', 'Coupon', 'Yield', 'Purchase Date']) \
            .set_column_width(20)

        # iterate bonds & add them to the report
        for bond in self.__bonds:
            printer.add_row([
                bond.symbol,
                bond.shares,
                f'${bond.purchase_price:,.2f}',
                f'${bond.current_value:,.2f}',
                f'{bond.coupon:,.2f}',
                f'{bond.bond_yield:.2f}%',
                bond.purchase_date
            ])

        # generate report
        return printer.generate_table()

    def record_bond_purchase(self, bond):
        """Adds bond to investor bond investments"""

        # associates bond to investor
        bond.investor_id = self.id
        # adds bond to bonds
        self.__bonds.append(bond)
