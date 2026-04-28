import os
from parser import C_PUSH
from parser import C_POP

COMMAND_TYPE_DICT = {
    C_PUSH : "push",
    C_POP : "pop"
}

POINTER_TO_ASSMBLE = [
    "@THIS",
    "@THAT" 
]

SEGMENT_TO_ASSMBLE = {
    "local" : "@LCL",
    "argument" : "@ARG",
    "this" : "@THIS",
    "that" : "@THAT"
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
                "M=M-D",
                "@SP",
                "M=M+1"
            ],
    "neg" : [
                "@SP",
                "AM=M-1",
                "M=-M",
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
                "@SP",
                "A=M",
                "M=0",
                "@END",
                "0;JMP",
                "(TRUE)",
                "@SP",
                "A=M",
                "M=-1",
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
                "D=M-D",
                "@TRUE",
                "D;JGT",
                "(FALSE)",
                "@SP",
                "A=M",
                "M=0",
                "@END",
                "0;JMP",
                "(TRUE)",
                "@SP",
                "A=M",
                "M=-1",
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
                "D=M-D",
                "@TRUE",
                "D;JLT",
                "(FALSE)",
                "@SP",
                "A=M",
                "M=0",
                "@END",
                "0;JMP",
                "(TRUE)",
                "@SP",
                "A=M",
                "M=-1",
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
                "M=!M",
                "@SP",
                "M=M+1"
            ],
}

init_instructions = [
    "//Set up the stack pointer",
    "@256",
    "D=A",
    "@SP",
    "M=D",
    "@Sys.init",
    "0;JMP"
]


class CodeWriter:
    def __init__(self, file_name : str = "vm.asm"):
        self.file = open(file_name, "w")
        base_name = os.path.basename(file_name)
        self.file_name = base_name.replace(".vm", "")
        self.write_count = 0
        self.current_function = ""
        self.call_count = 0

    def _writeInstructions(self, instructions : list[str]):
        for instruction in instructions:
            self.file.write(instruction + '\n')
            self.write_count += 1

    def setFileName(self, file_name : str):
        base_name = os.path.basename(file_name)
        self.file_name = base_name.replace(".vm", "")

    def writeInit(self):
        self._writeInstructions(init_instructions)

    def writeArithmetic(self, operation : str):
        instructions = []
        instructions.append(f"//{operation}") 
        instructions += ARITHMETIC_TRANSLATIONS[operation]
        if (operation == "lt" or operation == "gt" or operation == "eq"):
            # making labels unique
            for i, _ in enumerate(instructions):
                if ("TRUE" in instructions[i]):
                    instructions[i] = instructions[i].replace("TRUE", f"TRUE{int(self.write_count)}")
                elif ("FALSE" in instructions[i]):
                    instructions[i] = instructions[i].replace("FALSE", f"FALSE{int(self.write_count)}")
                elif ("END" in instructions[i]):
                    instructions[i] = instructions[i].replace("END", f"END{int(self.write_count)}")

        self._writeInstructions(instructions)

    def writePushPop(self, command_type : int, segment : str, index : int):
        instructions = []
        instructions.append(f"//{COMMAND_TYPE_DICT[command_type]} {segment} {str(index)}")
        if (command_type == C_PUSH):
            if (segment == "constant"):
                constant_instructions = [
                    f"@{index}",
                    "D=A"
                ] 
                instructions += constant_instructions
            
            elif (segment == "static"):
                var_name = self.file_name.replace(".asm", "")
                static_instructions = [
                    f"@{var_name + "." + str(index)}",
                    "D=M"
                ]
                instructions += static_instructions 

            elif (segment == "temp"):
                start_temp = 5
                temp_reg = start_temp + index
                temp_instructions = [
                    f"@{temp_reg}",
                    "D=M"
                ]
                instructions += temp_instructions

            elif (segment == "pointer"):
                pointer_instructions = [
                    f"{POINTER_TO_ASSMBLE[index]}",
                    "D=M"
                ]
                instructions += pointer_instructions

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
            direct_instructions = [
                "D=A",
                "@R13",
                "M=D"
            ]
            if (segment == "constant"):
                instructions.append(f"@{index}")
                instructions += direct_instructions

            elif (segment == "static"):
                var_name = self.file_name.replace(".asm", "")
                instructions.append(f"@{var_name + "." + str(index)}")
                instructions += direct_instructions 

            elif (segment == "temp"):
                start_temp = 5
                temp_reg = start_temp + index
                instructions.append(f"@{temp_reg}")
                instructions += direct_instructions

            elif (segment == "pointer"):
                instructions.append(f"{POINTER_TO_ASSMBLE[index]}")
                instructions += direct_instructions 

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

    def writeLabel(self, label : str):
        instructions = []
        instructions.append(f"({self.current_function}${label})")

        self._writeInstructions(instructions)

    def writeGoto(self, label : str):
        goto_instructions = [
            f"//Goto {self.current_function}${label}",
            f"@{self.current_function}${label}",
            "0;JMP"
        ]

        self._writeInstructions(goto_instructions)
        
    def writeIf(self, label : str):
        if_goto_instructions = [
            f"//If-Goto {self.current_function}${label}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{self.current_function}${label}",
            "D;JNE"
        ]

        self._writeInstructions(if_goto_instructions)

    def writeFunction(self, function_name : str, nVars : int):
        self.current_function = f"{function_name}"
        function_instructions = [
            f"//def Function {function_name}",
            f"({self.current_function})"
        ]

        self._writeInstructions(function_instructions) 

        for _ in range(nVars):
            self.writePushPop(C_PUSH, "constant", "0")
        

    def writeCall(self, function_name : str, nArgs : int):
        function_label = f"{function_name}"
        return_label = f"{self.current_function}$ret.{self.call_count}"
        push_instructions = [
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
        
        call_instructions = [
            "// Push return address to stack",
            f"@{return_label}",
            "D=A",
        ]
        call_instructions += push_instructions
        
        call_instructions += [
            "// push LCL",
            "@LCL",
            "D=M",
        ]
        call_instructions += push_instructions
        
        call_instructions += [
            "// push ARG",
            "@ARG",
            "D=M",
        ]
        call_instructions += push_instructions
        
        call_instructions += [
            "// push THIS",
            "@THIS",
            "D=M",
        ]
        call_instructions += push_instructions
        
        call_instructions += [
            "// push THAT",
            "@THAT",
            "D=M",
        ]
        call_instructions += push_instructions
        
        arg_offset = 5 + nArgs
        call_instructions += [
            "// repostitions ARG",
            f"@{arg_offset}",
            "D=A",
            "@SP",
            "D=M-D",
            "@ARG",
            "M=D"
        ]

        call_instructions += [
            "// repostitions LCL",
            "@SP",
            "D=M",
            "@LCL",
            "M=D"
        ]

        call_instructions += [
            f"// Goto {function_label}",
            f"@{function_label}",
            "0;JMP"
        ]

        call_instructions += [
            f"({return_label})"
        ]

        self.call_count += 1
        self._writeInstructions(call_instructions) 
    
    def writeReturn(self):
        return_instructions = [
            "// Return",
            "// Frame = LCL",
            "@LCL",
            "D=M",
            "@R13",
            "M=D",
            "// RetAddr = *(frame - 5)",
            "@5",
            "D=A",
            "@R13",
            "A=M-D",
            "D=M",
            "@R14",
            "M=D",
            "// *ARG = pop()",
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            "// SP = ARG+1",
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D",
            "// THAT = *(frame - 1)",
            "@R13",
            "AM=M-1",
            "D=M",
            "@THAT",
            "M=D",
            "// THIS = *(frame - 2)",
            "@R13",
            "AM=M-1",
            "D=M",
            "@THIS",
            "M=D",
            "// ARG = *(frame - 3)",
            "@R13",
            "AM=M-1",
            "D=M",
            "@ARG",
            "M=D",
            "// LCL = *(frame - 4)",
            "@R13",
            "AM=M-1",
            "D=M",
            "@LCL",
            "M=D",
            "// Goto return address",
            "@R14",
            "A=M",
            "0;JMP"
        ]

        self._writeInstructions(return_instructions) 

        self.call_count = 0

    def close(self):
        self.file.close()


if __name__ == "__main__":
    code_writer = CodeWriter()
    code_writer.writeArithmetic("add")
    code_writer.writeArithmetic("not")
    code_writer.writeArithmetic("and")
    code_writer.writeArithmetic("gt")
    code_writer.writeArithmetic("gt")
    code_writer.writePushPop(C_PUSH, "static", 0)
    code_writer.writePushPop(C_PUSH, "local", 5)
    code_writer.writePushPop(C_PUSH, "argument", 5)
    code_writer.writePushPop(C_PUSH, "constant", 24)
    code_writer.writePushPop(C_POP, "argument", 5)
    code_writer.writePushPop(C_POP, "local", 7)
    code_writer.writePushPop(C_POP, "constant", 37)
    code_writer.writePushPop(C_POP, "static", 5)
    code_writer.writePushPop(C_POP, "temp", 5)
    code_writer.writePushPop(C_POP, "pointer", 0)
    code_writer.writePushPop(C_POP, "pointer", 1)
    code_writer.writePushPop(C_PUSH, "pointer", 1)
    code_writer.writePushPop(C_PUSH, "pointer", 0)
    code_writer.close()
