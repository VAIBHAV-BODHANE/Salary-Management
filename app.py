import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from db import init_db, close_db

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "salary.db"),
        DB_ENGINE='sqlite',
    )

    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        database_url = os.environ.get('DATABASE_URL', '')
        if database_url:
            # Render/Heroku may supply the legacy postgres:// prefix
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            app.config['DATABASE_URL'] = database_url
            app.config['DB_ENGINE'] = 'postgresql'

    os.makedirs(app.instance_path, exist_ok=True)

    app.teardown_appcontext(close_db)
    init_db(app)

    from routes import register_blueprints
    register_blueprints(app)

    CORS(app, origins=["http://localhost:5173", "https://salarymanagementfrontend.vercel.app"])

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
