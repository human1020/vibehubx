# transaction.py v1.0

from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    gig_id = db.Column(db.Integer, db.ForeignKey('gigs.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # Total payment
    platform_fee = db.Column(db.Float, nullable=False)  # 5% cut
    coder_payment = db.Column(db.Float, nullable=False)  # 95% to coder
    paypal_transaction_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_to_coder_at = db.Column(db.DateTime, nullable=True)

    # Relationship
    gig = db.relationship('Gig', backref='transaction', uselist=False)

    def __repr__(self):
        return f'<Transaction {self.id} for Gig {self.gig_id}>'