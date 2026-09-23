# =========================================================
# TESTS DE INTEGRACION - PERSISTENCIA
# =========================================================


def test_producto_persiste_entre_peticiones(client, auth_headers):
    respuesta_creacion = client.post(
        "/productos",
        json={
            "nombre": "Portatil",
            "precio": 899.99,
            "stock": 3
        },
        headers=auth_headers
    )

    assert respuesta_creacion.status_code == 201

    producto_id = respuesta_creacion.get_json()["id"]

    respuesta_consulta = client.get(
        f"/productos/{producto_id}",
        headers=auth_headers
    )

    assert respuesta_consulta.status_code == 200

    producto = respuesta_consulta.get_json()

    assert producto["nombre"] == "Portatil"
    assert producto["precio"] == 899.99
    assert producto["stock"] == 3


def test_cliente_persiste_entre_peticiones(client, auth_headers):
    respuesta_creacion = client.post(
        "/clientes",
        json={
            "nombre": "Maria",
            "email": "maria@test.com",
            "telefono": "600123456"
        },
        headers=auth_headers
    )

    assert respuesta_creacion.status_code == 201

    cliente_id = respuesta_creacion.get_json()["id"]

    respuesta_consulta = client.get(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )

    assert respuesta_consulta.status_code == 200

    cliente = respuesta_consulta.get_json()

    assert cliente["nombre"] == "Maria"
    assert cliente["email"] == "maria@test.com"
    assert cliente["telefono"] == "600123456"


def test_actualizacion_producto_persiste(client, auth_headers):
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

    actualizada = client.put(
        f"/productos/{producto_id}",
        json={
            "nombre": "Monitor actualizado",
            "precio": 200,
            "stock": 2
        },
        headers=auth_headers
    )

    assert actualizada.status_code == 200

    consulta = client.get(
        f"/productos/{producto_id}",
        headers=auth_headers
    )

    assert consulta.status_code == 200

    producto = consulta.get_json()

    assert producto["nombre"] == "Monitor actualizado"
    assert producto["precio"] == 200
    assert producto["stock"] == 2


def test_eliminacion_producto_persiste(client, auth_headers):
    creada = client.post(
        "/productos",
        json={
            "nombre": "Producto temporal",
            "precio": 10,
            "stock": 1
        },
        headers=auth_headers
    )

    producto_id = creada.get_json()["id"]

    eliminada = client.delete(
        f"/productos/{producto_id}",
        headers=auth_headers
    )

    assert eliminada.status_code == 204

    consulta = client.get(
        f"/productos/{producto_id}",
        headers=auth_headers
    )

    assert consulta.status_code == 404