#Segments
ARGUMENT_SEG = 0
LOCAL_SEG = 1
STATIC_SEG = 2
THIS_SEG = 3
THAT_SEG = 4
POINTER_SEG = 5
TEMP_SEG = 6
CONSTANT_SEG = 7

segment_dict = {
    ARGUMENT_SEG : "argument",
    LOCAL_SEG : "local",
    STATIC_SEG : "static",
    THIS_SEG : "this",
    THAT_SEG : "that",
    POINTER_SEG : "pointer",
    TEMP_SEG : "temp",
    CONSTANT_SEG : "constant"
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
        self.output_file.write(f"push {segment_dict[segment]} {index}\n")

    def writePop(self, segment, index):
        self.output_file.write(f"pop {segment_dict[segment]} {index}\n")

    def writeArithmetic(self, command):
        self.output_file.write(f"{command_dict[command]}\n")

    def writeLabel(self, label):
        self.output_file.write(f"label {label}\n")

    def writeGoto(self, label):
        self.output_file.write(f"goto {label}\n")

    def writeIf(self, label):
        self.output_file.write(f"if-goto {label}\n")

    def writeCall(self, name, nArgs):
        self.output_file.write(f"call {name} {nArgs}\n")

    def writeFunction(self, name, nVars):
        self.output_file.write(f"function {name} {nVars}\n")

    def close(self):
        self.output_file.write("\n")
        self.output_file.close()

