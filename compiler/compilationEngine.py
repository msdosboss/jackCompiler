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
from tokenizer import keyword_dict

reverse_keyword_dict = {value: key for key, value in keyword_dict.items()}

token_type_dict = {
    -1 : "invalid",
    KEYWORD : "keyword",
    SYMBOL : "symbol",
    IDENTIFIER : "identifier",
    INT_CONST : "integerConstant",
    STRING_CONST : "stringConstant"
}

class CompilationEngine:
    def __init__(self, tokenizer : Tokenizer, output_file_name : str):
        self.tokenizer = tokenizer
        self.output_file = open(output_file_name, "w")
        self.tab_count = 0


    def _writeTab(self):
        for _ in range(self.tab_count):
            self.output_file.write("  ")


    def _writeTag(self, tag : str, token : str):
        self._writeTab()
        self.output_file.write(f"<{tag}> {token} </{tag}>" + "\n")


    def _printError(self, excpected : str, got : str):
        print(f"failed to parse program excpected {excpected}, got {got}")


    # This should be called with a fresh tokenizer
    def compileClass(self):
        if(not self.tokenizer.hasMoreTokens()):
            print("compileClass called when there were no tokens left")
            return

        self.tokenizer.advance()
        if(self.tokenizer.keyWord() != CLASS):
            self._printError("class", self.tokenizer.current_token)
            return

        self.output_file.write("<class>\n")
        self.tab_count += 1
        
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)
        
        self.tokenizer.advance()
        if(self.tokenizer.tokenType() != IDENTIFIER):
            self._printError(token_type_dict[IDENTIFIER], token_type_dict[self.tokenizer.tokenType()])
            return
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)

        self.tokenizer.advance()
        if(self.tokenizer.current_token != '{'):
            self._printError('{', self.tokenizer.current_token)
            return
        self._writeTag(token_type_dict[self.tokenizer.tokenType()], self.tokenizer.current_token)

        self.tokenizer.advance()
        key_word = self.tokenizer.keyWord()
        while(key_word == STATIC or key_word == FIELD):
            self.compileClassVarDec()
            key_word = self.tokenizer.keyWord()

        key_word = self.tokenizer.keyWord()
        while(key_word == CONSTRUCTOR or key_word == FUNCTION or key_word == METHOD):
            self.compileSubroutine()
            key_word = self.tokenizer.keyWord()

        self.tab_count -= 1
        self.output_file.write("</class>")
        self.output_file.close()
        

        
    def compileClassVarDec(self):
        self._writeTab()
        self.output_file.write("<classVarDec>\n")
        self.tab_count += 1

        self.tokenizer.advance()

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</classVarDec>\n")


    def compileSubroutine(self):
        self._writeTab()
        self.output_file.write("<subroutineDec>\n")
        self.tab_count += 1

        self.tokenizer.advance()

        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</subroutineDec>\n")

    def compileParameterList(self):
        self._writeTab()
        self.output_file.write("<parameterList>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</parameterList>\n")

    def compileSubroutineBody(self):
        self._writeTab()
        self.output_file.write("<subroutineBody>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</subroutineBody>\n")

    def compileVarDec(self):
        self._writeTab()
        self.output_file.write("<varDec>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</varDec>\n")

    def compileStatements(self):
        self._writeTab()
        self.output_file.write("<statements>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</statements>\n")

    def compileLet(self):
        self._writeTab()
        self.output_file.write("<letStatement>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</letStatement>\n")

    def compileIf(self):
        self._writeTab()
        self.output_file.write("<ifStatement>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</ifStatement>\n")

    def compileWhile(self):
        self._writeTab()
        self.output_file.write("<whileStatement>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</whileStatement>\n")

    def compileDo(self):
        self._writeTab()
        self.output_file.write("<doStatement>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</doStatement>\n")

    def compileReturn(self):
        self._writeTab()
        self.output_file.write("<returnStatement>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</returnStatement>\n")

    def compileExpression(self):
        self._writeTab()
        self.output_file.write("<expression>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</expression>\n")

    def compileTerm(self):
        self._writeTab()
        self.output_file.write("<term>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</term>\n")

    def compileExpressionList(self):
        self._writeTab()
        self.output_file.write("<expressionList>\n")
        self.tab_count += 1


        self.tab_count -= 1
        self._writeTab()
        self.output_file.write("</expressionList>\n")

