import pytest
from app import app


@pytest.fixture()
def server():
    app.config.update({
        "TESTING": True,
    })

    yield app

    # TODO: Clear the database


@pytest.fixture()
def client(server):
    return app.test_client()


@pytest.fixture()
def runner(server):
    return app.test_cli_runner()
