from http import HTTPStatus
from const import Fields

def test_movies_valid_post(client):
    data = {Fields.title: "The Matrix", Fields.release_year: 1999}
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.OK
    data[Fields.id] = response.get_json().get(Fields.id)
    data[Fields.description] = None
    assert response.get_json() == data

    data[Fields.description] = "The Matrix description"
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.OK
    data[Fields.id] = response.get_json().get(Fields.id)
    assert response.get_json() == data


def test_invalid_movie_post(client):
    # wrong data type of release_year
    data = {Fields.title: "The Matrix", Fields.release_year: "1999"}
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # missing release_year
    del data[Fields.release_year]
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # missing title
    data = {Fields.release_year: 1999}
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # wrong data type of title
    data = {Fields.title: 1999, Fields.release_year: 1999}
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # title is null
    data = {Fields.title: None, Fields.release_year: 1999}
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # release_year is null
    data = {Fields.title: "The Matrix", Fields.release_year: None}
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_movie_id_get(client):
    data = {Fields.title: "The Matrix", Fields.description: "The Matrix description",
            Fields.release_year: 1999}
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.OK
    data[Fields.id] = response.get_json().get(Fields.id)

    response = client.get(f"/movies/{data[Fields.id]}")
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == data

    # test movie without description
    del data[Fields.description]
    response = client.post("/movies", json=data)
    assert response.status_code == HTTPStatus.OK
    data[Fields.id] = response.get_json().get(Fields.id)
    data[Fields.description] = None
    response = client.get(f"/movies/{data[Fields.id]}")
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == data


def test_invalid_movie_id_get(client):
    # movie ids start from 1
    response = client.get("/movies/0")
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.get("/movies/15648567")
    assert response.status_code == HTTPStatus.NOT_FOUND
