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
    file_names = []
    if (len(sys.argv) < 2):
        file_names.append("orca.vm")
    else:
        if (os.path.exists(sys.argv[1])):
            file_name = sys.argv[1]
            if(".jack" in file_name):
                file_names.append(file_name)
            else:
                file_names = os.listdir(file_name)
                # Remove all non VM files
                file_names = [file for file in file_names if ".vm" in file]
                for i, _ in enumerate(file_names):
                    # Windows is going to make this break because it would need a \
                    file_names[i] = file_name + '/' + file_names[i]
        else:
            file_names.append("orca.vm")
            print(f"{sys.argv[1]} does not exist, using {file_name}")

    code_writer = CodeWriter(f"{sys.argv[1].replace("/", "")}/out.asm")

    code_writer.writeInit()

    for file_name in file_names:
        parser = Parse(file_name)
        code_writer.setFileName(file_name)
 
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

            elif (parser.instruction_type == C_FUNCTION):
                code_writer.writeFunction(parser.getArgOne(), parser.getArgTwo())

            elif (parser.instruction_type == C_CALL):
                code_writer.writeCall(parser.getArgOne(), parser.getArgTwo())

            elif (parser.instruction_type == C_RETURN):
                code_writer.writeReturn()

    code_writer.close()

