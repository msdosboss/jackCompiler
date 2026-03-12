# All the different token types
KEYWORD = 0
SYMBOL = 1
IDENTIFIER = 2
INT_CONST = 3
STRING_CONST = 4

# All different keywords
CLASS = 0
METHOD = 1
FUNCTION = 2
CONSTRUCTOR = 3
INT = 4
BOOLEAN = 5
CHAR = 6
VOID = 7
VAR = 8
STATIC = 9
FIELD = 10
LET = 11
DO = 12
IF = 13
ELSE = 14
WHILE = 15
RETURN = 16
TRUE = 17
FALSE = 18
NULL = 19
THIS = 20

keyword_dict = {
    "class" : CLASS,
    "method" : METHOD,
    "function" : FUNCTION,
    "constructor" : CONSTRUCTOR,
    "int" : INT,
    "bool" : BOOLEAN,
    "boolean" : BOOLEAN,
    "char" : CHAR,
    "void" : VOID,
    "var" : VAR,
    "static" : STATIC,
    "field" : FIELD,
    "let" : LET,
    "do" : DO,
    "if" : IF,
    "else" : ELSE,
    "while" : WHILE,
    "return" : RETURN,
    "true" : TRUE,
    "false" : FALSE,
    "null" : NULL,
    "this" : THIS
}

symbol_set = {
    '{',
    '}',
    '(',
    ')',
    '[',
    ']',
    '.',
    ',',
    ';',
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '>',
    '<',
    '=',
    '~'
}


identifier_symbol_set = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


class Tokenizer:
    def __init__(self, file_name: str) -> None:
        self.token_type = None
        self.file_name = file_name
        self.line_index = 0
        self.str_index = 0
        self.current_token = ""
        with open(file_name, "r") as f:
            self.file_text = f.readlines()

        for i, _ in enumerate(self.file_text):
            self.file_text[i] = self.file_text[i].replace('\n', '')

        self.current_char = self.file_text[0][0]


    def hasMoreTokens(self) -> bool:
        if(self.line_index == len(self.file_text)):
            return False
        if(self.str_index >= len(self.file_text[self.line_index])):
            return False
        
        return True


    def _skipWhiteSpace(self):
        #skips all white space
        while(self.current_char == ' ' or self.current_char == '\t'): 
            self._advanceFileText()

    def _advanceFileText(self):
        self.str_index += 1
        if(self.str_index >= len(self.file_text[self.line_index])):
           self.line_index += 1
           self.str_index = 0

        # added this to keep track of line count
        while(self.line_index < len(self.file_text) and len(self.file_text[self.line_index]) == 0):
            self.line_index += 1

        if(self.line_index >= len(self.file_text)):
            self.current_char = ' '
        else:
            self.current_char = self.file_text[self.line_index][self.str_index]
        

    def _skipComment(self):
        self.line_index += 1
        self.str_index = 0
        if(self.hasMoreTokens() is False):
            return False
        self.current_char = self.file_text[self.line_index][self.str_index]
        self._skipWhiteSpace()
        return True



    def advance(self) -> bool:
        if (self.hasMoreTokens() is False):
            self.token_type = -1
            return False

        self._skipWhiteSpace()

        if(self.current_char in symbol_set):
            self.token_type = -1
            # skip one line comments
            if(self.current_char == '/' and self.file_text[self.line_index][self.str_index + 1] == '/'):
                while(self.current_char == '/' and self.file_text[self.line_index][self.str_index] == '/'):
                    if(self._skipComment() is False):
                        return False
            # skip multi line comments
            elif(self.current_char == '/' and self.file_text[self.line_index][self.str_index + 1] == '*'):
                while(self.current_char != '*' or self.file_text[self.line_index][self.str_index + 1] != '/'):
                    self._advanceFileText()
                    if(self.str_index + 1 == len(self.file_text[self.line_index])):
                        if(self._skipComment() is False):
                            return False
                # move past the */ chars
                self._advanceFileText()
                self._advanceFileText()
                self._skipWhiteSpace()
 
            else:
                self.token_type = SYMBOL
                self.current_token = self.current_char
                self._advanceFileText() 
                return True

        self.current_token = ""
        if(self.current_char == '\"'):
            self.token_type = STRING_CONST
            self._advanceFileText()
            while(self.current_char != '\"'):
                self.current_token += self.current_char
                self._advanceFileText()
            self._advanceFileText()
            return True

        while(self.current_char != ' ' and self.current_char not in symbol_set):
            self.current_token += self.current_char
            self._advanceFileText() 

        if(self.current_token in keyword_dict):
            self.token_type = KEYWORD
            return True

        if(self.current_token.isdigit()):
            self.token_type = INT_CONST
            return True

        is_not_valid_indentifier = set(self.current_token) - set(identifier_symbol_set)

        if(is_not_valid_indentifier or self.current_token[0].isdigit()):
            self.token_type = -1
        else:
            self.token_type = IDENTIFIER

        return True

    # the int is a CONST defined type
    def tokenType(self):
        return self.token_type

    # the int is a CONST defined type
    def keyWord(self) -> int:
        if(self.tokenType() == KEYWORD):
            return keyword_dict[self.current_token]
        return -1

    def symbol(self) -> str:
        if(self.tokenType() == SYMBOL):
            return self.current_token
        print("calling symbol when type is not SYMBOL")
        return None

    def identifier(self) -> str:
        if(self.tokenType() == IDENTIFIER):
            return self.current_token
        print("calling identifier when type is not IDENTIFIER")
        return None

    def intVal(self) -> int:
        if(self.tokenType() == INT_CONST):
            return int(self.current_token)
        print("calling intVal when type is not INT_CONST")
        return -1

    def stringVal(self) -> str:
        if(self.tokenType() == STRING_CONST):
            return self.current_token
        print("calling stringVal when type is not STRING_CONST")
        return None

    def lineCount(self) -> int:
        return self.line_index + 1
