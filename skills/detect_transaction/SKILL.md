# Skill: Detect Transaction

## Objetivo

Determinar automáticamente de qué sistema de origen proviene una
transacción cruda (Sistema A, B o C), analizando los nombres de los
campos que trae el diccionario recibido.

## Responsabilidades

- Inspeccionar las claves (nombres de campo) de una transacción cruda.
- Devolver una constante que identifica el sistema de origen.
- Devolver un valor de "origen desconocido" cuando ninguna clave
  conocida está presente, sin lanzar excepciones.

## Lo que esta Skill NO hace

- No transforma ni convierte ningún valor.
- No valida si los datos son correctos o completos.
- No decide si la transacción es válida o inválida.

## Entrada esperada

Un diccionario de Python con los campos crudos de una transacción, en
cualquiera de estas tres formas:

```python
# Sistema A
{"id": "1001", "amount": 250, "currency": "USD", "status": "completed", "date": "2025-06-01"}

# Sistema B
{"transaction": "1002", "value": "350.50", "coin": "US$", "state": "SUCCESS", "created_at": "01/06/2025"}

# Sistema C
{"reference": "1003", "total": 500, "currency_code": "DOLLAR", "status_code": 1, "timestamp": "2025/06/01"}
```

También acepta cualquier otro diccionario (o incluso un valor que no
sea diccionario), devolviendo el origen "desconocido" en ese caso.

## Salida esperada

Un string, una de estas 4 constantes definidas en el propio archivo:

- `SOURCE_A` = `"SYSTEM_A"`
- `SOURCE_B` = `"SYSTEM_B"`
- `SOURCE_C` = `"SYSTEM_C"`
- `SOURCE_UNKNOWN` = `"UNKNOWN"`

## Restricciones

- El criterio de detección se basa únicamente en la presencia del
  campo identificador de cada sistema (`id`, `transaction`,
  `reference`), por ser el único campo garantizado en cada esquema
  según las reglas del desarrollador. No se debe cambiar este criterio
  sin autorización del desarrollador.
- No debe lanzar excepciones ante entradas inesperadas; siempre debe
  devolver `SOURCE_UNKNOWN` en esos casos.

## Ejemplo de uso

```python
from skills.detect_transaction.skill import detect_transaction_source, SOURCE_A

transaction = {"id": "1001", "amount": 250, "currency": "USD", "status": "completed", "date": "2025-06-01"}
source = detect_transaction_source(transaction)
assert source == SOURCE_A
```

## Relación con otras Skills

Es la **primera Skill** del flujo. Su salida (la constante de origen)
es un insumo obligatorio para `normalize_transaction`, que la usa para
decidir cómo mapear los campos de esa transacción en particular.