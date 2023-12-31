#!/usr/bin/python3
"""
a flask web application listening on 0.0.0.0, port 5000 and displays
'Hello HBNB'
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def state_list():
    """Returns a given string"""
    states = storage.all(State)
    states = [state for state in states.values()]
    states = sorted(states, key=lambda val: val.name)
    sorted_states = {}
    for state in states:
        sorted_states[state] = sorted(state.cities, key=lambda val: val.name)
    return render_template("8-cities_by_states.html",
                           sorted_states=sorted_states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
