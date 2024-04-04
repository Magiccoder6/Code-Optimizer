from flask import Flask, jsonify, render_template, request

from modules.lexer import build_lexer
from modules.parser import run_parser


# Create an instance of the Flask class. This instance will be the WSGI application.
app = Flask(__name__)

# Define a route through the app.route decorator. In this case, the route is the root ("/").
@app.route("/")
def hello_world():
    
    return render_template('index.html')

@app.route("/run", methods=['POST'])
def run_compiler():
    data = request.json
    
    tokens, error = build_lexer(code=data['programData'])

    parse_result, parse_error = run_parser(code=data['programData'])
        
    return jsonify({'lexerResult': {'tokens': "Tokens {}".format(str(tokens)), 'error': error}, 'parserResult': {'result': parse_result, 'error': parse_error} })


if __name__ == "__main__":
    app.run(debug=True)