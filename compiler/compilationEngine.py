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

from VMWriter import VMWriter
from VMWriter import segment_dict 
from VMWriter import POINTER_SEG
from VMWriter import CONSTANT_SEG
from VMWriter import STATIC_SEG
from VMWriter import THIS_SEG
from VMWriter import THAT_SEG
from VMWriter import ARGUMENT_SEG
from VMWriter import LOCAL_SEG
from VMWriter import TEMP_SEG
from VMWriter import ADD
from VMWriter import SUB
from VMWriter import NEG
from VMWriter import EQ
from VMWriter import GT
from VMWriter import LT
from VMWriter import AND
from VMWriter import OR
from VMWriter import NOT
from VMWriter import MULT
from VMWriter import DIV

from symbolTable import SymbolTable
from symbolTable import STATIC_KIND
from symbolTable import FIELD_KIND
from symbolTable import ARG_KIND
from symbolTable import VAR_KIND

from syntaxException import JackSyntaxError
from referenceException import JackReferenceError

kind_to_seg_dict = {
    STATIC_KIND : STATIC_SEG,
    FIELD_KIND : THIS_SEG,
    ARG_KIND : ARGUMENT_SEG,
    VAR_KIND : LOCAL_SEG
}

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
    '|' : OR,
    '*' : MULT,
    '/' : DIV
}


kind_dict = {
    "static" : STATIC_KIND,
    "field" : FIELD_KIND,
    "arg" : ARG_KIND,
    "var" : VAR_KIND
}



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
        self.label_counter = 0


    def _whichSymbolTable(self, token, error = True):
        if(self.subroutine_symbol_table.isIn(token)):
            return self.subroutine_symbol_table
        elif(self.class_symbol_table.isIn(token)):
            return self.class_symbol_table
        elif(error):
            raise JackReferenceError(token, self.tokenizer.lineCount(), self.subroutine_symbol_table, self.class_symbol_table)


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
        current_token = self.tokenizer.current_token
        self.tokenizer.advance()
        return current_token

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
        current_token = self.tokenizer.current_token
        self.tokenizer.advance()
        return current_token

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
        current_token = self.tokenizer.current_token
        self.tokenizer.advance()
        return current_token

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
        self._compileVarGeneral(self.class_symbol_table)

        self._symbolCheck(';', "compileClassVarDec")



    def compileSubroutine(self):
        self.subroutine_symbol_table.reset()

        key_word = self.tokenizer.keyWord()
        # ARGUMENT_SEG 0 is reserved for the this pointer in methods 
        if(key_word == METHOD):
            self.subroutine_symbol_table.define("", "", ARG_KIND)
        self.tokenizer.advance()

        self._isDataTypeCheckVoid("compileSubroutine")

        function_name = self._indentifierCheck("compileSubRoutine")
        full_function_name = f"{self.input_file_name.replace(".jack", "")}.{function_name}"


        self._symbolCheck('(', "compileSubRoutine")

        self.compileParameterList()

        self._symbolCheck(')', "compileSubRoutine")
        
        # Moved this out of compileSubroutineBody to get var count for the function call write
        self._symbolCheck("{", "compileSubroutineBody")

        while(self.tokenizer.keyWord() == VAR):
            self.compileVarDec()
        
        nVars = self.subroutine_symbol_table.varCount(VAR_KIND)
        self.writer.writeFunction(full_function_name, nVars)

        if(key_word == CONSTRUCTOR):
            object_size = self.class_symbol_table.varCount(FIELD_KIND)
            self.writer.writePush(CONSTANT_SEG, object_size)
            self.writer.writeCall("Memory.alloc", 1)
            self.writer.writePop(POINTER_SEG, 0)

        elif(key_word == METHOD):
            # grabing the pointer to this
            self.writer.writePush(ARGUMENT_SEG, 0)
            # putting the pointer to this in pointer 0
            self.writer.writePop(POINTER_SEG, 0)

        self.compileSubroutineBody()



    def compileParameterList(self):
        # Empty parameter list i.e. method void orca()
        if(self.tokenizer.current_token == ')'):
            return 0

        data_type = self._isDataTypeCheck("compileParameterList")

        name = self._indentifierCheck("compileParameterList")

        nVars = 1
        self.subroutine_symbol_table.define(name, data_type, ARG_KIND)

        while(self.tokenizer.current_token == ','):
            self.tokenizer.advance()
            data_type = self._isDataTypeCheck("compileParameterList")
            name = self._indentifierCheck("compileParameterList")
            self.subroutine_symbol_table.define(name, data_type, ARG_KIND)
            nVars += 1

        return nVars


    def compileSubroutineBody(self):
        if(   self.tokenizer.keyWord() !=    LET and
              self.tokenizer.keyWord() !=     IF and
              self.tokenizer.keyWord() !=  WHILE and
              self.tokenizer.keyWord() !=     DO and
              self.tokenizer.keyWord() != RETURN):
            print(f"excpected statement token but instead got {self.tokenizer.current_token}")
            return
        
        self.compileStatements()

        self._symbolCheck('}', "compileSubroutineBody")


    def compileVarDec(self):
        self._compileVarGeneral(self.subroutine_symbol_table)

        self._symbolCheck(";", "compileVarDec")


    def compileStatements(self):
        while(self.tokenizer.keyWord() ==    LET or
              self.tokenizer.keyWord() ==     IF or
              self.tokenizer.keyWord() ==  WHILE or
              self.tokenizer.keyWord() ==     DO or
              self.tokenizer.keyWord() == RETURN):
            self.statement_method_dict[self.tokenizer.keyWord()]()
        


    def compileLet(self):
        self._keyWordCheck(LET, "compileLet")

        var_name = self.tokenizer.current_token
        symbol_table = self._whichSymbolTable(var_name)
        segment = kind_to_seg_dict[symbol_table.kindOf(var_name)]
        index = symbol_table.indexOf(var_name)
        self.tokenizer.advance()

        # optional array indexing
        if(self.tokenizer.current_token == '['):
            self.tokenizer.advance()
            symbol_table = self._whichSymbolTable(var_name)
            segment = kind_to_seg_dict[symbol_table.kindOf(var_name)]
            index = symbol_table.indexOf(var_name)
            self.writer.writePush(segment, index)
            
            self.compileExpression()

            self.writer.writeArithmetic(ADD)
            
            self._symbolCheck(']', "compileLet")
            self._symbolCheck('=', "compileLet")


            self.compileExpression()

            self._symbolCheck(';', "compileLet")
            self.writer.writePop(POINTER_SEG, 1)
            self.writer.writePop(TEMP_SEG, 0)
            self.writer.writePop(THAT_SEG, 0)

        else:
            self._symbolCheck('=', "compileLet")


            self.compileExpression()

            self._symbolCheck(';', "compileLet")
            self.writer.writePop(segment, index)



    def compileIf(self):
        self._keyWordCheck(IF, "compileLet")

        self._symbolCheck('(', "compileIf")

        self.compileExpression()

        self._symbolCheck(')', "compileIf")

        self._symbolCheck('{', "compileIf")

        self.writer.writeArithmetic(NOT)
        self.writer.writeIf(f"L{self.label_counter}")

        self.compileStatements()
        
        self._symbolCheck('}', "compileIf")

        self.writer.writeLabel(f"L{self.label_counter}")
        self.label_counter += 1

        #optional else check
        if(self.tokenizer.keyWord() == ELSE):
            self.tokenizer.advance()

            self._symbolCheck('{', "compileIf")

            self.compileStatements()
            
            self._symbolCheck('}', "compileIf")

        self.writer.writeLabel(f"L{self.label_counter}")
        self.label_counter += 1

        

    def compileWhile(self):
        self._keyWordCheck(WHILE, "compileWhile")

        self._symbolCheck('(', "compileWhile")

        self.writer.writeLabel(f"L{self.label_counter}")

        self.compileExpression()

        self._symbolCheck(')', "compileWhile")

        self._symbolCheck('{', "compileWhile")

        self.writer.writeArithmetic(NOT)
        self.writer.writeIf(f"L{self.label_counter + 1}")

        self.compileStatements()
        
        self._symbolCheck('}', "compileWhile")

        self.writer.writeGoto(f"L{self.label_counter}")
        self.label_counter += 1
        self.writer.writeLabel(f"L{self.label_counter}")



    def compileDo(self):
        self._keyWordCheck(DO, "compileDo")

        first_token = self.tokenizer.current_token
        self._indentifierCheck("compileDo")

        nArgs = 0
        if(self.tokenizer.current_token == '.'):
            # Pushing pointer to obj as 0th arg
            if(self.subroutine_symbol_table.isIn(first_token) or self.subroutine_symbol_table.isIn(first_token)):
                symbol_table = self._whichSymbolTable(first_token)
                segment = kind_to_seg_dict[symbol_table.kindOf(first_token)]
                index = symbol_table.indexOf(first_token)
                self.writer.writePush(segment, index)
                nArgs += 1
                first_token = symbol_table.typeOf(first_token)
                self._symbolCheck('.', "compileDo")
                second_token = self._indentifierCheck("compileDo")
                function_name = f"{first_token}.{second_token}"
            else:
                self._symbolCheck('.', "compileDo")
                second_token = self._indentifierCheck("compileDo")
                function_name = f"{first_token}.{second_token}"


        elif(self.tokenizer.current_token != '('):
            raise JackSyntaxError(
                    compile_step = "compileDo",
                    file_name = self.input_file_name,
                    line_count = self.tokenizer.lineCount(),
                    actual_token = self.tokenizer.current_token,
                    actual_type = token_type_dict[self.tokenizer.tokenType()],
                    expected_token = "( or ."
                )
        else:
            function_name = f"{self.input_file_name.replace(".jack", "")}.{first_token}"
        
        self._symbolCheck('(', "compileDo")
        nArgs += self.compileExpressionList()
        self._symbolCheck(')', "compileDo")


        self._symbolCheck(';', "compileDo")
        self.writer.writeCall(function_name, nArgs)
        self.writer.writePop(TEMP_SEG, 0)



    def compileReturn(self):
        self._keyWordCheck(RETURN, "compileReturn")

        if(self.tokenizer.current_token != ';'):
            self.compileExpression()
        else:
            self.writer.writePush(CONSTANT_SEG, 0)

        self._symbolCheck(';', "compileReturn")
        self.writer.writeReturn()


    def compileExpression(self):
        self.compileTerm()

        while(self.tokenizer.current_token in operator_set):
            op = self.tokenizer.current_token
            self.tokenizer.advance()
            
            self.compileTerm()
            self.writer.writeArithmetic(symbol_to_command_dict[op])
            

    def compileTerm(self):
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
                self.writer.writeCall("String.appendChar", 2)


            self.tokenizer.advance()

        elif(self.tokenizer.keyWord() in keyword_const_set):
            if(self.tokenizer.keyWord() == NULL or self.tokenizer.keyWord() == FALSE):
                self.writer.writePush(CONSTANT_SEG, 0)
            elif(self.tokenizer.keyWord() == TRUE):
                self.writer.writePush(CONSTANT_SEG, 1)
                self.writer.writeArithmetic(NEG)
            elif(self.tokenizer.keyWord() == THIS):
                self.writer.writePush(POINTER_SEG, 0)
            
            self.tokenizer.advance()

        elif((self.tokenizer.tokenType() == IDENTIFIER and peek_token != '[' and peek_token != '.' and peek_token != '(')):
            current_token = self.tokenizer.current_token
            symbol_table = self._whichSymbolTable(current_token)
            
            segment = kind_to_seg_dict[symbol_table.kindOf(current_token)]
            index = symbol_table.indexOf(current_token)
            self.writer.writePush(segment, index)
                
            self.tokenizer.advance()

        elif(self.tokenizer.current_token in unaryOp_set):
            unaryOp = self.tokenizer.current_token
            self.tokenizer.advance()
            
            self.compileTerm()
            self.writer.writeArithmetic(symbol_to_unary_command_dict[unaryOp])

        # Indexing into array
        elif(self.tokenizer.tokenType() == IDENTIFIER and peek_token == '['):
            current_token = self.tokenizer.current_token
            symbol_table = self._whichSymbolTable(current_token)
            segment = kind_to_seg_dict[symbol_table.kindOf(current_token)]
            index = symbol_table.indexOf(current_token)
            self.writer.writePush(segment, index)
            self.tokenizer.advance()

            # Moving past '['
            self.tokenizer.advance()

            self.compileExpression()

            self._symbolCheck(']', "compileTerm")
            
            self.writer.writeArithmetic(ADD)
            self.writer.writePop(POINTER_SEG, 1)
            self.writer.writePush(THAT_SEG, 0)

        elif(self.tokenizer.current_token == '('):
            self.tokenizer.advance()
            
            #self.compileExpressionList()
            self.compileExpression()

            self._symbolCheck(')', "compileTerm")

        # Calling self method
        elif(self.tokenizer.tokenType() == IDENTIFIER and peek_token == '('):
            function_name = f"{self.input_file_name.replace(".jack", "")}.{self.tokenizer.current_token}"
            self.tokenizer.advance()

            # Moving past '('
            self.tokenizer.advance()

            self.writer.writePush(POINTER_SEG, 0)
            arg_count = self.compileExpressionList()

            self.writer.writeCall(function_name, arg_count + 1)

            self._symbolCheck(')', "compileTerm")
            

        # Calling method or function from different file
        elif(self.tokenizer.tokenType() == IDENTIFIER and peek_token == '.'):
            nArgs = 0
            # first_tonken.second_token()
            first_token = self.tokenizer.current_token
            self.tokenizer.advance()
            # Move past .
            self.tokenizer.advance()
            second_token = self.tokenizer.current_token 

            # Is not a method call
            if(not (self.subroutine_symbol_table.isIn(first_token) or self.class_symbol_table.isIn(first_token))):
                function_name = f"{first_token}.{second_token}"
            # Is method call
            else:
                symbol_table = self._whichSymbolTable(first_token)
                segment = kind_to_seg_dict[symbol_table.kindOf(first_token)]
                index = symbol_table.indexOf(first_token)
                object_type = symbol_table.typeOf(first_token)
                self.writer.writePush(segment, index)
                function_name = f"{object_type}.{second_token}"
                nArgs += 1
                

            #self.tokenizer.advance()

            self._indentifierCheck("compileTerm")

            self._symbolCheck('(', "compileTerm")

            nArgs += self.compileExpressionList()

            self._symbolCheck(')', "compileTerm")

            self.writer.writeCall(function_name, nArgs)

        else:
            print("oof")


    def compileExpressionList(self)->int:
        arg_count = 0

        if(self.tokenizer.current_token == ')'):
            return arg_count

        arg_count += 1
        self.compileExpression()
        while(self.tokenizer.current_token == ','):
            self.tokenizer.advance()

            arg_count += 1
            self.compileExpression()

        return arg_count
