from parser import C_PUSH
from parser import C_POP


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

    def writeArithmetic(self, operation : str):
        instructions = ARITHMETIC_TRANSLATIONS[operation]
        if (operation == "lt" or operation == "gt" or operation == "eq"):
            # making labels unique
            for i, _ in enumerate(instructions):
                if (instructions[i] == "(TRUE)"):
                    instructions[i] = instructions[i].replace("TRUE", f"TRUE{int(self.write_count)}")
                elif (instructions[i] == "(FALSE)"):
                    instructions[i] = instructions[i].replace("FALSE", f"FALSE{int(self.write_count)}")
                elif (instructions[i] == "(END)"):
                    instructions[i] = instructions[i].replace("END", f"END{int(self.write_count)}")

        for instruction in instructions:
            self.file.write(instruction + '\n')
            self.write_count += 1

    def close(self):
        self.file.close()


if __name__ == "__main__":
    code_writer = CodeWriter()
    code_writer.writeArithmetic("add")
    code_writer.writeArithmetic("not")
    code_writer.writeArithmetic("and")
    code_writer.writeArithmetic("gt")
    code_writer.writeArithmetic("lt")
    code_writer.close()
