"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: Imports csv stocks and bonds files and outputs a financial report.
"""
from datetime import datetime
from os.path import exists

from lib.finance import Investor
from lib.utils import import_bonds, import_stocks

# Source data files
BONDS_FILE_PATH = './files/Lesson6_Data_Bonds.csv'
STOCKS_FILE_PATH = './files/Lesson6_Data_Stocks.csv'


def write_to_file(investor, file_path):
    """Writes investor report to file. WILL OVERWRITE EXISTING FILE DATA"""
    try:
        # open file in write mode
        with open(file_path, 'w') as report:
            # write stocks report
            report.writelines(investor.generate_stocks_report())
            report.writelines('\n')
            # write bonds report
            report.writelines(investor.generate_bonds_report())
        print(f'{file_path} generated')
    except Exception as e:
        # catch file errors
        print(f'Failed to generate file {e}')


def generate_investor_report(investor):
    """
        Generate investor report dialogue.
        - Asks if report is desired
        - Confirms overwrite if file already exists
    """
    # hold look exist strategy
    doExit = False
    # generated file name {investor}_investment_report_{current date}.txt
    output_file_name = f"{investor.name.lower().replace(' ', '_')}_investment_report_{datetime.today().strftime('%m_%d_%Y')}.txt"

    # cycles through prompts
    while not doExit:
        # capture if report is wanted
        doGenerate = input(
            f'Generate investment report for {investor.name.title()}? Type: yes or no \n').lower()

        if doGenerate == 'yes':
            # generate report
            if exists(output_file_name):
                # if report file already exists confirm overwrite
                doContinue = input(
                    f'Warning! {output_file_name} already exists, continuing will overwrite it\'s contents.\nDo you wish to continue? Type yes or no \n').lower()

                if doContinue == 'yes':
                    # create report & exit
                    write_to_file(investor, output_file_name)
                    doExit = True
                elif doContinue == 'no':
                    # exit
                    doExit = True
                else:
                    # NOOP restart dialogue
                    print(f"Sorry, I don't understand \"{doContinue}\"")
            else:
                # report file does not already exist, generate and exit
                write_to_file(investor, output_file_name)
                doExit = True
        elif doGenerate == 'no':
            # exit
            doExit = True
        else:
            # NOOP restart dialogue
            print(f"Sorry, I don't understand \"{doGenerate}\"")
    # exit message
    print('Exiting...')


# Create investor
investor = Investor(name='Bob Smith', address='123 fake St.',
                    phone_number='123-123-1234')
# get investment data
import_stocks(STOCKS_FILE_PATH, investor)
import_bonds(BONDS_FILE_PATH, investor)
# output report
generate_investor_report(investor)
