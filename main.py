from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from flask import Flask
from config import Config
from extensions import mongo, login_manager

# Import blueprints after extensions exist
from blueprints.auth.routes import auth_bp
from blueprints.books.routes import books_bp

# Import your user loader function
from models import load_user


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Fail fast so you don't get mongo.db == None later
    if not app.config.get("MONGO_URI"):
        raise RuntimeError("MONGO_URI is missing. Check that .env exists and is loading.")

    mongo.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def _load_user(user_id):
        return load_user(user_id)

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)

    from flask import render_template

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)