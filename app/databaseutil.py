import flask
import psycopg2
from app.instance.config import TestConfig as config
import psycopg2.extras
from app import app


def get_connection():
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = psycopg2.connect(
        database=config.DB_NAME, host=config.DB_HOST,
        user=config.DB_USER, password=config.DB_PASS)

    return flask.g.dbconn


def get_cursor():
    return get_connection().cursor(cursor_factory=psycopg2.extras.DictCursor)


def query_one(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        print(cur.description)
        return dict(cur.fetchone())


def query_all(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        db_response = cur.fetchall()
        result = {}
        for index, el in enumerate(db_response):
            result.update({index: dict(el)})
        return result


def _rollback_db(sender, exception, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.rollback()
        conn.close()
        delattr(flask.g, 'dbconn')


flask.got_request_exception.connect(_rollback_db, app)


def _commit_db(sender, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.commit()
        conn.close()
        delattr(flask.g, 'dbconn')


flask.request_finished.connect(_commit_db, app)


def execute(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        return True


def execute_and_return_new(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        new_id = cur.fetchone()[0]
        return new_id

