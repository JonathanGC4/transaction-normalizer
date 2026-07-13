# Skill: Normalize Transaction

## Objetivo

Convertir una transacción cruda (con nombres de campo distintos según
el sistema de origen) al modelo de datos normalizado único usado por
el resto del sistema, definido en `models/transaction.py`.

## Responsabilidades

- Recibir una transacción cruda y el origen ya detectado por la Skill
  `detect_transaction`.
- Renombrar (mapear) cada campo crudo a su campo equivalente en el
  modelo normalizado: `id`, `amount`, `currency`, `status`, `date`.
- Agregar el campo `source` con el origen recibido.
- Si el origen es desconocido, devolver la estructura vacía del
  modelo (todos los campos en `None`), para que la Skill
  `validate_transaction` la trate como inválida por falta de datos.

## Lo que esta Skill NO hace

- No convierte valores (no traduce estados, monedas ni fechas a su
  formato final). Esa es responsabilidad exclusiva de la Skill
  `validate_transaction`.
- No valida ni decide si la transacción es válida o inválida.

## Entrada esperada

- `transaction`: diccionario crudo (la misma entrada que recibió
  `detect_transaction`).
- `source`: uno de los valores devueltos por
  `detect_transaction_source` (`SOURCE_A`, `SOURCE_B`, `SOURCE_C` o
  `SOURCE_UNKNOWN`).

## Salida esperada

Un diccionario con exactamente estas claves, con los valores **aún
sin convertir** (tal como venían en el archivo original):

```python
{
    "id": ...,
    "amount": ...,
    "currency": ...,
    "status": ...,
    "date": ...,
    "source": "SYSTEM_A",  # o el origen que corresponda
}
```

## Restricciones

- El mapeo de campos por sistema es una decisión del desarrollador y
  no debe modificarse sin su autorización:

| Campo normalizado | Sistema A | Sistema B | Sistema C |
|---|---|---|---|
| id | id | transaction | reference |
| amount | amount | value | total |
| currency | currency | coin | currency_code |
| status | status | state | status_code |
| date | date | created_at | timestamp |

- Debe usar `models.transaction.EMPTY_TRANSACTION` como base cuando el
  origen es desconocido, en vez de definir su propia estructura vacía,
  para no duplicar el modelo.

## Ejemplo de uso

```python
from skills.detect_transaction.skill import SOURCE_A
from skills.normalize_transaction.skill import normalize_transaction

raw = {"id": "1001", "amount": 250, "currency": "USD", "status": "completed", "date": "2025-06-01"}
mapped = normalize_transaction(raw, SOURCE_A)
assert mapped == {
    "id": "1001", "amount": 250, "currency": "USD",
    "status": "completed", "date": "2025-06-01", "source": "SYSTEM_A",
}
```

## Relación con otras Skills

Se ejecuta **siempre después** de `detect_transaction` (necesita su
resultado) y **siempre antes** de `validate_transaction` (le entrega
la transacción ya mapeada estructuralmente, para que esta ultima
convierta los valores y decida su validez).