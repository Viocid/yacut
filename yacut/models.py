from datetime import datetime

from flask import url_for

from yacut import db
from yacut.constants import MAX_LENGHT_ORIGINAL, MAX_LENGHT_SHORT


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGHT_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGHT_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            "url": self.original,
            "short_link": url_for(
                "redirect_view", short_id=self.short, _external=True
            ),
        }
