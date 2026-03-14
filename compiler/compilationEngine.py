import copy

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

from syntaxException import JackSyntaxError

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
    def __init__(self, tokenizer : Tokenizer, input_file_name : str):
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
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()

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
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
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
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()

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

    def _compileVarGeneral(self):
        self._isDataTypeCheck("compileVarGeneral")

        self._indentifierCheck("compileVarGeneral")

        while(self.tokenizer.current_token == ','):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()
            self._indentifierCheck("compileVarGeneral")

    # This should be called with a fresh tokenizer
    def compileClass(self):
        if(not self.tokenizer.hasMoreTokens()):
            print("compileClass called when there were no tokens left")
            return
        self.output_file.write("<class>\n")
        self.tab_count += 1

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

        self.tab_count -= 1
        self.output_file.write("</class>")
        self.output_file.write('\n')
        self.output_file.close()
        

    def compileClassVarDec(self):
        self._writeTab()
        self.output_file.write("<classVarDec>\n")
        self.tab_count += 1

        # don't need to verify the first token becuase if this the token is either static or field
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()
        
        self._compileVarGeneral()

        self._symbolCheck(';', "compileClassVarDec")

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</classVarDec>\n")


    def compileSubroutine(self):
        self._writeTab()
        self.output_file.write("<subroutineDec>\n")
        self.tab_count += 1

        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()

        self._isDataTypeCheckVoid("compileSubroutine")

        self._indentifierCheck("compileSubRoutine")

        self._symbolCheck('(', "compileSubRoutine")

        self.compileParameterList()

        self._symbolCheck(')', "compileSubRoutine")

        self.compileSubroutineBody()

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</subroutineDec>\n")


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
        
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        self.tokenizer.advance()
        
        self._compileVarGeneral()

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

        # optional expression to return
        # todo make it optional
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
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()
            
            self.compileTerm()
            
        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</expression>\n")


    def compileTerm(self):
        self._writeTab()
        self.output_file.write("<term>\n")
        self.tab_count += 1

        # This is probably pretty slow
        # I should probably create a peek method
        # But that sounds annoying
        tokenizer_copy = copy.deepcopy(self.tokenizer)
        # this is the one instruction that is not LL(1), requring to look ahead 1 token to determine the type of term
        prev_token = self.tokenizer.current_token
        prev_type = self.tokenizer.tokenType()
        prev_key_word = self.tokenizer.keyWord()
        self.tokenizer.advance()

        if(prev_type == INT_CONST             or 
           prev_type == STRING_CONST          or
           prev_key_word in keyword_const_set or
           (prev_type == IDENTIFIER and self.tokenizer.current_token != '[' and self.tokenizer.current_token != '.' and self.tokenizer.current_token != '(')):
            self._writeTag(token_type_dict[prev_type], prev_token)

        elif(prev_token in unaryOp_set):
            self._writeTag(token_type_dict[prev_type], prev_token)
            
            self.compileTerm()

        # Indexing into array
        elif(prev_type == IDENTIFIER and self.tokenizer.current_token == '['):
            self._writeTag(token_type_dict[prev_type], prev_token)

            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            self.compileExpression()

            self._symbolCheck(']', "compileTerm")

        elif(prev_token == '('):
            self._writeTag(token_type_dict[prev_type], prev_token)
            
            #self.compileExpressionList()
            self.compileExpression()

            self._symbolCheck(')', "compileTerm")

        # Calling function
        elif(prev_type == IDENTIFIER and self.tokenizer.current_token == '('):
            self._writeTag(token_type_dict[prev_type], prev_token)

            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            self.compileExpressionList()

            self._symbolCheck(')', "compileTerm")
            

        # Calling method
        elif(prev_type == IDENTIFIER and self.tokenizer.current_token == '.'):
            self._writeTag(token_type_dict[prev_type], prev_token)

            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            self._indentifierCheck("compileTerm")

            self._symbolCheck('(', "compileTerm")

            self.compileExpressionList()

            self._symbolCheck(')', "compileTerm")

        # If there is no valid term I don't want to advance forward one
        else:
            self.tokenizer = tokenizer_copy

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</term>\n")


    def compileExpressionList(self):
        self._writeTab()
        self.output_file.write("<expressionList>\n")
        self.tab_count += 1
        
        if(self.tokenizer.current_token == ')'):
            self.tab_count -= 1
            self._writeTab()
            self.output_file.write("</expressionList>\n")
            return

        self.compileExpression()
        while(self.tokenizer.current_token == ','):
            self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
            self.tokenizer.advance()

            self.compileExpression()


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</expressionList>\n")

