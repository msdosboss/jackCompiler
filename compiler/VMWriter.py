#Segments
ARGUMENT = 0
LOCAL = 1
STATIC = 2
THIS = 3
THAT = 4
POINTER = 5
TEMP = 6
CONSTANT = 7

segment_dict = {
    ARGUMENT : "argument",
    LOCAL : "local",
    STATIC : "static",
    THIS : "this",
    THAT : "that",
    POINTER : "pointer",
    TEMP : "temp",
    CONSTANT : "constant"
}

#Commands
ADD = 0
SUB = 1
NEG = 2
EQ = 3
GT = 4
LT = 5
AND = 6
OR = 7
NOT = 8

command_dict = {
    ADD : "add",
    SUB : "sub",
    NEG : "neg",
    EQ : "eq",
    GT : "gt",
    LT : "lt",
    AND : "and",
    OR : "or",
    NOT : "not"
}


class VMWriter:
    def __init__(self, file_name):
        self.output_file = open(file_name.replace(".jack", ".vm"), "w")

    def writePush(self, segment, index):
        self.output_file.write(f"push {segment_dict[segment]} {index}")

    def writePop(self, segment, index):
        self.output_file.write(f"pop {segment_dict[segment]} {index}")

    def writeArithmetic(self, command):
        self.output_file.write(command_dict[command])

    def writeLabel(self, label):
        self.output_file.write(f"label {label}")

    def writeGoto(self, label):
        self.output_file.write(f"goto {label}")

    def writeIf(self, label):
        self.output_file.write(f"if-goto {label}")

    def writeCall(self, name, nArgs):
        self.output_file.write(f"call {name} {nArgs}")

    def writeFunction(self, name, nVars):
        self.output_file.write(f"function {name} {nVars}")

    def close(self):
        self.output_file.close()

