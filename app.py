import os
from flask import Flask
from db import init_db, close_db


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "salary.db"),
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    app.teardown_appcontext(close_db)
    init_db(app)

    from routes import register_blueprints
    register_blueprints(app)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
