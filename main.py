from datetime import datetime
from os.path import exists

from lib.finance import Investor, Stock, Bond
from lib.utils import CSVPropertyMapper, fill_from_csv

BONDS_FILE_PATH = './files/Lesson6_Data_Bonds.csv'
STOCKS_FILE_PATH = './files/Lesson6_Data_Stocks.csv'

def import_stocks(stocks_csv_file_path, investor):
    try:
        stock_mapper = CSVPropertyMapper() \
                            .add_mapping(0, 'symbol') \
                            .add_mapping(1, 'shares') \
                            .add_mapping(2, 'purchase_price') \
                            .add_mapping(3, 'current_value') \
                            .add_mapping(4, 'purchase_date')

        stock_data: list[Stock] = fill_from_csv(stocks_csv_file_path, Stock, stock_mapper)

        for stock in stock_data:
            investor.record_stock_purchase(stock)
    except Exception as e:
        print(f'Failed to parse stocks for investor err::{str(e)}')

def import_bonds(bonds_csv_file_path, investor):
    try:
        bond_mapper = CSVPropertyMapper() \
                            .add_mapping(0, 'symbol') \
                            .add_mapping(1, 'shares') \
                            .add_mapping(2, 'purchase_price') \
                            .add_mapping(3, 'current_value') \
                            .add_mapping(4, 'purchase_date') \
                            .add_mapping(5, 'coupon') \
                            .add_mapping(6, 'bond_yield')

        bond_data: list[Stock] = fill_from_csv(bonds_csv_file_path, Bond, bond_mapper)

        for bond in bond_data:
            investor.record_bond_purchase(bond)
    except Exception as e:
        print(f'Failed to parse bonds for investor err::{str(e)}')


def generate(investor, file_path):
    try:
        with open(file_path, 'w') as report:
            report.writelines(investor.generate_stocks_report())
            report.writelines('\n')
            report.writelines(investor.generate_bonds_report())
        print(f'{file_path} generated')
    except Exception as e:
        print(f'Failed to generate file {e}')   

def generate_investor_report(investor):
    doExit = False
    output_file_name = f"{investor.name.lower().replace(' ', '_')}_investment_report_{datetime.today().strftime('%m_%d_%Y')}.txt"

    while not doExit:
        doGenerate = input(f'Generate investment report for {investor.name.title()}? Type: yes or no \n').lower()

        if doGenerate == 'yes':
            if exists(output_file_name):
                doContinue = input(f'Warning! {output_file_name} already exists, continuing will overwrite it\'s contents.\nDo you wish to continue? Type yes or no \n').lower()

                if doContinue == 'yes':
                    generate(investor, output_file_name)
                    doExit = True
                elif doContinue == 'no':
                    doExit = True
                else:
                    print(f"Sorry, I don't understand \"{doContinue}\"")
            else:
                generate(investor, output_file_name)
                doExit = True
        elif doGenerate == 'no':
            doExit = True
        else: 
            print(f"Sorry, I don't understand \"{doGenerate}\"")

    print('Exiting...')




investor = Investor(name='Bob Smith', address='123 fake St.', phone_number='123-123-1234')
import_stocks(STOCKS_FILE_PATH, investor)
import_bonds(BONDS_FILE_PATH, investor)
generate_investor_report(investor)

