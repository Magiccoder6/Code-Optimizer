
import re


def remove_dead_code(dict:list[dict], symbol_table: list[dict]):
    for s in symbol_table:
        if(s['count']==1):
            filtered_array = [d for d in dict if d.get('variable') != s['name']]
            return (filtered_array, False)
        
    return (dict, True)

def generate_code_from_ast(ast:list[dict]):
    code = ''
    for a in ast:
        if a['type'] == 'constant':
            code = f'{code}{a["literal"]}\n'
        if a['type'] == 'variableAssignment':
            code = f'{code}{a["variable"]} {a["operator"]} {print_expression(a["expression"])}\n'
        if a['type'] == 'functionDefinition':
            code = f'{code}{a["identifier"]} {a["function_id"]}\n'
        if a['type'] == 'printStatement':
            statement = a["statement"]
            exp = re.search(r'\((.*?)\)', a["statement"]).group(1)
            if 'type' in exp:
                statement = re.sub(r'\(.*?\)', f'({str(print_expression(eval(exp)))})', statement)
            code = f'{code}{statement}\n'

    return code

def modify_symbol_table(table:list[dict], variable_name, initial:bool):
    #initial means if a variable or function was initialized or reinit
    # Dead code elimination
    for dictionary in table:
        if (variable_name in dictionary.values()):
            if initial:
                dictionary['count'] = 1
            else:
                dictionary['count'] += 1
            return

    table.append({'name': variable_name, 'count': 1})

def print_expression(json_expr):
    # Base case: if the json_expr is a leaf node, return its value
    if isinstance(json_expr, (int, float, str)):
        return str(json_expr)
    
    # Recursively construct the expression
    if('literal' in json_expr):
        return json_expr['literal']
    else:
        operand1 = print_expression(json_expr['operand1'])
        operand2 = print_expression(json_expr['operand2'])
        operator = json_expr['operator']
    
        # Concatenate the operands and operator to form the expression
        return f"({operand1} {operator} {operand2})"