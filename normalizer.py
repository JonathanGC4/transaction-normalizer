"""
normalizer.py

Responsabilidad unica de este modulo: convertir una transaccion cruda
al modelo normalizado unico usado por el resto del programa:

    {
        "id": "",
        "amount": 0.0,
        "currency": "USD",
        "status": "COMPLETED",
        "date": "YYYY-MM-DD",
        "source": ""
    }

IMPORTANTE: en esta Iteracion 2 solo se resuelve el MAPEO ESTRUCTURAL
de campos (renombrar claves segun el sistema de origen). Las
conversiones de valores (estados, monedas, fechas) y la deteccion de
transacciones invalidas se implementan en la Iteracion 3.
"""

from detector import SOURCE_A, SOURCE_B, SOURCE_C, SOURCE_UNKNOWN

EMPTY_NORMALIZED_TRANSACTION = {
    "id": None,
    "amount": None,
    "currency": None,
    "status": None,
    "date": None,
    "source": None,
}


def _map_system_a(transaction: dict) -> dict:
    return {
        "id": transaction.get("id"),
        "amount": transaction.get("amount"),
        "currency": transaction.get("currency"),
        "status": transaction.get("status"),
        "date": transaction.get("date"),
    }


def _map_system_b(transaction: dict) -> dict:
    return {
        "id": transaction.get("transaction"),
        "amount": transaction.get("value"),
        "currency": transaction.get("coin"),
        "status": transaction.get("state"),
        "date": transaction.get("created_at"),
    }


def _map_system_c(transaction: dict) -> dict:
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
    sistema de origen detectado previamente por detector.py.
    """
    mapper = _MAPPERS.get(source)

    if mapper is None:
        normalized = dict(EMPTY_NORMALIZED_TRANSACTION)
    else:
        normalized = mapper(transaction)

    normalized["source"] = source
    return normalized