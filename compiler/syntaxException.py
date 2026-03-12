class JackSyntaxError(Exception):
    def __init__(self, compile_step:str, file_name:str, line_count:int, actual_token:str, actual_type:str, expected_token=None, expected_type=None):
        self.expected_token = expected_token
        self.expected_type = expected_type
        self.actual_token = actual_token
        self.file_name = file_name
        self.line_count = line_count
        self.actual_type = actual_type
        self.compile_step = compile_step
        super().__init__()


    def __str__(self):
        if(self.expected_type):
            return f"""SyntaxError in {self.file_name} ({self.line_count}): > Failed while parsing {self.compile_step}.
                  Expected type: {self.expected_type}
                  Actual type: {self.actual_type} (Token: \"{self.actual_token}\")"""
        elif(self.expected_token):
            return f"""SyntaxError in {self.file_name} ({self.line_count}): > Failed while parsing {self.compile_step}.
                  Expected token: {self.expected_token}
                  Actual token: \"{self.actual_token}\" (Type: {self.actual_type})"""
        else:
            return "Didn't provide enough information to SyntaxError"
