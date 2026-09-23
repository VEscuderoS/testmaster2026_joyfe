from app import validar_registro, validar_producto, validar_cliente

# =========================================================
# TESTS validar_registro
# =========================================================

def test_validar_registro_correcto():
    datos = {
        "username": "victor",
        "password": "1234"
    }

    assert validar_registro(datos) is None


def test_validar_registro_cuerpo_invalido():
    assert validar_registro("datos") == "Cuerpo de la peticion invalido"


def test_validar_registro_sin_username():
    datos = {
        "password": "1234"
    }

    assert validar_registro(datos) == "El campo username es obligatorio"


def test_validar_registro_username_invalido():
    datos = {
        "username": 123,
        "password": "1234"
    }

    assert validar_registro(datos) == "El campo username es obligatorio"


def test_validar_registro_sin_password():
    datos = {
        "username": "victor"
    }

    assert validar_registro(datos) == "El campo password debe tener al menos 4 caracteres"


def test_validar_registro_password_corta():
    datos = {
        "username": "victor",
        "password": "123"
    }

    assert validar_registro(datos) == "El campo password debe tener al menos 4 caracteres"


def test_validar_registro_password_invalida():
    datos = {
        "username": "victor",
        "password": 1234
    }

    assert validar_registro(datos) == "El campo password debe tener al menos 4 caracteres"
# =========================================================
# TESTS validar_producto
# =========================================================

def test_validar_producto_correcto():
    producto = {
        "nombre": "Teclado",
        "precio": 25.50,
        "stock": 10
    }

    assert validar_producto(producto) is None


def test_validar_producto_cuerpo_invalido():
    assert validar_producto("producto") == "Cuerpo de la peticion invalido"


def test_validar_producto_sin_nombre():
    producto = {
        "precio": 25.50,
        "stock": 10
    }

    assert validar_producto(producto) == "El campo nombre es obligatorio"


def test_validar_producto_precio_negativo():
    producto = {
        "nombre": "Teclado",
        "precio": -5,
        "stock": 10
    }

    assert validar_producto(producto) == "El campo precio debe ser un numero >= 0"


def test_validar_producto_precio_invalido():
    producto = {
        "nombre": "Teclado",
        "precio": "barato",
        "stock": 10
    }

    assert validar_producto(producto) == "El campo precio debe ser un numero >= 0"


def test_validar_producto_stock_negativo():
    producto = {
        "nombre": "Teclado",
        "precio": 25.50,
        "stock": -1
    }

    assert validar_producto(producto) == "El campo stock debe ser un entero >= 0"


def test_validar_producto_stock_invalido():
    producto = {
        "nombre": "Teclado",
        "precio": 25.50,
        "stock": "diez"
    }

    assert validar_producto(producto) == "El campo stock debe ser un entero >= 0"


# =========================================================
# TESTS validar_cliente
# =========================================================

def test_validar_cliente_correcto():
    cliente = {
        "nombre": "Victor",
        "email": "victor@test.com"
    }

    assert validar_cliente(cliente) is None


def test_validar_cliente_cuerpo_invalido():
    assert validar_cliente("cliente") == "Cuerpo de la peticion invalido"


def test_validar_cliente_sin_nombre():
    cliente = {
        "email": "victor@test.com"
    }

    assert validar_cliente(cliente) == "El campo nombre es obligatorio"


def test_validar_cliente_sin_email():
    cliente = {
        "nombre": "Victor"
    }

    assert validar_cliente(cliente) == "El campo email no es valido"


def test_validar_cliente_email_invalido():
    cliente = {
        "nombre": "Victor",
        "email": "esto-no-es-un-email"
    }

    assert validar_cliente(cliente) == "El campo email no es valido"
    
