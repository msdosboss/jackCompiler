import sys
import os.path

from codeWriter import CodeWriter
from parser import Parse

from parser import C_PUSH
from parser import C_POP
from parser import C_ARITHMETIC


if (__name__ == "__main__"):
    file_name = ""
    if (len(sys.argv) < 2):
        file_name = "orca.vm"
    else:
        if (os.path.exists(sys.argv[1])):
            file_name = sys.argv[1]
        else:
            file_name = "orca.vm"
            print(f"{sys.argv[1]} does not exist, using {file_name}")

    parser = Parse(file_name)
    code_writer = CodeWriter(file_name.replace(".vm", ".asm"))

    while (parser.hasMoreLines()):
        parser.advance()
        if (parser.instruction_type == C_ARITHMETIC):
            code_writer.writeArithmetic(parser.getArgOne())

        elif (parser.instruction_type == C_PUSH or parser.instruction_type == C_POP):
            code_writer.writePushPop(parser.instruction_type, parser.getArgOne(), parser.getArgTwo())

    code_writer.close()

