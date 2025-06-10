# SQLAlchemy models
from app import db

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
