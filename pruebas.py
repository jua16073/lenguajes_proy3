class Parser(tokens):
    def __init__(self, tokens):
        self.tokens = tokens
        self.id_token = 0
        self.actual_token = ''
        self.advance()

    def advance(self):
        self.actual_token += 1
        if self.id_token < len(self.tokens):
            self.actual_token = self.tokens[self.id_token]