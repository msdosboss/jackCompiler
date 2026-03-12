from tokenizer import Tokenizer
from compilationEngine import CompilationEngine
from syntaxException import JackSyntaxError
import sys 
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("provide file name")
        exit()

    tokenizer = Tokenizer(sys.argv[1])
    compilationEngine = CompilationEngine(tokenizer, sys.argv[1])
    try:
        compilationEngine.compileClass()
    except JackSyntaxError as e:
        print(e)
