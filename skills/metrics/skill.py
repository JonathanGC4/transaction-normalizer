"""
skills/metrics/skill.py

Skill: Metrics.

Responsabilidad unica de esta Skill: calcular estadisticas generales
a partir de las transacciones ya procesadas (validas e invalidas).

Esta Skill NO normaliza, NO valida. Solo cuenta y agrupa datos que ya
vienen resueltos por las Skills normalize_transaction y
validate_transaction.

NOTA: el codigo de esta Skill es identico al que antes vivia en
metrics.py, en la raiz del proyecto. Solo cambio su ubicacion.
"""

from collections import Counter


def build_metrics(valid_transactions: list, invalid_transactions: list) -> dict:
    """
    Construye un diccionario con las estadisticas minimas requeridas.
    """
    total_valid = len(valid_transactions)
    total_invalid = len(invalid_transactions)
    total_processed = total_valid + total_invalid

    status_counts = Counter(t["status"] for t in valid_transactions)
    currency_counts = Counter(t["currency"] for t in valid_transactions)

    source_counts = Counter(t["source"] for t in valid_transactions)
    source_counts.update(
        entry["transaction"].get("source") for entry in invalid_transactions
    )

    id_counts = Counter(t["id"] for t in valid_transactions)
    duplicated_ids = [tx_id for tx_id, count in id_counts.items() if count > 1]

    return {
        "total_processed": total_processed,
        "total_valid": total_valid,
        "total_invalid": total_invalid,
        "by_status": dict(status_counts),
        "by_currency": dict(currency_counts),
        "by_source": dict(source_counts),
        "duplicated_ids": duplicated_ids,
    }