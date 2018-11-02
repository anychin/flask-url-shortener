"""This script is used to initialize the Database tables."""

from api.app import db

db.create_all()
