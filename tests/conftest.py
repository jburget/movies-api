import pytest
from app import app
from db import init_db


@pytest.fixture()
def server():
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        init_db()

    yield app



@pytest.fixture()
def client(server):
    return app.test_client()


@pytest.fixture()
def runner(server):
    return app.test_cli_runner()

@pytest.fixture()
def movie():
    return {
        "title": "The Matrix",
        "description": "The Matrix description",
        "release_year": 1999
    }
