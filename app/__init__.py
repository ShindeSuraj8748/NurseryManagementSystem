from flask import Flask
from flask_migrate import Migrate
from app.routes.plants import plants
from config import Config
from app.database import db
from app.routes.home import main
from app.models import Plant

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(plants)

    return app