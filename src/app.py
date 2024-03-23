from flask import Flask, render_template

# Create an instance of the Flask class. This instance will be the WSGI application.
app = Flask(__name__)

# Define a route through the app.route decorator. In this case, the route is the root ("/").
@app.route("/")
def hello_world():
    return render_template('index.html')

# Check if the executed script is the main program and run the Flask application.
# The debug=True argument provides a debug information page if there's an error and auto-reloads the server on code changes.
if __name__ == "__main__":
    app.run(debug=True)