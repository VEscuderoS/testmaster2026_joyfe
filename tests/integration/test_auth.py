# =========================================================
# TESTS DE INTEGRACION - AUTENTICACION
# =========================================================


def test_registro_correcto(client):
    respuesta = client.post(
        "/registro",
        json={
            "username": "victor",
            "password": "1234"
        }
    )

    assert respuesta.status_code == 201

    datos = respuesta.get_json()

    assert datos["mensaje"] == "Usuario creado correctamente"


def test_registro_sin_username(client):
    respuesta = client.post(
        "/registro",
        json={
            "password": "1234"
        }
    )

    assert respuesta.status_code == 400

    datos = respuesta.get_json()

    assert datos["error"] == "El campo username es obligatorio"


def test_registro_password_corta(client):
    respuesta = client.post(
        "/registro",
        json={
            "username": "victor",
            "password": "123"
        }
    )

    assert respuesta.status_code == 400

    datos = respuesta.get_json()

    assert datos["error"] == "El campo password debe tener al menos 4 caracteres"


def test_registro_usuario_duplicado(client):
    usuario = {
        "username": "victor",
        "password": "1234"
    }

    primera_respuesta = client.post(
        "/registro",
        json=usuario
    )

    segunda_respuesta = client.post(
        "/registro",
        json=usuario
    )

    assert primera_respuesta.status_code == 201
    assert segunda_respuesta.status_code == 409

    datos = segunda_respuesta.get_json()

    assert datos["error"] == "Ese usuario ya existe"


def test_login_correcto(client):
    usuario = {
        "username": "victor",
        "password": "1234"
    }

    client.post(
        "/registro",
        json=usuario
    )

    respuesta = client.post(
        "/login",
        json=usuario
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert "token" in datos
    assert isinstance(datos["token"], str)
    assert len(datos["token"]) == 32


def test_login_password_incorrecta(client):
    client.post(
        "/registro",
        json={
            "username": "victor",
            "password": "1234"
        }
    )

    respuesta = client.post(
        "/login",
        json={
            "username": "victor",
            "password": "incorrecta"
        }
    )

    assert respuesta.status_code == 401

    datos = respuesta.get_json()

    assert datos["error"] == "Usuario o contrasena incorrectos"


def test_login_usuario_inexistente(client):
    respuesta = client.post(
        "/login",
        json={
            "username": "usuario_que_no_existe",
            "password": "1234"
        }
    )

    assert respuesta.status_code == 401

    datos = respuesta.get_json()

    assert datos["error"] == "Usuario o contrasena incorrectos"