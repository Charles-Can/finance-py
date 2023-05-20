from .table_object import TableObject

from ..finance import Investor
from ..utils import CSVPropertyMapper


class InvestorsStore(TableObject):

    def __init__(self, connection):
        super().__init__(connection)
        self.__create_table__()
        self.__mapper = CSVPropertyMapper() \
            .add_mapping(0, 'id') \
            .add_mapping(1, 'name') \
            .add_mapping(2, 'address') \
            .add_mapping(3, 'phone_number')

    def __create_table__(self):
        self.q.execute("""
            CREATE TABLE IF NOT EXISTS investors (
                name TEXT,
                address TEXT,
                phone_number TEXT
            );
        """)
        self.connection.commit()

    def insert(self, investor: Investor):
        q = self.q
        q.execute("INSERT INTO investors VALUES (?, ?, ? );",
                  [investor.name, investor.address, investor.phone_number])

        investor.id = q.lastrowid
        self.connection.commit()

    def get_by_id(self, id) -> Investor | None:
        q = self.q
        data = q.execute("""SELECT rowid AS id, name, address, phone_number 
                            FROM investors 
                            WHERE rowid = ?;""",
                         [id]).fetchone()

        if data:
            investor = Investor()
            self.__mapper.map_properties(data, investor)
            return investor
        self.connection.commit()
