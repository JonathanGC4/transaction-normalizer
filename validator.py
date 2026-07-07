"""
validator.py

Responsabilidad unica: tomar una transaccion ya mapeada estructuralmente
(salida de normalizer.py) y:

1. Convertir sus valores al formato final del modelo normalizado
   (estado fijo, moneda en codigo fijo, fecha en formato ISO, monto
   como float).
2. Determinar si la transaccion es valida o invalida, segun las
   reglas del desarrollador.

Estas reglas son decisiones explicitas del desarrollador (documentadas
en TECHNICAL_NOTE.md) y no deben modificarse sin su autorizacion:

    - Estados validos: COMPLETED, PENDING, FAILED
    - Monedas validas: USD, EUR, GTQ
    - Fechas: formato final YYYY-MM-DD, validado con datetime.strptime
    - Una transaccion es invalida si: falta el id, falta el monto, el
      monto no es numerico, la moneda no es soportada, el estado no
      puede convertirse, la fecha es invalida, o falta la fecha.
"""

import json
import os
from datetime import datetime

import config


class ValidationResult:
    """
    Representa el resultado de validar una transaccion.

    Se usa una clase pequena en lugar de una tupla para que el codigo
    que la consume sea mas legible: result.is_valid, result.transaction,
    result.error, en vez de indices sin nombre.
    """

    def __init__(self, transaction: dict, is_valid: bool, error: str = None):
        self.transaction = transaction
        self.is_valid = is_valid
        self.error = error


def _load_json_config(file_name: str):
    """Carga un archivo de configuracion JSON desde la carpeta configs/."""
    path = os.path.join(config.CONFIGS_DIR, file_name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


_STATUS_MAPPING = _load_json_config("status_mapping.json")
_CURRENCY_MAPPING = _load_json_config("currency_mapping.json")
_SUPPORTED_DATE_FORMATS = _load_json_config("supported_formats.json")

VALID_STATUSES = {"COMPLETED", "PENDING", "FAILED"}
VALID_CURRENCIES = {"USD", "EUR", "GTQ"}


def _convert_status(raw_status):
    """
    Convierte un estado crudo (texto o codigo numerico) a uno de los
    estados validos, usando configs/status_mapping.json.
    """
    if raw_status is None:
        return None

    key = str(raw_status).strip().lower()
    return _STATUS_MAPPING.get(key)


def _convert_currency(raw_currency):
    """
    Convierte una moneda cruda a uno de los codigos validos, usando
    configs/currency_mapping.json.
    """
    if raw_currency is None:
        return None

    key = str(raw_currency).strip().lower()
    return _CURRENCY_MAPPING.get(key)


def _convert_date(raw_date):
    """
    Convierte una fecha cruda (en cualquiera de los formatos listados
    en configs/supported_formats.json) al formato final YYYY-MM-DD.
    """
    if not raw_date:
        return None

    raw_date = str(raw_date).strip()

    for date_format in _SUPPORTED_DATE_FORMATS:
        try:
            parsed_date = datetime.strptime(raw_date, date_format)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def _convert_amount(raw_amount):
    """Convierte un monto crudo (numero o texto) a float."""
    if raw_amount is None:
        return None

    try:
        return float(raw_amount)
    except (TypeError, ValueError):
        return None


def validate_transaction(mapped_transaction: dict) -> ValidationResult:
    """
    Valida y convierte una transaccion ya mapeada estructuralmente.

    El orden de verificacion sigue el orden en que el desarrollador
    definio los casos de transaccion invalida: identificador, monto,
    fecha, moneda y finalmente estado.
    """
    transaction_id = mapped_transaction.get("id")
    if not transaction_id:
        return ValidationResult(mapped_transaction, False, "Falta el identificador")

    raw_amount = mapped_transaction.get("amount")
    if raw_amount is None:
        return ValidationResult(mapped_transaction, False, "Falta el monto")
    amount = _convert_amount(raw_amount)
    if amount is None:
        return ValidationResult(mapped_transaction, False, "El monto no es numerico")

    raw_date = mapped_transaction.get("date")
    if not raw_date:
        return ValidationResult(mapped_transaction, False, "Falta la fecha")
    date = _convert_date(raw_date)
    if date is None:
        return ValidationResult(mapped_transaction, False, "La fecha es invalida")

    currency = _convert_currency(mapped_transaction.get("currency"))
    if currency is None:
        return ValidationResult(mapped_transaction, False, "La moneda no es soportada")

    status = _convert_status(mapped_transaction.get("status"))
    if status is None:
        return ValidationResult(mapped_transaction, False, "El estado no puede convertirse")

    final_transaction = {
        "id": str(transaction_id),
        "amount": amount,
        "currency": currency,
        "status": status,
        "date": date,
        "source": mapped_transaction.get("source"),
    }

    return ValidationResult(final_transaction, True, None)