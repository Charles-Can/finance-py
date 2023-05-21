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
from lib.db import InvestorsStore, StocksStore, BondsStore, StockPricesStore

# Source data files
BONDS_FILE_PATH = './files/Lesson6_Data_Bonds.csv'
STOCKS_FILE_PATH = './files/Lesson6_Data_Stocks.csv'
STOCK_PRICES_FILE_PATH = './files/AllStocks.json'

# app contsants
CHART_STYLE = 'Solarize_Light2'
SAVE_FOLDER = './out_files/'

# Setup database objects
db = sqlite3.connect(':memory:')

investor_store = InvestorsStore(db)
stock_store = StocksStore(db)
bond_store = BondsStore(db)
prices_store = StockPricesStore(db)


def insert_stocks_from_file(file_path: str, investor_id: int):
    """inserts stock data into store and associates it with an investor"""
    stocks = import_stocks(file_path)
    for stock in stocks:
        stock.investor_id = investor_id
        stock_store.insert(stock)


def insert_bonds_from_file(file_path: str, investor_id: int):
    """inserts bond data into store and associates it with an investor"""
    bonds = import_bonds(file_path)
    for bond in bonds:
        bond.investor_id = investor_id
        bond_store.insert(bond)


def insert_prices_from_file(file_path: str):
    """inserts stock price data into store"""
    prices = import_stock_price_history(file_path)

    for price in prices:
        prices_store.insert(price)


def build_stock_plot_chart_by_investor(investor: Investor) -> tuple[fig.Figure, axes.Axes]:
    """Builds stock plot chart"""
    f, ax = plt.subplots()
    # set size
    f.set_size_inches(8, 6)

    # get stocks for investor
    stocks = stock_store.select_by_investor_id(investor.id)

    for stock in stocks:
        # Get prices for the stock symbol
        prices = prices_store.select_by_symbol(stock.symbol)
        # pull dates
        dates = [pr.recorded_date for pr in prices]
        # pull values * shares
        stock_values = [float(pr.close) * stock.shares for pr in prices]

        plt.plot(dates, stock_values, label=stock.symbol)

    # Format Chart display
    # titles
    plt.title(
        f'stock values over time for {investor.name}'.title(), fontsize=18)
    ax.set_xlabel('Date Recorded', fontsize=14)
    ax.set_ylabel('Shares Value', fontsize=14)
    # set max xticks for chart
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    plt.xticks(rotation=45)
    # legend
    plt.legend(loc='upper left')

    return (fig, ax)


def main():

    # Create investor
    investor = Investor(name='Bob Smith', address='123 fake St.',
                        phone_number='123-123-1234')
    # save investor to store
    investor_store.insert(investor)

    # import data
    insert_stocks_from_file(STOCKS_FILE_PATH, investor.id)
    insert_bonds_from_file(BONDS_FILE_PATH, investor.id)
    insert_prices_from_file(STOCK_PRICES_FILE_PATH)

    # set chart style
    plt.style.use(CHART_STYLE)

    build_stock_plot_chart_by_investor(investor)

    # create filename for investor
    today = datetime.today().strftime('%d_%m_%y').lower()

    plt.savefig(
        f'{SAVE_FOLDER}{investor.name.replace(" ", "_").lower()}_{today}.pdf')
    plt.show()

    # close db connection
    db.close()


if __name__ == '__main__':
    main()
