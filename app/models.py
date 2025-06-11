# SQLAlchemy models
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class HCP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(10))
    is_primary = db.Column(db.Boolean, default=False)

class Residence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    hcp_id = db.Column(db.Integer, db.ForeignKey('hcp.id'))
    cert_begin_date = db.Column(db.Date)
    cert_end_date = db.Column(db.Date)


class User(UserMixin, db.Model):
    """Simple user model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
