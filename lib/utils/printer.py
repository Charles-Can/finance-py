"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality:  Printer class that generates a tabular report from lists
"""


class Printer:
    """Printer generates table with header. Supports chainable calls"""

    def __init__(self):
        self.headers = []
        """column headers"""
        self.rows = []
        """table data"""
        self.report_name = ''
        """Table header"""
        self.column_width = 30
        """Table column width"""

    def set_report_name(self, name='Untitled'):
        """Chainable report name setter"""
        self.report_name = name
        return self

    def set_column_width(self, width=30):
        """Chainable column width setter"""
        self.column_width = int(width)
        return self

    def set_headers(self, header_list=[]):
        """Chainable headers setter"""
        self.headers = header_list
        return self

    def add_row(self, row_list=[]):
        """Chainable adds table data. Must match header count"""
        if len(self.headers) == len(row_list):
            self.rows.append(row_list)
        else:
            print(f'Failed to add row. Row mismatch!')

        return self

    def generate_table(self):
        """Generates table"""
        table = ''
        # table header
        table += self.report_name.center(self.column_width * len(self.headers))
        table += '\n'
        table += '-' * self.column_width * len(self.headers)
        table += '\n'
        # Column headers
        table += ''.join([header.ljust(self.column_width)
                         for header in self.headers])
        table += '\n'
        table += '-' * self.column_width * len(self.headers)
        table += '\n'
        # table body
        for row in self.rows:
            table += ''.join([str(cell).ljust(self.column_width)
                             for cell in row])
            table += '\n'
        table += '-' * self.column_width * len(self.headers)
        table += '\n'

        return table
