# Skill: Metrics

## Objetivo

Calcular estadísticas generales sobre el conjunto de transacciones ya
procesadas (válidas e inválidas).

## Responsabilidades

- Calcular el total de transacciones procesadas, válidas e inválidas.
- Contar transacciones válidas agrupadas por estado.
- Contar transacciones válidas agrupadas por moneda.
- Contar transacciones (válidas e inválidas) agrupadas por sistema de
  origen.
- Detectar identificadores repetidos entre las transacciones válidas.

## Lo que esta Skill NO hace

- No normaliza ni valida ningún dato; solo cuenta y agrupa datos que
  ya fueron resueltos por `validate_transaction`.
- No decide si el resultado se muestra, se exporta o se resume; solo
  calcula y devuelve los números.

## Entrada esperada

- `valid_transactions`: lista de transacciones ya normalizadas y
  válidas (salida de `validate_transaction`).
- `invalid_transactions`: lista de diccionarios
  `{"transaction": ..., "error": ...}` con las transacciones que no
  pasaron la validación.

## Salida esperada

Un diccionario:

```python
{
    "total_processed": int,
    "total_valid": int,
    "total_invalid": int,
    "by_status": {"COMPLETED": int, ...},
    "by_currency": {"USD": int, ...},
    "by_source": {"SYSTEM_A": int, ...},
    "duplicated_ids": ["id1", "id2", ...],
}
```

## Restricciones

- Los conteos por estado y por moneda se calculan **solo** sobre las
  transacciones válidas, ya que son las únicas con esos campos
  normalizados de forma confiable.
- El conteo por sistema de origen sí incluye tanto válidas como
  inválidas, ya que el origen se puede detectar aunque la transacción
  termine siendo inválida por otro motivo.

## Ejemplo de uso

```python
from skills.metrics.skill import build_metrics

metrics = build_metrics(valid_transactions, invalid_transactions)
print(metrics["total_processed"])
```

## Relación con otras Skills

Recibe su entrada de `validate_transaction` (a través del Agente). Es
independiente de `export_json` y `summary`: ninguna de las tres se
necesita entre sí para funcionar, cada una puede habilitarse o
deshabilitarse sin afectar a las demás.