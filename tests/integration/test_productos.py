# =========================================================
# TESTS DE INTEGRACION - PRODUCTOS
# =========================================================


def test_listar_productos_sin_token(client):
    respuesta = client.get("/productos")

    assert respuesta.status_code == 401
    assert respuesta.get_json()["error"] == "Falta el token de autenticacion"


def test_listar_productos_token_invalido(client):
    respuesta = client.get(
        "/productos",
        headers={"Authorization": "Bearer token-invalido"}
    )

    assert respuesta.status_code == 401
    assert respuesta.get_json()["error"] == "Token invalido o caducado"


def test_listar_productos_vacio(client, auth_headers):
    respuesta = client.get(
        "/productos",
        headers=auth_headers
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json() == []


def test_crear_producto(client, auth_headers):
    producto = {
        "nombre": "Teclado",
        "precio": 29.99,
        "stock": 10
    }

    respuesta = client.post(
        "/productos",
        json=producto,
        headers=auth_headers
    )

    assert respuesta.status_code == 201

    datos = respuesta.get_json()

    assert datos["nombre"] == "Teclado"
    assert datos["precio"] == 29.99
    assert datos["stock"] == 10
    assert "id" in datos


def test_crear_producto_invalido(client, auth_headers):
    producto = {
        "nombre": "Teclado",
        "precio": -10,
        "stock": 5
    }

    respuesta = client.post(
        "/productos",
        json=producto,
        headers=auth_headers
    )

    assert respuesta.status_code == 400
    assert respuesta.get_json()["error"] == \
        "El campo precio debe ser un numero >= 0"


def test_obtener_producto(client, auth_headers):
    producto = {
        "nombre": "Raton",
        "precio": 15.50,
        "stock": 20
    }

    creada = client.post(
        "/productos",
        json=producto,
        headers=auth_headers
    )

    producto_id = creada.get_json()["id"]

    respuesta = client.get(
        f"/productos/{producto_id}",
        headers=auth_headers
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert datos["id"] == producto_id
    assert datos["nombre"] == "Raton"
    assert datos["precio"] == 15.50
    assert datos["stock"] == 20


def test_obtener_producto_inexistente(client, auth_headers):
    respuesta = client.get(
        "/productos/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404
    assert respuesta.get_json()["error"] == "Producto no encontrado"


def test_actualizar_producto(client, auth_headers):
    creada = client.post(
        "/productos",
        json={
            "nombre": "Monitor",
            "precio": 150,
            "stock": 5
        },
        headers=auth_headers
    )

    producto_id = creada.get_json()["id"]

    respuesta = client.put(
        f"/productos/{producto_id}",
        json={
            "nombre": "Monitor 27 pulgadas",
            "precio": 199.99,
            "stock": 3
        },
        headers=auth_headers
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert datos["id"] == producto_id
    assert datos["nombre"] == "Monitor 27 pulgadas"
    assert datos["precio"] == 199.99
    assert datos["stock"] == 3


def test_actualizar_producto_inexistente(client, auth_headers):
    respuesta = client.put(
        "/productos/9999",
        json={
            "nombre": "Monitor",
            "precio": 100,
            "stock": 5
        },
        headers=auth_headers
    )

    assert respuesta.status_code == 404
    assert respuesta.get_json()["error"] == "Producto no encontrado"


def test_eliminar_producto(client, auth_headers):
    creada = client.post(
        "/productos",
        json={
            "nombre": "Webcam",
            "precio": 49.99,
            "stock": 4
        },
        headers=auth_headers
    )

    producto_id = creada.get_json()["id"]

    respuesta = client.delete(
        f"/productos/{producto_id}",
        headers=auth_headers
    )

    assert respuesta.status_code == 204

    comprobacion = client.get(
        f"/productos/{producto_id}",
        headers=auth_headers
    )

    assert comprobacion.status_code == 404


def test_eliminar_producto_inexistente(client, auth_headers):
    respuesta = client.delete(
        "/productos/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404
    assert respuesta.get_json()["error"] == "Producto no encontrado"