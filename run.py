# run.py v1.0

import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    Entry point for the VibeHubX application.
    Creates and runs the Flask app in development or production mode.
    """
    # Create the Flask app using the factory function
    app = create_app()

    # Determine the environment (development or production)
    env = os.getenv('FLASK_ENV', 'development')
    debug = env == 'development'

    if debug:
        logger.info("Starting VibeHubX in development mode on http://127.0.0.1:5000")
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        logger.info("Starting VibeHubX in production mode. Use Gunicorn for deployment.")
        # In production, this script is typically run via Gunicorn, e.g.:
        # gunicorn -w 4 -b 0.0.0.0:8000 run:app
        # The 'app' instance is used directly by Gunicorn, so no app.run() is needed here.

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"Failed to start VibeHubX: {str(e)}")
        raise