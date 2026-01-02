class CodeWriter:
    def __init__(self, file_name : str = "vm.out"):
        self.file = open(file_name, "w")

    def writeArithmetic(self, operation : str):
        


'''
add:
@sp
M=M-1
A=M
D=M

@sp
M=M-1
A=M
M=D+M

@sp
M=M+1

'''
