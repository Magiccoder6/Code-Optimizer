import ply.yacc as yacc

from modules.lexer import tokens
from modules.helpers.optimizer import remove_dead_code, generate_code_from_ast, modify_symbol_table

SYMBOL_TABLE = []

# Define grammar rules
def p_program(p):
    '''program : statement
                | function
                | print_statement'''
    p[0] = p[1]

def p_function_def(p):
    '''function : DEF_KEYWORD NAME LPAREN RPAREN COLON'''
    p[0] = {'type': 'functionDefinition', 'identifier': p[1], 'name': p[2], 'function_id': f'{p[2]}{p[3]}{p[4]}{p[5]}'}
    modify_symbol_table(table=SYMBOL_TABLE, variable_name=p[2], initial=True)

def p_print_statement(p):
    '''print_statement : PRINT_KEYWORD LPAREN NAME RPAREN
                       | PRINT_KEYWORD LPAREN NUMBER RPAREN
                       | PRINT_KEYWORD LPAREN expression RPAREN'''
    p[0] = {'type': 'printStatement', 'statement': f'{p[1]}{p[2]}{p[3]}{p[4]}'}
    if isinstance(p[3], str):
        modify_symbol_table(table=SYMBOL_TABLE, variable_name=p[3], initial=False)

def p_statement(p):
    '''statement : assignment_statement
                | expression_statement'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : NAME EQUALS expression'''
    p[0] = {'type':'variableAssignment','variable': p[1], 'operator': p[2], 'expression': p[3]}
    modify_symbol_table(table=SYMBOL_TABLE, variable_name=p[1], initial=True)


def p_statement_expr(p):
    'expression_statement : expression'
    p[0] = p[1]

def p_binary_operators(p): 
    '''expression : expression PLUS term
                  | expression MINUS term
       term       : term TIMES factor
                  | term DIVIDE factor'''
    # Constant folding solution
    if (isinstance(p[1], int) and isinstance(p[3], int)):
        if p[2] == '+':
            p[0] = {'type':'constant','literal': p[1] + p[3]}
        elif p[2] == '-':
            p[0] = {'type':'constant','literal': p[1] - p[3]}
        elif p[2] == '*':
            p[0] = {'type':'constant','literal': p[1] * p[3]}
        elif p[2] == '/':
            p[0] = {'type':'constant','literal': p[1] / p[3]} 
    else:
        p[0] = {'operand1': p[1], 'operator': p[2], 'operand2': p[3]}
        

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_name(p):
    'factor : NAME'
    p[0] = p[1]
    modify_symbol_table(table=SYMBOL_TABLE, variable_name=p[1], initial=False)

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    if p:
        raise Exception(f"Syntax error at token {p.type}, value '{p.value}', line {p.lineno}")
    else:
        raise Exception("Syntax error at EOF")

def run_parser(code):
    global SYMBOL_TABLE
    # Build the parser
    
    error = 'None'
    result = []
    optimized_code = ''

    try:
        lines = code.splitlines()
        parser = yacc.yacc()

        while True:
            for line in lines:
                print(line)
                if line.strip() != '':
                    data = parser.parse(line)
                    result.append(data)
            
            #remove dead code OPTIMIZATION
            result, all_deadcode_removed = remove_dead_code(result, SYMBOL_TABLE)
            SYMBOL_TABLE = []

            lines = generate_code_from_ast(result)
            optimized_code = lines

            if not all_deadcode_removed:
                if lines != '':
                    lines = lines.splitlines()
                    result = []
                else:
                    break
            else:
                break
            
    except Exception as e:
        error = e.__str__()
        result = None
        
    
    return [result, error, optimized_code]