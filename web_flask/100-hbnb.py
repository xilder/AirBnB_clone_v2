#!/usr/bin/python3
"""
a flask web application listening on 0.0.0.0, port 5000 and displays
'Hello HBNB'
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User
app = Flask(__name__)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb_filters():
    """Returns a given string"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place).values()
    users = storage.all(User).values()
    places_users = {}
    for place in places:
        for user in users:
            if place.user_id == user.id:
                places_users[place] = user

    return render_template("100-hbnb.html", states=states,
                           amenities=amenities, places=places_users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
