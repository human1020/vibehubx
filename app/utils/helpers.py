# helpers.py v1.0

from datetime import datetime, timedelta

def calculate_fees(amount):
    """
    Calculates the platform fee and coder payment from a gig's total amount.
    - amount: The total payment amount for the gig (in USD).
    Returns a tuple (platform_fee, coder_payment) where:
        - platform_fee: 5% of the total amount.
        - coder_payment: 95% of the total amount.
    """
    platform_fee = amount * 0.05
    coder_payment = amount * 0.95
    return platform_fee, coder_payment

def set_expiration_time(hours=24):
    """
    Sets an expiration time for a gig based on the current UTC time.
    - hours: The number of hours until expiration (default is 24).
    Returns a datetime object representing the expiration time.
    """
    return datetime.utcnow() + timedelta(hours=hours)