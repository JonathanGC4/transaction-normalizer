"""
detector.py

Responsabilidad unica de este modulo: mirar las claves (nombres de
campo) de una transaccion cruda y determinar de que sistema de origen
proviene (A, B o C), en base a la forma de sus campos.

Este modulo NO transforma valores, NO valida datos. Solo identifica
el "esquema" de la transaccion para que normalizer.py sepa como
mapear cada campo.
"""

SOURCE_A = "SYSTEM_A"
SOURCE_B = "SYSTEM_B"
SOURCE_C = "SYSTEM_C"
SOURCE_UNKNOWN = "UNKNOWN"

_SYSTEM_A_KEYS = {"id", "amount", "currency", "status", "date"}
_SYSTEM_B_KEYS = {"transaction", "value", "coin", "state", "created_at"}
_SYSTEM_C_KEYS = {"reference", "total", "currency_code", "status_code", "timestamp"}


def detect_transaction_source(transaction: dict) -> str:
    """
    Determina el sistema de origen de una transaccion cruda, en base
    a las claves presentes en el diccionario.
    """
    if not isinstance(transaction, dict):
        return SOURCE_UNKNOWN

    keys = set(transaction.keys())

    if "id" in keys:
        return SOURCE_A
    if "transaction" in keys:
        return SOURCE_B
    if "reference" in keys:
        return SOURCE_C

    return SOURCE_UNKNOWN