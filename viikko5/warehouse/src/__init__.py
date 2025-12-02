from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', secrets.token_hex(32)),
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(
                app.instance_path, 'warehouse.db'
            ),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    return app
