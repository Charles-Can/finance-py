"""
    Author: Charles Candelaria
    Date: 06/02/2023
    Functionality: User Polygon.io to pull stock prices by symbol and data. Polygon.io's free
    account allows to pull historical data up to 2 years back. For the free account, the api
    rate limits request to 5 per minute. Since I'm cheap, this harvester pulls until it's request
    throttle and then sleeps 1 minute before restarting. Includes retry logic and skipping for no data
    scenarios that come up for holidays and weekends.

    Basic flow:
    1. Read json file into memory
    2. Build a dictionary of stocks with last known price by date
    3. Mark each stock either "pending" or "complete" with first date and last date price
    4. Loop through "pending" symbols and attempt to load the price for the next date until we reach today
    5. Push each price into in memory list from file
    6. Write in memory list to json file

    @SEE https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date

"""
import pandas as pd
import pandas
from datetime import datetime, timedelta
import requests
import time
import sys


class HarvestStatus:
    """'Enum' class used to hold Harvest statuses"""
    PENDING = 'PENDING'
    """Harvest has not completed"""
    COMPLETE = 'COMPLETE'
    """Harvest has completed"""
    ERROR = 'ERROR'
    """Harvest is in error state Not Used"""


def get_start_of_today() -> datetime:
    """Get today at midnight"""
    return datetime.combine(datetime.today().date(), datetime.min.time())


def ts_gte(ts1: datetime | pandas.Timestamp, ts2: datetime | pandas.Timestamp) -> bool:
    """Returns whether datetime or timestamp is greater than or equal to another datetime or timestamp"""
    date1 = timestamp_to_datetime(ts1)
    date2 = timestamp_to_datetime(ts2)

    time_delta = (date1 - date2).days

    return time_delta > 0 or time_delta == 0


def ts_lte(ts1: datetime | pandas.Timestamp, ts2: datetime | pandas.Timestamp) -> bool:
    """Returns whether datetime or timestamp is less than or equal to another datetime or timestamp"""
    date1 = timestamp_to_datetime(ts1)
    date2 = timestamp_to_datetime(ts2)

    time_delta = (date1 - date2).days

    return time_delta < 0 or time_delta == 0


def timestamp_to_datetime(ts: pandas.Timestamp | datetime) -> datetime:
    """Converts timestamp to datetime"""
    try:
        if isinstance(ts, datetime):
            return ts
        else:
            return datetime.strftime(ts, '%b %d %H:%M:%S %Y')
    except Exception as e:
        print(
            f'timestamp_to_datetime::Failed to convert value to datetime {e}')
        return get_start_of_today()


EARLIEST_DATE = get_start_of_today() - timedelta(days=365 * 2)
"""Holds earliest allowed request price. 2 years before today"""
MAX_RETRIES = 3
"""Amount of request retries before moving on"""

FILE_PATH = './files/stock_price_data.json'
"""Path to json file"""

API_KEY = None

STOCK_SYMBOLS = [
    'GOOG',
    'MSFT',
    'AIG',
    'META',
    'M',
    'F',
    'IBM'
]
"""Static list of stocks to pull prices for"""

STOCK_DATES = {}
"""
Holds stock summary of data.
    key: stock_symbol
    tail: first date recorded for stock
    head: last date recorded for stock
    status: pending | complete @See HarvestStatus
"""

# Load stocks
working_df = pd.read_json(FILE_PATH)


def build_stock_dates():
    """Creates a stock_date entry for each symbol in the stock symbols list"""
    for symbol in STOCK_SYMBOLS:
        # filter to just this symbol
        df = working_df[working_df.Symbol == symbol]

        # set defaults
        max_date = EARLIEST_DATE
        min_date = EARLIEST_DATE

        # if there is price date for symbol use those dates for min & max
        if len(df) > 0:
            max_date = df['Date'].max()
            min_date = df['Date'].min()

        STOCK_DATES[symbol] = {
            'head': max_date if ts_gte(max_date, EARLIEST_DATE) else EARLIEST_DATE,
            'tail': min_date,
            'status': HarvestStatus.COMPLETE if ts_gte(max_date, get_start_of_today()) else HarvestStatus.PENDING
        }


def main():
    # require api key
    if len(sys.argv) < 2:
        print(f'Please provide polygon.io api key')
        sys.exit(2)
    else:
        API_KEY = sys.argv[1]
        print(API_KEY)

    build_stock_dates()

    for symbol, data in STOCK_DATES.items():

        if data['status'] == HarvestStatus.PENDING:
            # only request for pending stocks
            request_count = 0

            while ts_lte(data['head'], get_start_of_today() - timedelta(days=1)):
                # keep requesting until we reach today

                req_date = data['head'] + timedelta(days=1)  # advance one day

                request_count += 1  # increment request count
                response = None # @todo - should be typed as a response dataclass or None

                print(f'symbol:{symbol}')
                print(f'date:{req_date.strftime("%Y-%m-%d")}')

                try:
                    # make api request
                    response = requests.get(
                        f'https://api.polygon.io/v1/open-close/{symbol.upper()}/{req_date.strftime("%Y-%m-%d")}?apiKey={API_KEY}').json()
                except Exception as e:
                    response = {
                        'status': 'ERROR',
                        'ERROR': f'Request failed {str(e)}'
                    }
                # handle api error responses
                if response.get('status', 'ERROR') == 'ERROR':
                    if 'exceeded the maximum requests' in response.get('error', ''):
                        print('hit api request limit, waiting one minute...')
                        # wait on minute and then retry with out advancing date
                        time.sleep(61)
                    elif request_count >= MAX_RETRIES:
                        # max retries hit reset to next date and continue
                        print(
                            f'Max retries hit for {symbol}:{str(req_date)} message: {response.get("error", "NO_ERROR_SUPPLIED")}')
                        print('Moving to next date')
                        data['head'] = req_date
                        request_count = 0
                    else:
                        # some other error, retry and hope for the best
                        print(response)
                        print(
                            f'Request [count {request_count}] for {symbol}:{str(req_date)} failed with {response.get("error", "NO_ERROR_SUPPLIED")}')
                        print('retrying...')

                    continue  # restart loop
                elif response.get('status', '') == 'NOT_FOUND':
                    # no data for this symbol & date move on
                    print(
                        f'No data for {symbol.replace("-", "")}:{str(req_date)}')
                    data['head'] = req_date
                    continue

                data['head'] = req_date  # advance date for next iteration
                request_count = 0  # reset request count

                # create new row for json file
                new_row = {
                    'Symbol': response.get('symbol', 'not_supplied'),
                    'Date': pd.to_datetime(response['from']),
                    'Open': response['open'],
                    'High': response['high'],
                    'Low': response['low'],
                    'Close': response['close'],
                    'Volume': int(response['volume'])
                }
                # append new row
                working_df.loc[len(working_df)] = new_row
                # print summary
                print(response)
                print(working_df.tail())
                print('\n\n')

                # write new data to file
                with open(FILE_PATH, 'w') as harvested:
                    # convert date format to string to match course material format
                    to_write = working_df.copy()
                    to_write['Date'] = to_write['Date'].dt.strftime('%d-%b-%y')
                    # write json to file
                    json = to_write.to_json(orient='records', indent=2)
                    harvested.write(json)
        else:
            # symbol has completed!
            print(f'Harvesting complete for [{symbol}]')
            data['status'] = HarvestStatus.COMPLETE

    print('-'*50)
    print('ALL STOCKS COMPLETED')
    print('-'*50)


if __name__ == '__main__':
    main()
