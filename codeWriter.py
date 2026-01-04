import copy

from parser import C_PUSH
from parser import C_POP

SEGMENT_TO_ASSMBLE = {
    "local" : "@LCL",
    "argument" : "@ARG",
    "this" : "@THAT",
    "that" : "@THAT",
    "static" : "@16"
}


ARITHMETIC_TRANSLATIONS = {
    "add" : [
                "@SP",
                "AM=M-1",
                "D=M",
                "@SP",
                "AM=M-1",
                "M=D+M",
                "@SP",
                "M=M+1"
            ],
    "sub" : [
                "@SP",
                "AM=M-1",
                "D=M",
                "@SP",
                "AM=M-1",
                "M=D-M",
                "@SP",
                "M=M+1"
            ],
    "neg" : [
                "@SP",
                "AM=M-1",
                "-M",
                "@SP",
                "M=M+1"
            ],
    "eq" :  [
                "@SP",
                "AM=M-1",
                "D=M",
                "@SP",
                "AM=M-1",
                "D=D-M",
                "@TRUE",
                "D;JEQ",
                "(FALSE)",
                "@0",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@END",
                "0;JMP",
                "(TRUE)",
                "@1",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "(END)",
                "@SP",
                "M=M+1"
            ],
    "gt" :  [
                "@SP",
                "AM=M-1",
                "D=M",
                "@SP",
                "AM=M-1",
                "D=D-M",
                "@TRUE",
                "D;JGE",
                "(FALSE)",
                "@0",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@END",
                "0;JMP",
                "(TRUE)",
                "@1",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "(END)",
                "@SP",
                "M=M+1"
            ],
    "lt" :  [
                "@SP",
                "AM=M-1",
                "D=M",
                "@SP",
                "AM=M-1",
                "D=D-M",
                "@TRUE",
                "D;JLT",
                "(FALSE)",
                "@0",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@END",
                "0;JMP",
                "(TRUE)",
                "@1",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "(END)",
                "@SP",
                "M=M+1"
            ],
    "and" : [
                "@SP",
                "AM=M-1",
                "D=M",
                "@SP",
                "AM=M-1",
                "M=D&M",
                "@SP",
                "M=M+1"
            ],
    "or" : [
                "@SP",
                "AM=M-1",
                "D=M",
                "@SP",
                "AM=M-1",
                "M=D|M",
                "@SP",
                "M=M+1"
            ],
    "not" : [
                "@SP",
                "AM=M-1",
                "!M",
                "@SP",
                "M=M+1"
            ],
}


class CodeWriter:
    def __init__(self, file_name : str = "vm.out"):
        self.file = open(file_name, "w")
        self.write_count = 0

    def _writeInstructions(self, instructions : list[str]):
        for instruction in instructions:
            self.file.write(instruction + '\n')
            self.write_count += 1

    def writeArithmetic(self, operation : str):
        instructions = ARITHMETIC_TRANSLATIONS[operation]
        if (operation == "lt" or operation == "gt" or operation == "eq"):
            instructions = copy.deepcopy(instructions)
            # making labels unique
            for i, _ in enumerate(instructions):
                if (instructions[i] == "(TRUE)"):
                    instructions[i] = instructions[i].replace("TRUE", f"TRUE{int(self.write_count)}")
                elif (instructions[i] == "(FALSE)"):
                    instructions[i] = instructions[i].replace("FALSE", f"FALSE{int(self.write_count)}")
                elif (instructions[i] == "(END)"):
                    instructions[i] = instructions[i].replace("END", f"END{int(self.write_count)}")

        self._writeInstructions(instructions)

    def writePushPop(self, command_type : int, segment : str, index : int):
        instructions = []
        if (command_type == C_PUSH):
            if (segment == "constant"):
                constant_instructions = [
                    f"@{index}",
                    "D=A"
                ] 

                instructions += constant_instructions

            else:
                instructions.append(SEGMENT_TO_ASSMBLE[segment])

                index_instructions = [
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M"
                ] 

                instructions += index_instructions

            push_instructions = [
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]

            instructions += push_instructions

        else:
            if (segment == "constant"):
                constant_instructions = [
                    f"@{index}",
                    "D=A",
                    "@R13",
                    "M=D"
                ]
                instructions += constant_instructions

            else:
                instructions.append(SEGMENT_TO_ASSMBLE[segment])
                index_instructions = [
                    "D=M",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D"
                ]
                instructions += index_instructions

            pop_instructions = [
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ]
            instructions += pop_instructions

        self._writeInstructions(instructions)

    def close(self):
        self.file.close()


if __name__ == "__main__":
    code_writer = CodeWriter()
    code_writer.writeArithmetic("add")
    code_writer.writeArithmetic("not")
    code_writer.writeArithmetic("and")
    code_writer.writeArithmetic("gt")
    code_writer.writePushPop(C_PUSH, "static", 0)
    code_writer.writePushPop(C_PUSH, "local", 5)
    code_writer.writePushPop(C_PUSH, "argument", 5)
    code_writer.writePushPop(C_PUSH, "constant", 24)
    code_writer.writePushPop(C_POP, "argument", 5)
    code_writer.writePushPop(C_POP, "local", 7)
    code_writer.writePushPop(C_POP, "constant", 37)
    code_writer.close()
