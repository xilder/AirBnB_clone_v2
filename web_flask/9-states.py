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


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def state_list(id=None):
    """Returns a given string"""
    states = storage.all(State)
    if id is None:
        return render_template("9-states.html", states=states, mode="all")
    else:
        for state in states.values():
            if state.id == id:
                return render_template("9-states.html",
                                       states=state, mode="id")
        return render_template("9-states.html", states=None, mode="none")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
