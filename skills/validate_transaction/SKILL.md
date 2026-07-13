# Skill: Validate Transaction

## Objetivo

Convertir los valores de una transacción ya mapeada estructuralmente
a su formato final (estado, moneda, fecha, monto), y determinar si la
transacción es válida o inválida según las reglas del desarrollador.

## Responsabilidades

- Convertir el estado crudo a uno de: `COMPLETED`, `PENDING`, `FAILED`
  (usando `configs/status_mapping.json`).
- Convertir la moneda cruda a uno de: `USD`, `EUR`, `GTQ` (usando
  `configs/currency_mapping.json`).
- Convertir la fecha cruda al formato `YYYY-MM-DD`, validando con
  `datetime.strptime()` contra los formatos definidos en
  `configs/supported_formats.json`.
- Convertir el monto crudo a `float`.
- Determinar si la transacción es válida o inválida, y en caso de ser
  inválida, indicar el motivo exacto.

## Lo que esta Skill NO hace

- No detecta el sistema de origen (responsabilidad de
  `detect_transaction`).
- No hace el mapeo estructural de campos (responsabilidad de
  `normalize_transaction`).
- No detiene la ejecución del programa ante una transacción inválida;
  simplemente la reporta como tal.

## Entrada esperada

Un diccionario con la forma de salida de `normalize_transaction`:
`id`, `amount`, `currency`, `status`, `date`, `source`, con los
valores aún sin convertir.

## Salida esperada

Una instancia de `ValidationResult`, con tres atributos:

- `transaction`: si es válida, el diccionario final ya convertido
  (`amount` como `float`, `status`/`currency`/`date` en su formato
  final). Si es inválida, la transacción mapeada tal como llegó (sin
  convertir).
- `is_valid`: `True` o `False`.
- `error`: `None` si es válida, o un string con el motivo si es
  inválida.

## Restricciones (reglas del desarrollador, no modificables por la IA)

Una transacción es inválida si ocurre, en este orden de verificación,
cualquiera de estos casos:

1. Falta el identificador.
2. Falta el monto.
3. Falta la fecha.
4. La fecha es inválida (no coincide con ningún formato soportado).
5. La moneda no es soportada.
6. El estado no puede convertirse.
7. El monto no es numérico.

Nota documentada: los montos negativos actualmente se aceptan como
válidos (no están en la lista de criterios de invalidez de arriba);
es una decisión pendiente de confirmar por el desarrollador, señalada
también en `TECHNICAL_NOTE.md`.

## Ejemplo de uso

```python
from skills.validate_transaction.skill import validate_transaction

mapped = {
    "id": "1001", "amount": 250, "currency": "USD",
    "status": "completed", "date": "2025-06-01", "source": "SYSTEM_A",
}
result = validate_transaction(mapped)
assert result.is_valid is True
assert result.transaction["status"] == "COMPLETED"
```

## Relación con otras Skills

Recibe su entrada de `normalize_transaction`. Su salida (transacciones
finales, ya sea válidas o inválidas con su motivo) es el insumo de
`metrics`, `export_json` y `summary`.