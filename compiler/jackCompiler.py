from tokenizer import Tokenizer
from compilationEngine import CompilationEngine
from syntaxException import JackSyntaxError
from referenceException import JackReferenceError
from symbolTable import SymbolTable
from VMWriter import VMWriter
import sys 
import os.path

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("provide file name")
        exit()

    file_names = []
    if(".jack" not in sys.argv[1]):
        if(not os.path.exists(sys.argv[1])):
            print(f"{sys.argv[1]} is not in dir")
            exit()
        folder_name = sys.argv[1]
        file_names = os.listdir(folder_name)
        file_names: list[str] = [file for file in file_names if ".jack" in file]
        for i, _ in enumerate(file_names):
            file_names[i] = f"{folder_name}/{file_names[i]}"
        

    else:
        file_names.append(sys.argv[1])
        
    for file_name in file_names:
        class_symbol_table = SymbolTable()
        subroutine_symbol_table = SymbolTable()
        writer = VMWriter(file_name)
        tokenizer = Tokenizer(file_name)
        compilationEngine = CompilationEngine(tokenizer, file_name, class_symbol_table, subroutine_symbol_table, writer)
        try:
            compilationEngine.compileClass()
        except JackSyntaxError as e:
            print(e)
        except JackReferenceError as e:
            print(e)
