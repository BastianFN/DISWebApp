# uffo/UFO/routes.py
from flask import Blueprint, jsonify
from uffo.UFO.database import select_all_ufo_sightings

# Create a new blueprint
ufo = Blueprint('ufo', __name__)

@ufo.route('/sightings')
def get_sightings():
    sightings = select_all_ufo_sightings()
    # Convert the sightings to a format suitable for JSON serialization
    sightings = [
        {
            'latitude': sighting[0],
            'longitude': sighting[1]
        }
        for sighting in sightings
    ]
    return jsonify(sightings)

