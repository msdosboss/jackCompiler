class JackReferenceError(Exception):
    def __init__(self, var_name, line_number, subroutine_symbol_table, class_symbol_table):
        self.var_name = var_name
        self.line_number = line_number
        self.subroutine_symbol_table = subroutine_symbol_table
        self.class_symbol_table = class_symbol_table
        super().__init__()

    def __str__(self):
        return f"""Made a reference to undefined variable: {self.var_name}
                   On Line {self.line_number}
                   subroutine_symbol_table: {self.subroutine_symbol_table}
                   class_symbol_table {self.class_symbol_table}"""


