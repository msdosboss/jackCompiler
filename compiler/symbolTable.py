STATIC = 0
FIELD = 1
ARG = 2
VAR = 3

class SymbolTable:
    def __init__(self):
        self.table_dict = dict()
        self.kind_index = {
            STATIC : 0,
            FIELD : 0,
            ARG : 0,
            VAR : 0
        }

    def reset(self)->None:
        self.table_dict = dict()

    def define(self, name : str, symbol_type : str, kind : int)->None:
        # symbol_type: int, char, bool, *class_identifier*
        # kind: STATIC, FIELD, ARG, VAR
        self.table_dict[name] = (symbol_type, kind, self.kind_index[kind])
        self.kind_index[kind] += 1

    def varCount(self, kind : int)->int:
        return self.kind_index[kind]

    def kindOf(self, name : str)->int:
        return self.table_dict[name][1]

    def typeOf(self, name : str)->str:
        return self.table_dict[name][0]

    def indexOf(self, name : str)->int:
        return self.table_dict[name][2]
