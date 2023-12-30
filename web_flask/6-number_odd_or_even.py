#!/usr/bin/python3
"""
a flask web application listening based on 0-hbnb_route.py that prints
'HBNB' using /hbnb path
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """Returns a given string"""
    return ("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns a given string"""
    return ("HBNB")


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """Returns a given string"""
    text = text.replace('_', ' ')
    return (f"C {text}")


@app.route('/python', strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text="is cool"):
    """Returns a given string"""
    text = text.replace('_', ' ')
    return (f"Python {text}")


@app.route("/number/<int:n>", strict_slashes=False)
def number_n(n):
    """Returns a given string"""
    return(f"{n} is a number")


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template_n(n):
    """Returns an HTML template"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even_n(n):
    """Returns an HTML template"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
