# config.py v1.0

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///vibehubx.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE') or 'sandbox'
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')