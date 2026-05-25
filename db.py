import sqlite3
import os
import weakref
from flask import g, current_app


def get_db():
    if "db" not in g:
        # For :memory: databases a persistent connection is stored on the app;
        # each sqlite3.connect(":memory:") call creates a separate empty database,
        # so all requests must share the one connection created during init_db.
        persistent = getattr(current_app._get_current_object(), "_persistent_db", None)
        if persistent is not None:
            g.db = persistent
        else:
            g.db = sqlite3.connect(
                current_app.config["DATABASE"],
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    # Skip closing the shared persistent connection; it is closed by the
    # weakref finalizer registered in init_db when the app is garbage-collected.
    if db is not None and not getattr(current_app._get_current_object(), "_persistent_db", None):
        db.close()


def init_db(app):
    conn = sqlite3.connect(
        app.config["DATABASE"],
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    conn.row_factory = sqlite3.Row
    schema_path = os.path.join(os.path.dirname(__file__), "schema", "employee.sql")
    with open(schema_path) as f:
        conn.executescript(f.read())
    conn.commit()

    if app.config["DATABASE"] == ":memory:":
        app._persistent_db = conn
        weakref.finalize(app, conn.close)
