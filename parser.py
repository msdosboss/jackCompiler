# Different types of insturctions that exist
C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8

ARITHEMTIC_INSTRUCTIONS = [
        "add",
        "sub",
        "neg",
        "eq",
        "gt",
        "lt",
        "and",
        "or",
        "not"
]


class Parse:
    def __init__(self, program_name: str):
        file = open(program_name, "r")
        self.lines_list = file.readlines()
        file.close()
        self.index = -1
        self.instruction_type = None

    def hasMoreLines(self) -> bool:
        if (self.index + 1 >= len(self.lines_list)):
            return False
        return True

    # Count is how many instructions you want to advance through
    def advance(self, count: int = 1) -> None:
        for i in range(count):

            while (self.hasMoreLines()):
                self.index += 1
                current_line = self.lines_list[self.index]
                # skipping comments and blank lines
                # This is a bit fragile 
                if(current_line[0] == '\n' or current_line[0] == '/'):
                    continue
                else:
                    # means we are at the end of the count
                    if (i + 1 == count):
                        self.lines_list[self.index] = self.lines_list[self.index].replace("\n", "")
                        # removes inline comments if they exist
                        comment_index = self.lines_list[self.index].find('/')
                        if (comment_index != -1):
                            self.lines_list[self.index] = self.lines_list[self.index][:comment_index]

                        tokens = self.lines_list[self.index].split()                 
                        print(tokens)

                        if (tokens[0] in ARITHEMTIC_INSTRUCTIONS):
                            self.instruction_type = C_ARITHMETIC
                        elif (tokens[0] == "push"):
                            self.instruction_type = C_PUSH
                        elif (tokens[0] == "pop"):
                            self.instruction_type = C_POP

                        return current_line
                    else:
                        continue

            # MegaMind meme goes here
            print("No lines?")
            return None

    def get_arg_one(self) -> str:
        if (self.instruction_type == C_RETURN):
            return None

        tokens = self.lines_list[self.index].split()

        if (self.instruction_type == C_ARITHMETIC):
            return tokens[0]

        return tokens[1]

    def get_arg_two(self) -> int:
        tokens = self.lines_list[self.index].split()
        if (self.instruction_type == C_PUSH or self.instruction_type == C_POP):
            return int(tokens[2])

        return None


if __name__ == "__main__":
        parser = Parse("orca.vm")
        while (parser.hasMoreLines()):
                parser.advance()
                print(parser.instruction_type)
                print(parser.get_arg_one() + " " + str(parser.get_arg_two()))
