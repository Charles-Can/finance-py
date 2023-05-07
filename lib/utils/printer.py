class Printer:
    def __init__(self):
        self.headers = []
        self.rows = []
        self.report_name = ''
        self.column_width = 30

    def set_report_name(self, name=''):
        self.report_name = name
        return self
    
    def set_column_width(self, width= 30):
        self.column_width = int(width)
        return self

    def set_headers(self, header_list=[]):
        self.headers = header_list
        return self
    
    def add_row(self, row_list=[]):
        if len(self.headers) == len(row_list):
            self.rows.append(row_list)
        else:
            print(f'Failed to add row. Row mismatch!')

        return self

    def generate_table(self):
        table = ''

        table += self.report_name.center(self.column_width * len(self.headers))
        table += '\n'
        table += '-' * self.column_width * len(self.headers)
        table += '\n'
        table += ''.join([header.ljust(self.column_width) for header in self.headers])
        table += '\n'
        table += '-' * self.column_width * len(self.headers)
        table += '\n'
        for row in self.rows:
            table += ''.join([str(cell).ljust(self.column_width) for cell in row])
            table += '\n'
        table += '-' * self.column_width * len(self.headers)
        table += '\n'
        
        return table
        