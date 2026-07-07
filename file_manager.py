"""
file_manager.py

Responsabilidad unica de este modulo: leer archivos del disco y
convertirlos en estructuras de datos de Python (listas de diccionarios).

Este modulo NO normaliza, NO valida el contenido de las transacciones,
y NO conoce nada sobre el modelo normalizado.
"""

import json
import os


class FileReadError(Exception):
    """Excepcion propia para errores al leer el archivo."""
    pass


def load_transactions_file(file_path: str) -> list:
    """
    Lee un archivo JSON y devuelve su contenido como una lista de
    transacciones (lista de diccionarios).
    """
    if not os.path.isfile(file_path):
        raise FileReadError(f"El archivo no existe: {file_path}")

    if os.path.getsize(file_path) == 0:
        raise FileReadError(f"El archivo esta vacio: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)
    except json.JSONDecodeError as error:
        raise FileReadError(
            f"El archivo no contiene JSON valido: {error}"
        ) from error
    except OSError as error:
        raise FileReadError(
            f"No se pudo abrir el archivo: {error}"
        ) from error

    if not isinstance(content, list):
        raise FileReadError(
            "El archivo JSON debe contener una lista de transacciones "
            f"(se encontro un tipo '{type(content).__name__}')."
        )

    return content