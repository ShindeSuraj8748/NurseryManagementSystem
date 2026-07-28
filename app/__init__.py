from flask import Flask, flash, redirect, request
from flask_migrate import Migrate
from werkzeug.exceptions import RequestEntityTooLarge

from config import Config
from app.database import db
from app.routes.home import main
from app.routes.plants import plants

migrate = Migrate()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(plants)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_file(e):
        flash("Image size must be less than 2 MB.", "danger")
        return redirect(request.url)

    return app