"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: Imports csv stocks and bonds files and outputs a financial report.
"""
import sqlite3

from lib.finance import Investor
from lib.utils import import_bonds, import_stocks, import_stock_price_history
from lib.db import Investors, Stocks, Bonds, StockPrices

# Source data files
BONDS_FILE_PATH = './files/Lesson6_Data_Bonds.csv'
STOCKS_FILE_PATH = './files/Lesson6_Data_Stocks.csv'
STOCK_PRICES_FILE_PATH = './files/AllStocks.json'

db = sqlite3.connect(':memory:')

investor_store = Investors(db)
stock_store = Stocks(db)
bond_store = Bonds(db)
prices_store = StockPrices(db)

def main():

    # Create investor
    investor = Investor(name='Bob Smith', address='123 fake St.',
                        phone_number='123-123-1234')
    investor_store.insert(investor)
    


    # get investment data
    stocks = import_stocks(STOCKS_FILE_PATH)
    for stock in stocks:
        stock.investor_id = investor.id
        stock_store.insert(stock)


    bonds = import_bonds(BONDS_FILE_PATH)
    for bond in bonds:
        bond.investor_id = investor.id
        bond_store.insert(bond)


    prices = import_stock_price_history(STOCK_PRICES_FILE_PATH)

    for price in prices:
        prices_store.insert(price)

    # output report
    # generate_investor_report(investor)
    db.close()


if __name__ == '__main__':
    main()