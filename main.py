"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: Imports csv stocks and bonds files and outputs a financial report.
"""
from datetime import datetime
from os.path import exists

from lib.finance import Investor
from lib.utils import import_bonds, import_stocks, import_stock_price_history

# Source data files
BONDS_FILE_PATH = './files/Lesson6_Data_Bonds.csv'
STOCKS_FILE_PATH = './files/Lesson6_Data_Stocks.csv'
STOCK_PRICES_FILE_PATH = './files/AllStocks.json'




def main():

    # Create investor
    investor = Investor(name='Bob Smith', address='123 fake St.',
                        phone_number='123-123-1234')
    # get investment data
    stocks = import_stocks(STOCKS_FILE_PATH)
    bonds = import_bonds(BONDS_FILE_PATH)
    prices = import_stock_price_history(STOCK_PRICES_FILE_PATH)

    # output report
    # generate_investor_report(investor)


if __name__ == '__main__':
    main()