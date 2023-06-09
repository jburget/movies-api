from http import HTTPStatus


def test_root_response(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.text == "Hello, world!"
