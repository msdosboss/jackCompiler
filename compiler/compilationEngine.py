from VMWriter import VMWriter
from symbolTable import SymbolTable
from tokenizer import Tokenizer
from tokenizer import KEYWORD
from tokenizer import SYMBOL
from tokenizer import IDENTIFIER
from tokenizer import INT_CONST
from tokenizer import STRING_CONST
from tokenizer import CLASS
from tokenizer import METHOD
from tokenizer import FUNCTION
from tokenizer import CONSTRUCTOR
from tokenizer import STATIC
from tokenizer import FIELD
from tokenizer import INT
from tokenizer import CHAR
from tokenizer import BOOLEAN
from tokenizer import VAR
from tokenizer import DO
from tokenizer import LET
from tokenizer import IF
from tokenizer import WHILE
from tokenizer import RETURN
from tokenizer import ELSE
from tokenizer import TRUE
from tokenizer import FALSE
from tokenizer import NULL
from tokenizer import THIS
from tokenizer import VOID
from tokenizer import keyword_dict

from VMWriter import CONSTANT_SEG
from VMWriter import ADD
from VMWriter import SUB
from VMWriter import NEG
from VMWriter import EQ
from VMWriter import GT
from VMWriter import LT
from VMWriter import AND
from VMWriter import OR
from VMWriter import NOT

symbol_to_unary_command_dict = {
    '-' : NEG,
    '~' : NOT
}

symbol_to_command_dict = {
    '+' : ADD,
    '-' : SUB,
    '=' : EQ,
    '>' : GT,
    '<' : LT,
    '&' : AND,
    '|' : OR
}

from symbolTable import STATIC_KIND
from symbolTable import FIELD_KIND
from symbolTable import ARG_KIND
from symbolTable import VAR_KIND

kind_dict = {
    "static" : STATIC_KIND,
    "field" : FIELD_KIND,
    "arg" : ARG_KIND,
    "var" : VAR_KIND
}

from VMWriter import segment_dict 

from syntaxException import JackSyntaxError

reverse_segment_dict = {value: key for key, value in segment_dict.items()}
reverse_keyword_dict = {value: key for key, value in keyword_dict.items()}
reverse_keyword_dict[-1] = "Non-keyword"

token_type_dict = {
    -1 : "invalid",
    KEYWORD : "keyword",
    SYMBOL : "symbol",
    IDENTIFIER : "identifier",
    INT_CONST : "integerConstant",
    STRING_CONST : "stringConstant"
}

operator_set = {
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '>',
    '<',
    '='
}

unaryOp_set = {
    '-',
    '~'
}

keyword_const_set = {
    TRUE,
    FALSE,
    NULL,
    THIS
}

class CompilationEngine:
    def __init__(self, tokenizer : Tokenizer, input_file_name : str, class_symbol_table : SymbolTable, subroutine_symbol_table : SymbolTable, writer : VMWriter):
        self.tokenizer = tokenizer
        self.input_file_name = input_file_name
        self.output_file = open(input_file_name.replace(".jack", ".xml"), "w")
        self.tab_count = 0
        self.statement_method_dict = {
            DO : self.compileDo,
            LET : self.compileLet,
            IF : self.compileIf,
            WHILE : self.compileWhile,
            RETURN : self.compileReturn
        }       
        self.class_symbol_table = class_symbol_table
        self.subroutine_symbol_table = subroutine_symbol_table
        self.writer = writer


    def _writeTab(self):
        for _ in range(self.tab_count):
            self.output_file.write("  ")


    def _writeTag(self, tag : str, token : str):
        self._writeTab()
        if(token == '>'):
            token = '&gt;'
        elif(token == '<'):
            token = '&lt;'
        elif(token == '&'):
            token = '&amp;'
        self.output_file.write(f"<{tag}> {token} </{tag}>" + "\n")

    def _indentifierCheck(self, compile_step_name):
        if(self.tokenizer.tokenType() != IDENTIFIER):
            raise JackSyntaxError(
                    compile_step = compile_step_name,
                    file_name = self.input_file_name,
                    line_count = self.tokenizer.lineCount(),
                    actual_token = self.tokenizer.current_token,
                    actual_type = token_type_dict[self.tokenizer.tokenType()],
                    expected_type = "Identifier"
                )
        self.tokenizer.advance()
        return self.tokenizer.current_token

    def _symbolCheck(self, symbol, compile_step_name):
        if(self.tokenizer.current_token != symbol):
            raise JackSyntaxError(
                    compile_step = compile_step_name,
                    file_name = self.input_file_name,
                    line_count = self.tokenizer.lineCount(),
                    actual_token = self.tokenizer.current_token,
                    actual_type = token_type_dict[self.tokenizer.tokenType()],
                    expected_token = symbol
                )
        self.tokenizer.advance()

    def _keyWordCheck(self, key_word, compile_step_name):
        if(self.tokenizer.keyWord() != key_word):
            raise JackSyntaxError(
                    compile_step = compile_step_name,
                    file_name = self.input_file_name,
                    line_count = self.tokenizer.lineCount(),
                    actual_token = self.tokenizer.current_token,
                    actual_type = token_type_dict[self.tokenizer.tokenType()],
                    expected_token = reverse_keyword_dict[key_word]
                )
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()

    def _isDataTypeCheckVoid(self, compile_step_name):
        current_key_word = self.tokenizer.keyWord()
        if(current_key_word != INT     and 
           current_key_word != BOOLEAN and 
           current_key_word != CHAR    and 
           current_key_word != VOID    and
           self.tokenizer.tokenType() != IDENTIFIER):
            raise JackSyntaxError(
                    compile_step = compile_step_name,
                    file_name = self.input_file_name,
                    line_count = self.tokenizer.lineCount(),
                    actual_token = self.tokenizer.current_token,
                    actual_type = token_type_dict[self.tokenizer.tokenType()],
                    expected_type = "int or boolean or char"
                )
        self.tokenizer.advance()
        return self.tokenizer.current_token

    def _isDataTypeCheck(self, compile_step_name):
        current_key_word = self.tokenizer.keyWord()
        if(current_key_word != INT and current_key_word != BOOLEAN and current_key_word != CHAR and self.tokenizer.tokenType() != IDENTIFIER):
            raise JackSyntaxError(
                    compile_step = compile_step_name,
                    file_name = self.input_file_name,
                    line_count = self.tokenizer.lineCount(),
                    actual_token = self.tokenizer.current_token,
                    actual_type = token_type_dict[self.tokenizer.tokenType()],
                    expected_type = "int or boolean or char"
                )
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()

    def _compileVarGeneral(self, current_symbol_table):
        data_kind = self.tokenizer.current_token
        self.tokenizer.advance()
        data_type = self._isDataTypeCheck("compileVarGeneral")

        name = self._indentifierCheck("compileVarGeneral")

        current_symbol_table.define(name, data_type, kind_dict[data_kind])

        while(self.tokenizer.current_token == ','):
            self.tokenizer.advance()
            name = self._indentifierCheck("compileVarGeneral")
            current_symbol_table.define(name, data_type, kind_dict[data_kind])

    # This should be called with a fresh tokenizer
    def compileClass(self):
        if(not self.tokenizer.hasMoreTokens()):
            print("compileClass called when there were no tokens left")
            return

        self.class_symbol_table.reset()

        self.tokenizer.advance()
        self._keyWordCheck(CLASS, "compileClass")
        
        self._indentifierCheck("compileClass")
        
        self._symbolCheck("{", "compileClass")

        key_word = self.tokenizer.keyWord()
        while(key_word == STATIC or key_word == FIELD):
            self.compileClassVarDec()
            key_word = self.tokenizer.keyWord()

        key_word = self.tokenizer.keyWord()
        while(key_word == CONSTRUCTOR or key_word == FUNCTION or key_word == METHOD):
            self.compileSubroutine()
            key_word = self.tokenizer.keyWord()

        self._symbolCheck("}", "compileClass")

        self.writer.close()
        

    def compileClassVarDec(self):
        # don't need to verify the first token becuase if this the token is either static or field
        #self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        #self.tokenizer.advance()
        
        self._compileVarGeneral(self.class_symbol_table)

        self._symbolCheck(';', "compileClassVarDec")



    def compileSubroutine(self):
        self.class_symbol_table.reset()

        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()

        self._isDataTypeCheckVoid("compileSubroutine")

        self._indentifierCheck("compileSubRoutine")

        self._symbolCheck('(', "compileSubRoutine")

        self.compileParameterList()

        self._symbolCheck(')', "compileSubRoutine")

        self.compileSubroutineBody()



    def compileParameterList(self):
        self._writeTab()
        self.output_file.write("<parameterList>\n")
        self.tab_count += 1

        # Empty parameter list i.e. method void orca()
        if(self.tokenizer.current_token == ')'):
            self.tab_count -= 1
            self._writeTab()
            self.output_file.write("</parameterList>\n")
            return

        self._isDataTypeCheck("compileParameterList")

        self._indentifierCheck("compileParameterList")

        while(self.tokenizer.current_token == ','):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()
            self._isDataTypeCheck("compileParameterList")
            self._indentifierCheck("compileParameterList")

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</parameterList>\n")


    def compileSubroutineBody(self):
        self._writeTab()
        self.output_file.write("<subroutineBody>\n")
        self.tab_count += 1

        self._symbolCheck("{", "compileSubroutineBody")

        while(self.tokenizer.keyWord() == VAR):
            self.compileVarDec()
        
        if(   self.tokenizer.keyWord() !=    LET and
              self.tokenizer.keyWord() !=     IF and
              self.tokenizer.keyWord() !=  WHILE and
              self.tokenizer.keyWord() !=     DO and
              self.tokenizer.keyWord() != RETURN):
            print(f"excpected statement token but instead got {self.tokenizer.current_token}")
            return
        
        self.compileStatements()

        self._symbolCheck('}', "compileSubroutineBody")

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</subroutineBody>\n")


    def compileVarDec(self):
        self._writeTab()
        self.output_file.write("<varDec>\n")
        self.tab_count += 1
        
        self._compileVarGeneral(self.subroutine_symbol_table)

        self._symbolCheck(";", "compileVarDec")

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</varDec>\n")


    def compileStatements(self):
        self._writeTab()
        self.output_file.write("<statements>\n")
        self.tab_count += 1

        while(self.tokenizer.keyWord() ==    LET or
              self.tokenizer.keyWord() ==     IF or
              self.tokenizer.keyWord() ==  WHILE or
              self.tokenizer.keyWord() ==     DO or
              self.tokenizer.keyWord() == RETURN):
            self.statement_method_dict[self.tokenizer.keyWord()]()
        

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</statements>\n")


    def compileLet(self):
        self._writeTab()
        self.output_file.write("<letStatement>\n")
        self.tab_count += 1

        self._keyWordCheck(LET, "compileLet")

        self._indentifierCheck("compileLet")

        # optional array indexing
        if(self.tokenizer.current_token == '['):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()
            
            self.compileExpression()
            
            self._symbolCheck(']', "compileLet")

        self._symbolCheck('=', "compileLet")


        self.compileExpression()

        self._symbolCheck(';', "compileLet")

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</letStatement>\n")


    def compileIf(self):
        self._writeTab()
        self.output_file.write("<ifStatement>\n")
        self.tab_count += 1

        self._keyWordCheck(IF, "compileLet")

        self._symbolCheck('(', "compileIf")

        self.compileExpression()

        self._symbolCheck(')', "compileIf")

        self._symbolCheck('{', "compileIf")

        self.compileStatements()
        
        self._symbolCheck('}', "compileIf")

        #optional else check
        if(self.tokenizer.keyWord() == ELSE):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            self._symbolCheck('{', "compileIf")

            self.compileStatements()
            
            self._symbolCheck('}', "compileIf")



        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</ifStatement>\n")
        

    def compileWhile(self):
        self._writeTab()
        self.output_file.write("<whileStatement>\n")
        self.tab_count += 1

        self._keyWordCheck(WHILE, "compileWhile")

        self._symbolCheck('(', "compileWhile")

        self.compileExpression()

        self._symbolCheck(')', "compileWhile")

        self._symbolCheck('{', "compileWhile")

        self.compileStatements()
        
        self._symbolCheck('}', "compileWhile")


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</whileStatement>\n")


    def compileDo(self):
        self._writeTab()
        self.output_file.write("<doStatement>\n")
        self.tab_count += 1

        self._keyWordCheck(DO, "compileDo")

        self._indentifierCheck("compileDo")

        if(self.tokenizer.current_token == '.'):
            self._symbolCheck('.', "compileDo")
            self._indentifierCheck("compileDo")


        elif(self.tokenizer.current_token != '('):
            raise JackSyntaxError(
                    compile_step = "compileDo",
                    file_name = self.input_file_name,
                    line_count = self.tokenizer.lineCount(),
                    actual_token = self.tokenizer.current_token,
                    actual_type = token_type_dict[self.tokenizer.tokenType()],
                    expected_token = "( or ."
                )


        self._symbolCheck('(', "compileDo")
        self.compileExpressionList()
        self._symbolCheck(')', "compileDo")


        self._symbolCheck(';', "compileDo")

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</doStatement>\n")


    def compileReturn(self):
        self._writeTab()
        self.output_file.write("<returnStatement>\n")
        self.tab_count += 1

        self._keyWordCheck(RETURN, "compileReturn")

        if(self.tokenizer.current_token != ';'):
            self.compileExpression()

        self._symbolCheck(';', "compileReturn")

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</returnStatement>\n")


    def compileExpression(self):
        self._writeTab()
        self.output_file.write("<expression>\n")
        self.tab_count += 1

        self.compileTerm()

        while(self.tokenizer.current_token in operator_set):
            op = self.tokenizer.current_token
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()
            
            self.compileTerm()
            self.writer.writeArithmetic(symbol_to_command_dict[op])
            
        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</expression>\n")


    def compileTerm(self):
        self._writeTab()
        self.output_file.write("<term>\n")
        self.tab_count += 1

        peek_token, peek_type, peek_key_word = self.tokenizer.peek()

        if(self.tokenizer.tokenType() == INT_CONST):
            self.writer.writePush(CONSTANT_SEG, int(self.tokenizer.current_token))
            self.tokenizer.advance()

        elif(self.tokenizer.tokenType() == STRING_CONST):
            # Pushing str_len arg for String.New
            self.writer.writePush(CONSTANT_SEG, len(self.tokenizer.current_token))
            # Calling OS String constructor
            self.writer.writeCall("String.new", 1)

            for char in self.tokenizer.current_token:
                # ord is an ascii cast
                self.writer.writePush(CONSTANT_SEG, ord(char))
                self.writer.writeCall("String.appendChar", 1)


            self.tokenizer.advance()

        elif(self.tokenizer.tokenType() == STRING_CONST          or
             self.tokenizer.keyWord() in keyword_const_set or
            (self.tokenizer.tokenType() == IDENTIFIER and peek_token != '[' and peek_token != '.' and peek_token != '(')):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

        elif(self.tokenizer.current_token in unaryOp_set):
            unaryOp = self.tokenizer.current_token
            self.tokenizer.advance()
            
            self.compileTerm()
            self.writer.writeArithmetic(symbol_to_unary_command_dict[unaryOp])

        # Indexing into array
        elif(self.tokenizer.tokenType() == IDENTIFIER and peek_token == '['):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            self._writeTag(token_type_dict[peek_type], peek_token)
            self.tokenizer.advance()

            self.compileExpression()

            self._symbolCheck(']', "compileTerm")

        elif(self.tokenizer.current_token == '('):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()
            
            #self.compileExpressionList()
            self.compileExpression()

            self._symbolCheck(')', "compileTerm")

        # Calling function
        elif(self.tokenizer.tokenType() == IDENTIFIER and peek_token == '('):
            function_name = self.tokenizer.current_token
            self.tokenizer.advance()

            # Moving past '('
            self.tokenizer.advance()

            arg_count = self.compileExpressionList()

            self.writer.writeCall(function_name, arg_count)

            self._symbolCheck(')', "compileTerm")
            

        # Calling method
        elif(self.tokenizer.tokenType() == IDENTIFIER and peek_token == '.'):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            self._writeTag(token_type_dict[peek_type], peek_token)
            self.tokenizer.advance()
            #print(self.tokenizer.current_token)

            self._indentifierCheck("compileTerm")

            self._symbolCheck('(', "compileTerm")

            self.compileExpressionList()

            self._symbolCheck(')', "compileTerm")

        else:
            print("oof")


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</term>\n")


    def compileExpressionList(self)->int:
        arg_count = 0

        if(self.tokenizer.current_token == ')'):
            return arg_count

        arg_count += 1
        self.compileExpression()
        while(self.tokenizer.current_token == ','):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            arg_count += 1
            self.compileExpression()

        return arg_count
