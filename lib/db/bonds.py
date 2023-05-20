from .table_object import TableObject
from ..utils.mapper import CSVPropertyMapper
from ..finance import Bond


class Bonds(TableObject):

    def __init__(self, connection):
        super().__init__(connection)
        self.__create_table__()
        self.__mapper = CSVPropertyMapper() \
            .add_mapping(0, 'id') \
            .add_mapping(1, 'investor_id') \
            .add_mapping(2, 'symbol') \
            .add_mapping(3, 'shares') \
            .add_mapping(4, 'purchase_price') \
            .add_mapping(5, 'current_value') \
            .add_mapping(6, 'purchase_date') \
            .add_mapping(7, 'coupon') \
            .add_mapping(8, 'bond_yield') \


    def __create_table__(self):
        self.q.execute("""
            CREATE TABLE bonds (
                investor_id INT NOT NULL,
                symbol TEXT NOT NULL,
                shares INT,
                purchase_price REAL,
                current_value REAL,
                purchase_date TEXT NOT NULL,
                coupon REAL,
                yield REAL
            );
        """)
        self.connection.commit()

    def insert(self, bond: Bond):
        q = self.q
        q.execute("INSERT INTO bonds VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  [bond.investor_id,
                   bond.symbol,
                   bond.shares,
                   bond.purchase_price,
                   bond.current_value,
                   bond.purchase_date,
                   bond.coupon,
                   bond.bond_yield])
        bond.id = q.lastrowid
        self.connection.commit()

    def select_by_investor_id(self, id) -> list[Bond]:
        q = self.q
        data = q.execute("""SELECT rowid AS id, investor_id, symbol, shares, purchase_price, purchase_price, purchase_date, coupon, yield
                            FROM bonds 
                            WHERE investor_id = ?""",
                         [id]).fetchall()
        bonds = []
        for record in data:
            bond = Bond()
            self.__mapper.map_properties(record, bond)
            bonds.append(bond)

        return bonds
