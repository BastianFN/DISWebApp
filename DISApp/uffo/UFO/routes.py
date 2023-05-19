# uffo/UFO/routes.py
from flask import Blueprint, jsonify
from uffo.UFO.database import select_all_ufo_sightings
from flask import Blueprint, jsonify, request
from uffo.UFO.database import select_all_ufo_sightings, get_ufo_comments

# Create a new blueprint
ufo = Blueprint('ufo', __name__)

@ufo.route('/sightings')
def get_sightings():
    sightings = select_all_ufo_sightings()
    # Convert the sightings to a format suitable for JSON serialization
    sightings = [
        {
            'latitude': sighting[0],
            'longitude': sighting[1],
            'comments': sighting[2]  # note the change here
        }
        for sighting in sightings
    ]
    return jsonify(sightings)

@ufo.route('/comments')
def get_comments():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)
    comments = get_ufo_comments(page, per_page)
    return jsonify(comments)

