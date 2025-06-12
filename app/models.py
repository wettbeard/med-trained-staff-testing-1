from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    company = db.relationship('Company', backref='users')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        return self.role == role
    
    def can_edit_hcp(self, hcp):
        if self.role == 'admin':
            return True
        elif self.role == 'nurse':
            return hcp.company_id == self.company_id
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Company {self.name}>'

class HCP(db.Model):
    __tablename__ = 'hcps'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    hire_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company = db.relationship('Company', backref='hcps')
    certifications = db.relationship('Certification', backref='hcp', lazy='dynamic')
    
    @property
    def active_certifications(self):
        today = date.today()
        return self.certifications.filter(
            Certification.is_active == True,
            Certification.expiry_date >= today
        ).all()
    
    @property
    def expired_certifications(self):
        today = date.today()
        return self.certifications.filter(
            Certification.expiry_date < today
        ).all()
    
    def __repr__(self):
        return f'<HCP {self.name}>'

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(10), nullable=False)
    client_code = db.Column(db.String(20), unique=True)
    is_primary = db.Column(db.Boolean, default=False)
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    residence = db.relationship('Residence', backref='clients')
    
    def __repr__(self):
        return f'<Client {self.initials}>'

class Residence(db.Model):
    __tablename__ = 'residences'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company = db.relationship('Company', backref='residences')
    
    def __repr__(self):
        return f'<Residence {self.name}>'

class Certification(db.Model):
    __tablename__ = 'certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    hcp_id = db.Column(db.Integer, db.ForeignKey('hcps.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    certification_type = db.Column(db.String(50), nullable=False, default='medication_administration')
    issue_date = db.Column(db.Date, nullable=False, default=date.today)
    expiry_date = db.Column(db.Date, nullable=False)
    issued_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    revoked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    revoked_at = db.Column(db.DateTime)
    revocation_reason = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    client = db.relationship('Client', backref='certifications')
    issuer = db.relationship('User', foreign_keys=[issued_by], backref='issued_certifications')
    revoker = db.relationship('User', foreign_keys=[revoked_by], backref='revoked_certifications')
    
    @property
    def is_expired(self):
        return date.today() > self.expiry_date
    
    @property
    def days_until_expiry(self):
        return (self.expiry_date - date.today()).days
    
    def revoke(self, user, reason=None):
        self.is_active = False
        self.revoked_by = user.id
        self.revoked_at = datetime.utcnow()
        self.revocation_reason = reason
    
    def __repr__(self):
        return f'<Certification {self.hcp.name} -> {self.client.initials}>'