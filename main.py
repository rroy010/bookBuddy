from flask import Flask, render_template
from flask_login import LoginManager, current_user

from config import Config
from models import mongo, load_user
from blueprints.auth.routes import auth_bp
from blueprints.books.routes import books_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    login_manager.user_loader(load_user)

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)

    @app.context_processor
    def inject_user():
        return {'current_user': current_user}

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

app = create_app()
if __name__ == '__main__':
    
    app.run(debug=True)
