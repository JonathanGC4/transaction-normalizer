"""
skills/export_json/skill.py

Skill: Export JSON.

Responsabilidad unica de esta Skill: escribir las transacciones ya
normalizadas (validas) a un archivo JSON en disco.

Esta Skill NO decide que transacciones exportar (eso lo decide quien
la llama, normalmente el Agente pasando sus transacciones validas), y
NO conoce nada sobre como se llego a esos datos.

NOTA: el codigo de esta Skill es identico al que antes vivia en
exporter.py, en la raiz del proyecto. Solo cambio su ubicacion.
"""

import json
import os


class ExportError(Exception):
    """Excepcion propia para errores al exportar el archivo."""
    pass


def export_transactions(transactions: list, output_path: str) -> None:
    """
    Escribe la lista de transacciones normalizadas en un archivo JSON.
    """
    output_dir = os.path.dirname(output_path)

    try:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transactions, f, indent=4, ensure_ascii=False)

    except OSError as error:
        raise ExportError(f"No se pudo exportar el archivo: {error}") from error