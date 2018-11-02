"""URL Shortening service SQLAlchemy views."""

from .app import db


class Url(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(2048), unique=True, nullable=False, index=True)
    requests = db.Column(db.Integer, nullable=True, default=0)
    def __repr__(self):
        return '<Url %r - %r>' % (self.id, self.url, self.requests)
