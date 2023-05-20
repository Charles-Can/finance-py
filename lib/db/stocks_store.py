from .table_object import TableObject
from ..utils.mapper import PropertyMapper
from ..finance import Stock


class StocksStore(TableObject):

    def __init__(self, connection):
        super().__init__(connection)
        self.__create_table__()
        self.__mapper = PropertyMapper() \
            .add_mapping(0, 'id') \
            .add_mapping(1, 'investor_id') \
            .add_mapping(2, 'symbol') \
            .add_mapping(3, 'shares') \
            .add_mapping(4, 'purchase_price') \
            .add_mapping(5, 'current_value') \
            .add_mapping(6, 'purchase_date') \


    def __create_table__(self):
        self.q.execute("""
            CREATE TABLE stocks (
                investor_id INT NOT NULL,
                symbol TEXT NOT NULL,
                shares INT,
                purchase_price REAL,
                current_value REAL,
                purchase_date TEXT NOT NULL
            );
        """)
        self.connection.commit()

    def insert(self, stock: Stock):
        q = self.q
        q.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?)",
                  [stock.investor_id, stock.symbol, stock.shares, stock.purchase_price, stock.current_value, stock.purchase_date])
        stock.id = q.lastrowid
        self.connection.commit()

    def select_by_investor_id(self, id) -> list[Stock]:
        q = self.q
        data = q.execute("""SELECT rowid AS id, investor_id, symbol, shares, purchase_price, purchase_price, purchase_date 
                            FROM stocks 
                            WHERE investor_id = ?""",
                         [id]).fetchall()
        stocks = []
        for record in data:
            stock = Stock()
            self.__mapper.map_properties(record, stock)
            stocks.append(stock)

        return stocks
