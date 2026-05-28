import os
import re
import sqlite3
import weakref

from flask import g, current_app


class DBWrapper:
    """Normalises sqlite3 and psycopg2 so routes need no engine-specific code."""

    def __init__(self, conn, engine, persistent=False):
        self._conn = conn
        self._engine = engine
        self._persistent = persistent

    def _adapt(self, sql):
        """Convert ? → %s and LIKE → ILIKE for PostgreSQL."""
        if self._engine == 'postgresql':
            return sql.replace('?', '%s').replace(' LIKE ', ' ILIKE ')
        return sql

    def execute(self, sql, params=()):
        if self._engine == 'postgresql':
            cur = self._conn.cursor()
            cur.execute(self._adapt(sql), params)
            return cur
        return self._conn.execute(sql, params)

    def executemany(self, sql, rows):
        if self._engine == 'postgresql':
            from psycopg2.extras import execute_values
            # execute_values needs "VALUES %s", not "VALUES (%s, %s, ...)"
            adapted = re.sub(
                r'VALUES\s*\([^)]+\)', 'VALUES %s',
                self._adapt(sql), flags=re.IGNORECASE,
            )
            cur = self._conn.cursor()
            execute_values(cur, adapted, rows)
            return cur
        return self._conn.executemany(sql, rows)

    def insert_returning_id(self, sql, params=()):
        """Execute an INSERT and return the auto-generated primary key."""
        if self._engine == 'postgresql':
            cur = self._conn.cursor()
            cur.execute(self._adapt(sql) + ' RETURNING empid', params)
            return cur.fetchone()[0]
        cursor = self._conn.execute(sql, params)
        return cursor.lastrowid

    def tenure_avg_expr(self):
        """SQL fragment for average employee tenure in years."""
        if self._engine == 'postgresql':
            return "AVG(EXTRACT(EPOCH FROM (NOW() - doj::date)) / 31557600.0)"
        return "AVG((julianday('now') - julianday(doj)) / 365.25)"

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        if not self._persistent:
            self._conn.close()


def get_db():
    if 'db' not in g:
        engine = current_app.config.get('DB_ENGINE', 'sqlite')

        if engine == 'postgresql':
            import psycopg2
            import psycopg2.extras
            conn = psycopg2.connect(
                current_app.config['DATABASE_URL'],
                cursor_factory=psycopg2.extras.DictCursor,
            )
            g.db = DBWrapper(conn, 'postgresql')
        else:
            # Reuse the single persistent connection for :memory: databases
            # (each sqlite3.connect(":memory:") creates a separate empty DB).
            persistent = getattr(current_app._get_current_object(), '_persistent_db', None)
            if persistent is not None:
                g.db = DBWrapper(persistent, 'sqlite', persistent=True)
            else:
                conn = sqlite3.connect(
                    current_app.config['DATABASE'],
                    detect_types=sqlite3.PARSE_DECLTYPES,
                )
                conn.row_factory = sqlite3.Row
                g.db = DBWrapper(conn, 'sqlite')
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()  # DBWrapper.close() skips persistent connections


def init_db(app):
    engine = app.config.get('DB_ENGINE', 'sqlite')
    schema_dir = os.path.join(os.path.dirname(__file__), 'schema')

    if engine == 'postgresql':
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(
            app.config['DATABASE_URL'],
            cursor_factory=psycopg2.extras.DictCursor,
        )
        schema_path = os.path.join(schema_dir, 'employee_pg.sql')
        with open(schema_path) as f:
            conn.cursor().execute(f.read())
        conn.commit()
        conn.close()
        print("postgres table created successfully!")
    else:
        conn = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        conn.row_factory = sqlite3.Row
        schema_path = os.path.join(schema_dir, 'employee.sql')
        with open(schema_path) as f:
            conn.executescript(f.read())
        conn.commit()

        if app.config['DATABASE'] == ':memory:':
            app._persistent_db = conn
            weakref.finalize(app, conn.close)
