##########################
#TOKENS
##########################
TT_PLUS = 'TT_PLUS'
TOKEN_TYPE_INT = 'TT_INT'
TOKEN_TYPE_FLOAT = 'FLOAT'

class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.value}'

##########################
#LEXER
##########################
class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '+':
                tokens.append(TT_PLUS)
                self.advance()
        return tokens