"""
    Flask server for running the API for the database and web server for the application. 

    Currently provides routes to all static files in the `www` directory
"""

from flask import Flask, g

from blueprints.serve_static import serve_static
from blueprints.api import api
from config import Config, TestConfig


def create_app(testing=False):
    """Creates the Flask application for both serving static files and handling the database and API

    Args:
        testing (bool, optional): Whether or not to load the testing configuration or the deployment
            configuration. Defaults to False.

    Returns:
        Flask: The app to be run.
    """
    app = Flask(__name__)

    # Configure app
    if testing:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(serve_static)
    app.register_blueprint(api, url_prefix="/api")

    # Close database connections when the app context closes.
    @app.teardown_appcontext
    def close_db(exception):
        # pylint: disable=unused-argument
        """Closes the connection to the database when the app context is destroyed."""
        db = getattr(g, "_database", None)
        if db is not None:
            db.commit()
            db.close()

    return app
