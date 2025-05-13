# gigs.py v1.0

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.gig import Gig
from app.models.transaction import Transaction
from app.services.payment_service import PaymentService
from app.services.github_service import GitHubService
from app.utils.decorators import coder_required
from app.utils.helpers import set_expiration_time, calculate_fees

gigs = Blueprint('gigs', __name__)

@gigs.route('/')
def list_gigs():
    active_gigs = Gig.query.filter_by(is_active=True, coder_id=None).all()
    return render_template('gigs/list_gigs.html', gigs=active_gigs)

@gigs.route('/gig/<int:id>')
def gig_detail(id):
    gig = Gig.query.get_or_404(id)
    return render_template('gigs/gig_detail.html', gig=gig)

@gigs.route('/post', methods=['GET', 'POST'])
@login_required
def post_gig():
    if current_user.is_coder:
        flash('Only customers can post gigs.', 'danger')
        return redirect(url_for('gigs.list_gigs'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        budget = float(request.form.get('budget'))
        github_repo = request.form.get('github_repo')

        github_service = GitHubService()
        if not github_service.validate_repo(github_repo):
            flash('Invalid GitHub repository URL.', 'danger')
            return redirect(url_for('gigs.post_gig'))

        gig = Gig(
            title=title,
            description=description,
            budget=budget,
            github_repo=github_repo,
            customer_id=current_user.id,
            expires_at=set_expiration_time(hours=24),
            is_active=True
        )
        db.session.add(gig)
        db.session.commit()

        payment_service = PaymentService()
        return_url = url_for('gigs.payment_success', gig_id=gig.id, _external=True)
        cancel_url = url_for('gigs.payment_cancel', gig_id=gig.id, _external=True)
        approval_url = payment_service.create_payment(budget, gig.id, return_url, cancel_url)

        if approval_url:
            return redirect(approval_url)
        else:
            flash('Failed to initiate payment. Please try again.', 'danger')
            return redirect(url_for('gigs.post_gig'))

    return render_template('gigs/post_gig.html')

@gigs.route('/payment_success/<int:gig_id>')
def payment_success(gig_id):
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    gig = Gig.query.get_or_404(gig_id)
    payment_service = PaymentService()
    payment = payment_service.execute_payment(payment_id, payer_id)

    if payment:
        platform_fee, coder_payment = calculate_fees(gig.budget)
        transaction = Transaction(
            gig_id=gig.id,
            amount=gig.budget,
            platform_fee=platform_fee,
            coder_payment=coder_payment,
            paypal_transaction_id=payment.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Payment successful! Your gig is now live.', 'success')
    else:
        db.session.delete(gig)
        db.session.commit()
        flash('Payment failed. Gig has been removed.', 'danger')

    return redirect(url_for('gigs.list_gigs'))

@gigs.route('/payment_cancel/<int:gig_id>')
def payment_cancel(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    db.session.delete(gig)
    db.session.commit()
    flash('Payment cancelled. Gig has been removed.', 'danger')
    return redirect(url_for('gigs.list_gigs'))

@gigs.route('/claim/<int:id>', methods=['POST'])
@login_required
@coder_required
def claim_gig(id):
    gig = Gig.query.get_or_404(id)
    if not gig.is_active or gig.coder_id:
        flash('This gig is no longer available.', 'danger')
        return redirect(url_for('gigs.list_gigs'))

    gig.coder_id = current_user.id
    gig.claimed_at = datetime.utcnow()
    db.session.commit()
    flash('Gig claimed successfully!', 'success')
    return redirect(url_for('dashboard.coder_dashboard'))

@gigs.route('/complete/<int:id>', methods=['POST'])
@login_required
@coder_required
def complete_gig(id):
    gig = Gig.query.get_or_404(id)
    if gig.coder_id != current_user.id:
        flash('You are not authorized to complete this gig.', 'danger')
        return redirect(url_for('dashboard.coder_dashboard'))

    github_service = GitHubService()
    # For MVP, we assume the coder provides the commit SHA manually or we fetch the latest commit (simplified here)
    # In a full implementation, you'd integrate a form to submit the commit SHA
    commit_sha = "latest_commit_sha_placeholder"  # Replace with actual logic
    if not github_service.check_commit(gig.github_repo, commit_sha):
        flash('No valid commit found in the repository.', 'danger')
        return redirect(url_for('dashboard.coder_dashboard'))

    gig.completed_at = datetime.utcnow()
    gig.is_active = False
    transaction = gig.transaction
    payment_service = PaymentService()
    if payment_service.payout_to_coder(current_user.email, transaction.coder_payment):
        transaction.paid_to_coder_at = datetime.utcnow()
        db.session.commit()
        flash('Gig marked as completed! Payment has been sent.', 'success')
    else:
        flash('Payout failed. Please contact support.', 'danger')

    return redirect(url_for('dashboard.coder_dashboard'))