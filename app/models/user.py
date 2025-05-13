# user.py v1.0

from flask_login import UserMixin
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_coder = db.Column(db.Boolean, default=False)  # True for Vibe Coders, False for Customers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    gigs_posted = db.relationship('Gig', foreign_keys='Gig.customer_id', backref='customer', lazy=True)
    gigs_claimed = db.relationship('Gig', foreign_keys='Gig.coder_id', backref='coder', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'