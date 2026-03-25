from tokenizer import Tokenizer
from compilationEngine import CompilationEngine
from syntaxException import JackSyntaxError
from symbolTable import SymbolTable
from VMWriter import VMWriter
import sys 
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("provide file name")
        exit()

    class_symbol_table = SymbolTable()
    subroutine_symbol_table = SymbolTable()
    writer = VMWriter(sys.argv[1])
    tokenizer = Tokenizer(sys.argv[1])
    compilationEngine = CompilationEngine(tokenizer, sys.argv[1], class_symbol_table, subroutine_symbol_table, writer)
    try:
        compilationEngine.compileClass()
    except JackSyntaxError as e:
        print(e)
