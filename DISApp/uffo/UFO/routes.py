# uffo/UFO/routes.py
from flask import Blueprint, jsonify
from uffo.UFO.database import select_all_ufo_sightings
from flask import Blueprint, jsonify, request
from uffo.UFO.database import select_all_ufo_sightings, get_ufo_comments, select_all_sightings, get_all_comments

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
            'comments': sighting[2]
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

@ufo.route('/all_sightings')
def get_all_sightings():
    sightings = select_all_sightings()
    sightings = [{'latitude': s[0], 'longitude': s[1], 'comments': s[2]} for s in sightings]
    return jsonify(sightings)

@ufo.route('/all_comments')
def get_all_comments():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)
    comments = get_all_comments(page, per_page)
    return jsonify(comments)

