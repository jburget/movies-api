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


def test_movie_update(client, movie):
    response = client.post("/movies", json=movie)
    assert response.status_code == HTTPStatus.OK
    movie[Fields.id] = response.get_json().get(Fields.id)

    # update title
    movie[Fields.title] = "The Matrix 2"
    response = client.put(f"/movies/{movie[Fields.id]}", json=movie)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == movie

    # update description
    movie[Fields.description] = "The Matrix description 2"
    response = client.put(f"/movies/{movie[Fields.id]}", json=movie)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == movie

    # update release_year
    movie[Fields.release_year] = 2000
    response = client.put(f"/movies/{movie[Fields.id]}", json=movie)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == movie

    # check if updated correctly in database
    response = client.get(f"/movies/{movie[Fields.id]}")
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == movie

    # check deleting description
    del movie[Fields.description]
    response = client.put(f"/movies/{movie[Fields.id]}", json=movie)
    movie[Fields.description] = None
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == movie


def test_invalid_movie_update(client, movie):
    response = client.post("/movies", json=movie)
    assert response.status_code == HTTPStatus.OK
    movie[Fields.id] = response.get_json().get(Fields.id)

    # invalid movie id
    response = client.put(f"/movies/{movie[Fields.id] + 1}", json=movie)
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.put("/movies/0", json=movie)
    assert response.status_code == HTTPStatus.NOT_FOUND

    # missing title
    del movie[Fields.title]
    response = client.put(f"/movies/{movie[Fields.id]}", json=movie)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # wrong data type of release_year
    movie[Fields.release_year] = "1999"
    response = client.put(f"/movies/{movie[Fields.id]}", json=movie)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_all_movies(client, movie):
    expected_list = []
    for _ in range(10):
        response = client.post(f"/movies", json=movie)
        assert response.status_code == HTTPStatus.OK
        movie[Fields.id] = response.get_json().get(Fields.id)
        expected_list.append(movie.copy())

    response = client.get("/movies")
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == expected_list
