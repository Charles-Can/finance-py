"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: Imports csv stocks and bonds files and outputs a financial report.
"""
import sqlite3
from datetime import datetime
from matplotlib import pyplot as plt, figure as fig, axes

from lib.finance import Investor
from lib.utils import import_bonds, import_stocks, import_stock_price_history
from lib.db import Investors, Stocks, Bonds, StockPrices

# Source data files
BONDS_FILE_PATH = './files/Lesson6_Data_Bonds.csv'
STOCKS_FILE_PATH = './files/Lesson6_Data_Stocks.csv'
STOCK_PRICES_FILE_PATH = './files/AllStocks.json'

CHART_STYLE = 'Solarize_Light2'

db = sqlite3.connect(':memory:')

investor_store = Investors(db)
stock_store = Stocks(db)
bond_store = Bonds(db)
prices_store = StockPrices(db)


def insert_stocks_from_file(file_path: str, investor_id: int):
    # get investment data
    stocks = import_stocks(file_path)
    for stock in stocks:
        stock.investor_id = investor_id
        stock_store.insert(stock)


def insert_bonds_from_file(file_path: str, investor_id: int):
    bonds = import_bonds(file_path)
    for bond in bonds:
        bond.investor_id = investor_id
        bond_store.insert(bond)


def insert_prices_from_file(file_path: str):
    prices = import_stock_price_history(file_path)

    for price in prices:
        prices_store.insert(price)


def build_stock_plot_chart_by_investor(investor: Investor) -> tuple[fig.Figure, axes.Axes]:
    fig, ax = plt.subplots()

    stocks = stock_store.select_by_investor_id(investor.id)

    for stock in stocks:
        prices = prices_store.select_by_symbol(stock.symbol)
        dates = [pr.recorded_date for pr in prices]
        stock_values = [float(pr.close) * stock.shares for pr in prices]

        plt.plot(dates, stock_values, label=stock.symbol)

    # Format Chart display
    plt.title(f'stock values over time for {investor.name}'.title(), fontsize=18)
    ax.set_xlabel('Date Recorded', fontsize=14)
    ax.set_ylabel('Shares Value', fontsize=14)
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    plt.legend(loc='upper left')

    plt.xticks(rotation=45)

    return (fig, ax)


def main():

    # Create investor
    investor = Investor(name='Bob Smith', address='123 fake St.',
                        phone_number='123-123-1234')
    investor_store.insert(investor)

    insert_stocks_from_file(STOCKS_FILE_PATH, investor.id)
    insert_bonds_from_file(BONDS_FILE_PATH, investor.id)
    insert_prices_from_file(STOCK_PRICES_FILE_PATH)

    plt.style.use(CHART_STYLE)

    build_stock_plot_chart_by_investor(investor)

    plt.show()

    db.close()


if __name__ == '__main__':
    main()
