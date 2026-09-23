import sqlite3

from app import init_db


def test_init_db_crea_base_de_datos(tmp_path):
    ruta_db = tmp_path / "test.db"

    init_db(ruta_db)

    assert ruta_db.exists()


def test_init_db_crea_tablas(tmp_path):
    ruta_db = tmp_path / "test.db"

    init_db(ruta_db)

    conexion = sqlite3.connect(ruta_db)

    tablas = conexion.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    conexion.close()

    nombres_tablas = [tabla[0] for tabla in tablas]

    assert "usuarios" in nombres_tablas
    assert "tokens" in nombres_tablas
    assert "productos" in nombres_tablas
    assert "clientes" in nombres_tablas


def test_init_db_es_idempotente(tmp_path):
    ruta_db = tmp_path / "test.db"

    init_db(ruta_db)
    init_db(ruta_db)

    assert ruta_db.exists()