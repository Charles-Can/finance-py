"""
    Author: Charles Candelaria
    Date: 05/20/2023
    Functionality: Handles ORM operations for Investor objects with SQLlite
"""
from .table_object import TableObject

from ..finance import Investor
from ..utils import PropertyMapper


class InvestorsStore(TableObject):
    """SQLlite storage api for Investors"""

    def __init__(self, connection):
        super().__init__(connection)
        self.__create_table__()
        self.__mapper = PropertyMapper() \
            .add_mapping(0, 'id') \
            .add_mapping(1, 'name') \
            .add_mapping(2, 'address') \
            .add_mapping(3, 'phone_number')
        """Holds investor table tuple mapping to Investor"""

    def __create_table__(self):
        """Creates investor table"""

        self.q.execute("""
            CREATE TABLE IF NOT EXISTS investors (
                name TEXT,
                address TEXT,
                phone_number TEXT
            );
        """)
        self.connection.commit()

    def insert(self, investor: Investor):
        """Insert a investor into store, updates id on success"""
        try:

            q = self.q
            q.execute("INSERT INTO investors VALUES (?, ?, ? );",
                      [investor.name, investor.address, investor.phone_number])

            investor.id = q.lastrowid
            self.connection.commit()
        except Exception as e:
            print(f'InvestorsStore:: failed insert Investor\n{str(e)}')

    def get_by_id(self, id) -> Investor | None:
        """Retrieve an Investor from store by id"""
        try:
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
        except Exception as e:
            print(
                f'InvestorsStore:: Failed to retrieve investor: {id}\n{str(e)}')
