import pytest

from app import crear_app


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / "test.db"

    aplicacion = crear_app(db_path)

    aplicacion.config.update({
        "TESTING": True,
    })

    yield aplicacion


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    usuario = {
        "username": "victor",
        "password": "1234"
    }

    respuesta_registro = client.post(
        "/registro",
        json=usuario
    )

    assert respuesta_registro.status_code == 201

    respuesta_login = client.post(
        "/login",
        json=usuario
    )

    assert respuesta_login.status_code == 200

    token = respuesta_login.get_json()["token"]

    return {
        "Authorization": f"Bearer {token}"
    }