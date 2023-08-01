from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "flhMy0uJMACIg9fZeh7p"
    return app

