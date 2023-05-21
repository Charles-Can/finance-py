"""
    Author: Charles Candelaria
    Date: 05/20/2023
    Functionality: Collection of import util functions for CSV to stock, prices & bond
"""
import csv
import json

from ..finance.bond import Bond
from ..finance.stock import Stock
from ..finance.stock_price import StockPrice
from .mapper import PropertyMapper


def fill_from_csv(file_path, to_be_filled, mapper):
    """maps a CSV file to a collection of Objects"""
    data_list = []
    try:
        with open(file_path) as file_data:
            # read csv
            reader = csv.reader(file_data)
            # track header to skip
            isHeader = True
            for line in reader:
                # iterate csv lines
                if not isHeader:
                    # if not header map lin to object with mapper
                    instance = to_be_filled()
                    mapper.map_properties(line, instance)
                    # push mapped object to list
                    data_list.append(instance)
                # mark header skipped
                isHeader = False

    except FileNotFoundError:
        # catch file errors
        print(f'File: {file_path} not found!')

    return data_list


def import_stocks(stocks_csv_file_path) -> list[Stock]:
    stocks = []
    """Imports CSV data and maps it a Stock"""
    try:
        # map csv indexes to Stock properties in files/
        stock_mapper = PropertyMapper() \
            .add_mapping(0, 'symbol') \
            .add_mapping(1, 'shares') \
            .add_mapping(2, 'purchase_price') \
            .add_mapping(3, 'current_value') \
            .add_mapping(4, 'purchase_date')

        # Extract data from CSV
        stock_data: list[Stock] = fill_from_csv(
            stocks_csv_file_path, Stock, stock_mapper)

        # Loop through stock data and import it to investor
        for stock in stock_data:
            stocks.append(stock)
    except Exception as e:
        # handle parse errors
        print(f'Failed to parse stocks for investor err::{str(e)}')
    return stocks


def import_bonds(bonds_csv_file_path) -> list[Bond]:
    bonds = []
    """Imports CSV data and maps it to a Stock"""
    try:
        # map csv indexes to Bond properties in files/
        bond_mapper = PropertyMapper() \
            .add_mapping(0, 'symbol') \
            .add_mapping(1, 'shares') \
            .add_mapping(2, 'purchase_price') \
            .add_mapping(3, 'current_value') \
            .add_mapping(4, 'purchase_date') \
            .add_mapping(5, 'coupon') \
            .add_mapping(6, 'bond_yield')

        # Extract data from CSV
        bond_data: list[Stock] = fill_from_csv(
            bonds_csv_file_path, Bond, bond_mapper)

        # Loop through stock data and import it to investor
        for bond in bond_data:
            bonds.append(bond)
    except Exception as e:
        # handle parse errors
        print(f'Failed to parse bonds for investor err::{str(e)}')
    return bonds


def import_stock_price_history(json_file_path) -> list[StockPrice]:
    """Imports JSON data and maps it to a StockPrice"""
    prices = []

    try:
        # Set up mapper @SEE ./files/AllStocks.json
        price_mapper = PropertyMapper() \
            .add_mapping('Symbol', 'symbol') \
            .add_mapping('Date', 'date') \
            .add_mapping('Open', 'open') \
            .add_mapping('High', 'high') \
            .add_mapping('Low', 'low') \
            .add_mapping('Close', 'close') \
            .add_mapping('Volume', 'volume')

        with open(json_file_path) as json_data:
            price_data = json.load(json_data)

            for price in price_data:
                stock_price = StockPrice()
                price_mapper.map_properties(price, stock_price)
                prices.append(stock_price)

    except FileNotFoundError:
        # catch file errors
        print(f'File: {json_file_path} not found!')
    except Exception as e:
        print(f'Failed to parse stock price history err::{str(e)}')

    return prices
