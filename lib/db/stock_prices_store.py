"""
    Author: Charles Candelaria
    Date: 05/20/2023
    Functionality: Handles ORM operations for StockPrice objects with SQLlite
"""
from .table_object import TableObject
from ..utils.mapper import PropertyMapper
from ..finance import StockPrice


class StockPricesStore(TableObject):
    """SQLlite storage api for StockPrice"""

    def __init__(self, connection):
        super().__init__(connection)
        self.__create_table__()
        self.__mapper = PropertyMapper() \
            .add_mapping(0, 'id') \
            .add_mapping(1, 'symbol') \
            .add_mapping(2, 'date') \
            .add_mapping(3, 'open') \
            .add_mapping(4, 'high') \
            .add_mapping(5, 'low') \
            .add_mapping(6, 'close') \
            .add_mapping(7, 'volume')
        """Holds stock_price table tuple mapping to StockPrice"""

    def __create_table__(self):
        """Creates stock_prices table"""
        self.q.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                symbol TEXT,
                date TEXT,
                open TEXT,
                high TEXT,
                low TEXT,
                close REAL,
                volume INTEGER
            );
        """)
        self.connection.commit()

    def insert(self, stockPrice: StockPrice):
        """Insert a StockPrice into store, updates id on success"""
        try:
            q = self.q
            q.execute("INSERT INTO stock_prices VALUES (?, ?, ?, ?, ?, ?, ?)",
                      [stockPrice.symbol,
                       stockPrice.date,
                       stockPrice.open,
                       stockPrice.high,
                       stockPrice.low,
                       stockPrice.close,
                       stockPrice.volume])
            stockPrice.id = q.lastrowid
            self.connection.commit()
        except Exception as e:
            print(f'StockPricesStore:: failed insert StockPrice\n{str(e)}')

    def select_by_symbol(self, symbol: str) -> list[StockPrice]:
        """Retrieves StockPrices from store by symbol"""
        prices = []
        try:
            q = self.q
            data = q.execute("""
                SELECT rowid AS id, symbol, date, open, high, low, close, volume
                FROM stock_prices
                WHERE symbol = ?
            """, [symbol])

            for record in data:
                price = StockPrice()
                self.__mapper.map_properties(record, price)
                prices.append(price)
        except Exception as e:
            print(
                f'StockPricesStore:: Failed to retrieve StockPrices for: {symbol}\n{str(e)}')
        return prices
