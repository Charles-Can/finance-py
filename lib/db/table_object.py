import sqlite3

class TableObject:

    __connection: sqlite3.Connection = None

    def __init__(self, connection: sqlite3.Connection):
        self.__connection = connection

    @property
    def q(self) -> sqlite3.Cursor:
        return self.__connection.cursor()
    
    @property
    def connection(self) -> sqlite3.Connection:
        return self.__connection