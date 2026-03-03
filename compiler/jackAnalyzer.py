from tokenizer import Tokenizer
from compilationEngine import CompilationEngine
import sys 
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("provide file name")
        exit()

    tokenizer = Tokenizer(sys.argv[1])
    compilationEngine = CompilationEngine(tokenizer, sys.argv[1].replace(".jack", ".xml"))
    compilationEngine.compileClass()
