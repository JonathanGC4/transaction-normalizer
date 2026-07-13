"""
skills/summary/skill.py

Skill: Summary.

Responsabilidad unica de esta Skill: generar un resumen legible para
el usuario, indicando el total procesado, valido, invalido, y los
valores predominantes (estado, moneda, sistema de origen).

NOTA: a diferencia de las demas Skills, esta es una funcionalidad
NUEVA que no existia en el proyecto original (el menu de 9 opciones
nunca tuvo un "resumen"). Se agrega en esta iteracion porque el
enunciado de la refactorizacion la incluye explicitamente como parte
de la arquitectura y de la personalizacion del agente
(enable_summary).

Decision de diseño: esta Skill calcula sus propios conteos (no
reutiliza la Skill metrics) para que ambas Skills sean completamente
independientes entre si, tal como pide el enunciado.
"""

from collections import Counter


def build_summary(valid_transactions: list, invalid_transactions: list) -> str:
    """
    Construye un resumen legible en texto plano a partir de las
    transacciones ya procesadas.
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

    predominant_status = status_counts.most_common(1)[0][0] if status_counts else "N/A"
    predominant_currency = currency_counts.most_common(1)[0][0] if currency_counts else "N/A"
    predominant_source = source_counts.most_common(1)[0][0] if source_counts else "N/A"

    lines = [
        "===== RESUMEN =====",
        f"Total procesadas: {total_processed}",
        f"Total validas: {total_valid}",
        f"Total invalidas: {total_invalid}",
        f"Estado predominante: {predominant_status}",
        f"Moneda predominante: {predominant_currency}",
        f"Sistema con mas registros: {predominant_source}",
        "====================",
    ]
    return "\n".join(lines)