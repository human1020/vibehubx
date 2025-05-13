# auth_helpers.py v1.0

from flask_bcrypt import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Hashes a plaintext password using Flask-Bcrypt.
    - password: The plaintext password to hash.
    Returns the hashed password as a UTF-8 string.
    """
    return generate_password_hash(password).decode('utf8')

def verify_password(stored_hash, password):
    """
    Verifies a plaintext password against a stored hash.
    - stored_hash: The hashed password stored in the database.
    - password: The plaintext password provided by the user.
    Returns True if the password matches the hash, False otherwise.
    """
    return check_password_hash(stored_hash, password)