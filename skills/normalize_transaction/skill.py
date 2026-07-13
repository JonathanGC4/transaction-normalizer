"""
skills/normalize_transaction/skill.py

Skill: Normalize Transaction.

Responsabilidad unica de esta Skill: convertir una transaccion cruda
(con nombres de campo distintos segun el sistema de origen) al modelo
normalizado unico definido en models/transaction.py:

    {
        "id": "",
        "amount": 0.0,
        "currency": "USD",
        "status": "COMPLETED",
        "date": "YYYY-MM-DD",
        "source": ""
    }

IMPORTANTE: esta Skill solo resuelve el MAPEO ESTRUCTURAL de campos
(renombrar claves segun el sistema de origen). Las conversiones de
valores (normalizar estados, monedas y fechas a su formato final, y
detectar transacciones invalidas) son responsabilidad de la Skill
validate_transaction. Esta Skill NO decide si una transaccion es
valida o invalida.

NOTA: la logica de esta Skill es identica a la que antes vivia en
normalizer.py, en la raiz del proyecto. El unico cambio es de
organizacion: el modelo vacio (EMPTY_TRANSACTION) ya no se define
aqui, sino que se importa desde models/transaction.py, para no
duplicarlo con la Skill validate_transaction.
"""

from skills.detect_transaction.skill import SOURCE_A, SOURCE_B, SOURCE_C
from models.transaction import EMPTY_TRANSACTION


def _map_system_a(transaction: dict) -> dict:
    """Mapea los campos del Sistema A al modelo normalizado (sin transformar valores)."""
    return {
        "id": transaction.get("id"),
        "amount": transaction.get("amount"),
        "currency": transaction.get("currency"),
        "status": transaction.get("status"),
        "date": transaction.get("date"),
    }


def _map_system_b(transaction: dict) -> dict:
    """Mapea los campos del Sistema B al modelo normalizado (sin transformar valores)."""
    return {
        "id": transaction.get("transaction"),
        "amount": transaction.get("value"),
        "currency": transaction.get("coin"),
        "status": transaction.get("state"),
        "date": transaction.get("created_at"),
    }


def _map_system_c(transaction: dict) -> dict:
    """Mapea los campos del Sistema C al modelo normalizado (sin transformar valores)."""
    return {
        "id": transaction.get("reference"),
        "amount": transaction.get("total"),
        "currency": transaction.get("currency_code"),
        "status": transaction.get("status_code"),
        "date": transaction.get("timestamp"),
    }


_MAPPERS = {
    SOURCE_A: _map_system_a,
    SOURCE_B: _map_system_b,
    SOURCE_C: _map_system_c,
}


def normalize_transaction(transaction: dict, source: str) -> dict:
    """
    Convierte una transaccion cruda al modelo normalizado, segun el
    sistema de origen detectado previamente por la Skill
    detect_transaction.
    """
    mapper = _MAPPERS.get(source)

    if mapper is None:
        normalized = dict(EMPTY_TRANSACTION)
    else:
        normalized = mapper(transaction)

    normalized["source"] = source
    return normalized