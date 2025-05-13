# payment_service.py v1.0

import paypalrestsdk
from flask import current_app

class PaymentService:
    def __init__(self):
        paypalrestsdk.configure({
            "mode": current_app.config["PAYPAL_MODE"],  # "sandbox" or "live"
            "client_id": current_app.config["PAYPAL_CLIENT_ID"],
            "client_secret": current_app.config["PAYPAL_CLIENT_SECRET"]
        })

    def create_payment(self, amount, gig_id, return_url, cancel_url):
        """
        Creates a PayPal payment for a gig.
        - amount: The total payment amount (in USD).
        - gig_id: The ID of the gig being paid for.
        - return_url: URL to redirect to on successful payment.
        - cancel_url: URL to redirect to on payment cancellation.
        Returns the approval URL for the payment or None if failed.
        """
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "transactions": [{
                "amount": {
                    "total": f"{amount:.2f}",
                    "currency": "USD"
                },
                "description": f"Payment for VibeHubX Gig ID: {gig_id}"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return link.href
        return None

    def execute_payment(self, payment_id, payer_id):
        """
        Executes a PayPal payment after user approval.
        - payment_id: The ID of the payment.
        - payer_id: The ID of the payer.
        Returns the executed payment object or None if failed.
        """
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            return payment
        return None

    def payout_to_coder(self, coder_email, amount):
        """
        Sends a payout to the coder via PayPal.
        - coder_email: The coder's PayPal email.
        - amount: The amount to pay (in USD).
        Returns True if successful, False otherwise.
        """
        payout = paypalrestsdk.Payout({
            "sender_batch_header": {
                "sender_batch_id": f"PAYOUT-{int(datetime.utcnow().timestamp())}",
                "email_subject": "VibeHubX Payout"
            },
            "items": [{
                "recipient_type": "EMAIL",
                "amount": {
                    "value": f"{amount:.2f}",
                    "currency": "USD"
                },
                "receiver": coder_email,
                "note": "Thank you for your work on VibeHubX!"
            }]
        })