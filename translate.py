import sys
import os.path

from codeWriter import CodeWriter
from parser import Parse

from parser import C_PUSH
from parser import C_POP
from parser import C_ARITHMETIC
from parser import C_LABEL
from parser import C_GOTO
from parser import C_IF
from parser import C_FUNCTION
from parser import C_RETURN
from parser import C_CALL


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

    code_writer.writeInit()

    while (parser.hasMoreLines()):
        parser.advance()
        if (parser.instruction_type == C_ARITHMETIC):
            code_writer.writeArithmetic(parser.getArgOne())

        elif (parser.instruction_type == C_PUSH or parser.instruction_type == C_POP):
            code_writer.writePushPop(parser.instruction_type, parser.getArgOne(), parser.getArgTwo())

        elif (parser.instruction_type == C_LABEL):
            code_writer.writeLabel(parser.getArgOne())

        elif (parser.instruction_type == C_GOTO):
            code_writer.writeGoto(parser.getArgOne())

        elif (parser.instruction_type == C_IF):
            code_writer.writeIf(parser.getArgOne())

    code_writer.close()

