import flask
from flask import Flask, request
import db
from const import Fields
from http import HTTPStatus

app = Flask(__name__)
app.config.from_mapping(DATABASE="db.sqlite3")
db.init_app(app)


@app.route('/')
def hello():
    return "Hello, world!"

def validate_request(data: dict) -> bool:
    if not isinstance(data.get(Fields.description), str):
        data[Fields.description] = None
    return isinstance(data.get(Fields.title), str) \
        and isinstance(data.get(Fields.release_year), int)

@app.post('/movies')
def post_movie():
    app.logger.debug(request.data)
    if not validate_request(request.get_json()):
        flask.abort(HTTPStatus.BAD_REQUEST)

    data = request.get_json()
    db_conn = db.get_db()
    db_curr = db_conn.cursor()
    try:
        db_curr.execute(
                "INSERT INTO movies(title, description, release_year) VALUES (:title, :description, :release_year)",
                data)
        db_conn.commit()
        row_id = db_curr.execute("SELECT last_insert_rowid() FROM movies").fetchone()[0]
        app.logger.debug("Inserted row id: %s", row_id)
        data[Fields.id] = row_id
    except Exception as e:
        app.logger.error(e, exc_info=True)
        flask.abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db_curr.close()

    return data

@app.get('/movies/<int:id>')
def get_movie(id):
    app.logger.debug("Get movie with id: %s", id)
    db_conn = db.get_db()
    db_curr = db_conn.cursor()
    result = None
    try:
        db_curr.execute("SELECT * FROM movies WHERE id = ?", (id,))
        result = db_curr.fetchone()
    except Exception as e:
        app.logger.error(e, exc_info=True)
        flask.abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db_curr.close()

    if result is None:
        return flask.abort(HTTPStatus.NOT_FOUND)
    return {key: result[key] for key in result.keys()}


@app.get('/movies')
def get_movies():
    app.logger.debug("Retrieving all movies")
    db_curr = db.get_db().cursor()
    result = None
    try:
        db_curr.execute("SELECT * FROM movies")
        result = db_curr.fetchall()
    except Exception as e:
        app.logger.error(e, exc_info=True)
        flask.abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db_curr.close()

    if result is None:
        return []
    return [{key: row[key] for key in row.keys()} for row in result]


@app.put('/movies/<int:id>')
def update_movie(id):
    app.logger.debug("Updating movie with id: %s", id)
    if not validate_request(request.get_json()):
        flask.abort(HTTPStatus.BAD_REQUEST)
    data = request.get_json()
    data[Fields.id] = id

    db_conn = db.get_db()
    db_curr = db_conn.cursor()
    affected_rows = None
    try:
        db_curr.execute(
                "UPDATE movies SET"
                " title = :title, description = :description, release_year = :release_year"
                "  WHERE id = :id", data)
        db_conn.commit()
        affected_rows = db_curr.execute("SELECT total_changes() FROM movies").fetchone()
        app.logger.debug("Affected rows: %s", affected_rows)
    except Exception as e:
        app.logger.error(e, exc_info=True)
        flask.abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db_curr.close()

    if affected_rows is None or not affected_rows[0]:
        flask.abort(HTTPStatus.NOT_FOUND)
    return data


if __name__ == '__main__':
    app.run(debug=True)
