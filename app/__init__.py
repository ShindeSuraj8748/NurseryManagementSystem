from flask import Flask, flash, redirect, request
from flask_migrate import Migrate
from werkzeug.exceptions import RequestEntityTooLarge
from app.routes.batches import batches
from config import Config
from app.database import db
from app.routes.home import main
from app.routes.plants import plants
from app.routes.company import company
from app.routes.tray_sizes import tray
from app.routes.variety import variety
from app.routes.categories import categories
from app.routes.customers import customers
migrate = Migrate()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(plants)
    app.register_blueprint(batches)
    app.register_blueprint(company)
    app.register_blueprint(tray)
    app.register_blueprint(variety)
    app.register_blueprint(categories)
    app.register_blueprint(customers)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_file(e):
        flash("Image size must be less than 2 MB.", "danger")
        return redirect(request.url)

    return app