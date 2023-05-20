from .table_object import TableObject
from ..utils.mapper import CSVPropertyMapper
from ..finance import StockPrice


class StockPrices(TableObject):

    def __init__(self, connection):
        super().__init__(connection)
        self.__create_table__()
        self.__mapper = CSVPropertyMapper() \
            .add_mapping(0, 'id') \
            .add_mapping(1, 'symbol') \
            .add_mapping(2, 'date') \
            .add_mapping(3, 'open') \
            .add_mapping(4, 'high') \
            .add_mapping(5, 'low') \
            .add_mapping(6, 'close') \
            .add_mapping(7, 'volume') \


    def __create_table__(self):
        self.q.execute("""
            CREATE TABLE stock_prices (
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

    def select_by_symbol(self, symbol: str) -> list[StockPrice]:
        q = self.q
        data = q.execute("""
            SELECT rowid AS id, symbol, date, open, high, low, close, volume
            FROM stock_prices
            WHERE symbol = ?
        """, [symbol])

        prices = []

        for record in data:
            price = StockPrice()
            self.__mapper.map_properties(record, price)
            prices.append(price)

        return prices
