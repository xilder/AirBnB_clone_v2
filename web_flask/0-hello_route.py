#!/usr/bin/python3
"""
a flask web application listening on 0.0.0.0, port 5000 and displays
'Hello HBNB'
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """Returns a given string"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
