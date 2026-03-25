STATIC_KIND = 0
FIELD_KIND = 1
ARG_KIND = 2
VAR_KIND = 3

class SymbolTable:
    def __init__(self):
        self.table_dict = dict()
        self.kind_index = {
            STATIC_KIND : 0,
            FIELD_KIND : 0,
            ARG_KIND : 0,
            VAR_KIND : 0
        }

    def __str__(self):
        return f"{self.table_dict}"

    def reset(self)->None:
        self.__init__()

    def define(self, name : str, symbol_type : str, kind : int)->None:
        # symbol_type: int, char, bool, *class_identifier*
        # kind: STATIC, FIELD, ARG, VAR
        if(name not in self.table_dict):
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

    def isIn(self, name : str)->bool:
        return (name in self.table_dict)
