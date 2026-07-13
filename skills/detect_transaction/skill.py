"""
skills/detect_transaction/skill.py

Skill: Detect Transaction.

Responsabilidad unica de esta Skill: mirar las claves (nombres de
campo) de una transaccion cruda y determinar de que sistema de origen
proviene (A, B o C), en base a la forma de sus campos.

Esta Skill NO transforma valores, NO valida datos. Solo identifica
el "esquema" de la transaccion para que la Skill normalize_transaction
sepa como mapear cada campo.

NOTA: el codigo de esta Skill es identico al que antes vivia en
detector.py, en la raiz del proyecto. Solo cambio su ubicacion (ahora
es una Skill independiente y documentada), no su funcionalidad.
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

    Args:
        transaction: diccionario con los datos crudos de la transaccion.

    Returns:
        Una de las constantes SOURCE_A, SOURCE_B, SOURCE_C o
        SOURCE_UNKNOWN si no coincide con ningun esquema conocido.
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