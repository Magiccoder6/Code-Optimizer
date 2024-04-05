import ply.lex as lex

# List of token names.   This is always required
tokens = [
   'NUMBER',
   'NAME',
   'PLUS',
   'MINUS',
   'COMMA',
   'COLON',
   'EQUALS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'NEWLINE',
   'DEF_KEYWORD',
   'PRINT_KEYWORD'
 ]

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_COLON = r':'
t_EQUALS = r'='

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_DEF_KEYWORD(t):
    r'def'
    return t

def t_PRINT_KEYWORD(t):
    r'print'
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    t.lexer.skip(1)
    raise Exception("Illegal character '%s'" % t.value[0])

# Define a rule for names (identifiers)
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def build_lexer(code):
    # Build the lexer
    tks = []
    error = 'None'
    try:
        lexer = lex.lex()
        lexer.input(code)
        while True:
            tok = lexer.token()
            if not tok: 
                break  
            tks.append(tok)
    except Exception as e:
        error = e.__str__()
        tks = None
    
    return [tks, error]