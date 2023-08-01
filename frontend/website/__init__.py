from flask import Flask
from .views import views
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "flhMy0uJMACIg9fZeh7p"
    app.register_blueprint(views, url_prefix="/")
    return app

def run():
    """Runs the frontend."""
    app = create_app()
    app.run()
