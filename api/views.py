from flask import abort, request, redirect, jsonify, url_for
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from .utils import is_url_valid, integer_to_base62, base62_to_integer
from .models import Url
from .app import application, db


@application.route('/urls', methods=['POST'])
def create_url():
    data = request.json

    """
    Validation and format
    """
    if not data:
        return jsonify({'message': 'No valid JSON data was received'}), 400

    if 'url' not in data:
        return jsonify({'message': 'Url key is missing from POST data'}), 400

    url = request.json['url']
    if not url.startswith('https://'):
        url = 'https://{}'.format(url)

    if not is_url_valid(url):
        return jsonify({'message': 'The url format is invalid'}), 400

    if len(url) > 2048:
        return jsonify({'message': 'No more 2048 characters in URL'}), 400

    """
    Save URL in database
    """
    try:
        url_obj = Url.query.filter_by(url=url).one()
    except NoResultFound:
        url_obj = Url(url=url)
        db.session.add(url_obj)
        db.session.commit()

    base62_string = integer_to_base62(url_obj.id)

    return jsonify({
        "shortened_url": url_for('get_url', url_hash=base62_string, _external=True)
    }), 201


@application.route('/<url_hash>', methods=['GET'])
def get_url(url_hash):
    key = base62_to_integer(url_hash)
    try:
        url = Url.query.filter_by(id=key).one()
        url.requests += 1
        db.session.commit()
        return redirect(url.url)
    except NoResultFound:
        abort(404)


@application.route('/stats/<url_hash>', methods=['GET'])
def stats(url_hash):
    key = base62_to_integer(url_hash)
    try:
        url = Url.query.filter_by(id=key).one()
        return jsonify({
            "requests": url.requests,
            "hash": url_hash,
            "url": url.url
        }), 201
    except NoResultFound:
        abort(404)
