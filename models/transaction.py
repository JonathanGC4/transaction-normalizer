"""
models/transaction.py

Define el modelo de datos normalizado que usa todo el sistema.

Esta es una decision del desarrollador y no debe modificarse sin su
autorizacion. Antes de esta iteracion, la forma del modelo
(EMPTY_NORMALIZED_TRANSACTION) vivia dentro de normalizer.py, y los
valores validos (VALID_STATUSES, VALID_CURRENCIES) vivian dentro de
validator.py, duplicando el concepto de "modelo" en dos lugares. Se
centralizan aqui para que ambas Skills (normalize_transaction y
validate_transaction) usen la misma referencia unica.

Esto es un cambio de ORGANIZACION del codigo, no de comportamiento: el
modelo, los estados y las monedas validas son exactamente los mismos
que ya estaban definidos.
"""

EMPTY_TRANSACTION = {
    "id": None,
    "amount": None,
    "currency": None,
    "status": None,
    "date": None,
    "source": None,
}

VALID_STATUSES = {"COMPLETED", "PENDING", "FAILED"}
VALID_CURRENCIES = {"USD", "EUR", "GTQ"}