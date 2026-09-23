# =========================================================
# TESTS DE INTEGRACION - CLIENTES
# =========================================================


def test_listar_clientes_sin_token(client):
    respuesta = client.get("/clientes")

    assert respuesta.status_code == 401
    assert respuesta.get_json()["error"] == "Falta el token de autenticacion"


def test_listar_clientes_vacio(client, auth_headers):
    respuesta = client.get(
        "/clientes",
        headers=auth_headers
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json() == []


def test_crear_cliente(client, auth_headers):
    cliente = {
        "nombre": "Victor",
        "email": "victor@test.com",
        "telefono": "600123123"
    }

    respuesta = client.post(
        "/clientes",
        json=cliente,
        headers=auth_headers
    )

    assert respuesta.status_code == 201

    datos = respuesta.get_json()

    assert "id" in datos
    assert datos["nombre"] == "Victor"
    assert datos["email"] == "victor@test.com"
    assert datos["telefono"] == "600123123"


def test_crear_cliente_sin_telefono(client, auth_headers):
    cliente = {
        "nombre": "Victor",
        "email": "victor@test.com"
    }

    respuesta = client.post(
        "/clientes",
        json=cliente,
        headers=auth_headers
    )

    assert respuesta.status_code == 201

    datos = respuesta.get_json()

    assert datos["nombre"] == "Victor"
    assert datos["email"] == "victor@test.com"
    assert datos["telefono"] == ""


def test_crear_cliente_email_invalido(client, auth_headers):
    cliente = {
        "nombre": "Victor",
        "email": "correo-invalido"
    }

    respuesta = client.post(
        "/clientes",
        json=cliente,
        headers=auth_headers
    )

    assert respuesta.status_code == 400
    assert respuesta.get_json()["error"] == "El campo email no es valido"


def test_obtener_cliente(client, auth_headers):
    creada = client.post(
        "/clientes",
        json={
            "nombre": "Ana",
            "email": "ana@test.com",
            "telefono": "600111222"
        },
        headers=auth_headers
    )

    cliente_id = creada.get_json()["id"]

    respuesta = client.get(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert datos["id"] == cliente_id
    assert datos["nombre"] == "Ana"
    assert datos["email"] == "ana@test.com"
    assert datos["telefono"] == "600111222"


def test_obtener_cliente_inexistente(client, auth_headers):
    respuesta = client.get(
        "/clientes/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404
    assert respuesta.get_json()["error"] == "Cliente no encontrado"


def test_actualizar_cliente(client, auth_headers):
    creada = client.post(
        "/clientes",
        json={
            "nombre": "Ana",
            "email": "ana@test.com",
            "telefono": "600111222"
        },
        headers=auth_headers
    )

    cliente_id = creada.get_json()["id"]

    respuesta = client.put(
        f"/clientes/{cliente_id}",
        json={
            "nombre": "Ana Garcia",
            "email": "ana.garcia@test.com",
            "telefono": "600999888"
        },
        headers=auth_headers
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert datos["id"] == cliente_id
    assert datos["nombre"] == "Ana Garcia"
    assert datos["email"] == "ana.garcia@test.com"
    assert datos["telefono"] == "600999888"


def test_actualizar_cliente_inexistente(client, auth_headers):
    respuesta = client.put(
        "/clientes/9999",
        json={
            "nombre": "Ana",
            "email": "ana@test.com"
        },
        headers=auth_headers
    )

    assert respuesta.status_code == 404
    assert respuesta.get_json()["error"] == "Cliente no encontrado"


def test_eliminar_cliente(client, auth_headers):
    creada = client.post(
        "/clientes",
        json={
            "nombre": "Carlos",
            "email": "carlos@test.com",
            "telefono": "600555444"
        },
        headers=auth_headers
    )

    cliente_id = creada.get_json()["id"]

    respuesta = client.delete(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )

    assert respuesta.status_code == 204

    comprobacion = client.get(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )

    assert comprobacion.status_code == 404


def test_eliminar_cliente_inexistente(client, auth_headers):
    respuesta = client.delete(
        "/clientes/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404
    assert respuesta.get_json()["error"] == "Cliente no encontrado"