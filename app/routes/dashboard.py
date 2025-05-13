# dashboard.py v1.0

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import coder_required
from app.models.gig import Gig

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
@coder_required
def coder_dashboard():
    claimed_gigs = Gig.query.filter_by(coder_id=current_user.id, is_active=True).all()
    completed_gigs = Gig.query.filter_by(coder_id=current_user.id, is_active=False).all()
    return render_template('dashboard/coder_dashboard.html', claimed_gigs=claimed_gigs, completed_gigs=completed_gigs)