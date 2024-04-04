import ply.yacc as yacc

from modules.lexer import tokens

# Define grammar rules
# Constant folding solution
def p_binary_operators(p): 
    '''expression : expression PLUS term
                  | expression MINUS term
       term       : term TIMES factor
                  | term DIVIDE factor'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# dead code elimination
def p_statement(p):
    '''statement : expression
                 | empty'''
    if p[1] is not None:
        print("Executing statement:", p[1])
        # Execute the expression
    else:
        print("Empty statement")
        # Do nothing (or handle the case of an empty statement)

def p_func(p):
    '''func : NAME NAME LPAREN RPAREN COLON'''
    print(p)
def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    raise Exception("Syntax error in input!", p)

def run_parser(code):
    # Build the parser
    error = 'None'
    result = 'None'
    try:
        parser = yacc.yacc()
        result = parser.parse(code)
    except Exception as e:
        error = e.__str__()
    
    return [result, error]