# Transaction Normalizer

Aplicacion de consola (CLI) en Python que normaliza transacciones
provenientes de multiples sistemas de origen, cada uno con su propio
formato de campos, y permite explorarlas mediante un menu interactivo.

Este proyecto es un ejercicio academico cuyo objetivo es demostrar el
uso de la Inteligencia Artificial como herramienta de apoyo al
desarrollo (vibecoding), no como reemplazo del criterio del
desarrollador. Todas las reglas de negocio (modelo de datos, mapeos
de estado/moneda, criterios de invalidez) fueron decididas por el
desarrollador; el detalle de cada decision esta documentado en
`TECHNICAL_NOTE.md`.

## Requisitos

- Python 3.8 o superior.
- No requiere librerias externas (ver `requirements.txt`).

## Como ejecutar

Desde la carpeta raiz del proyecto:

    python main.py

Se abrira un menu interactivo:

    ==========================================
    TRANSACTION NORMALIZER
    ==========================================

    1. Cargar archivo JSON
    2. Mostrar todas las transacciones
    3. Mostrar transacciones validas
    4. Mostrar transacciones invalidas
    5. Filtrar por estado
    6. Filtrar por moneda
    7. Mostrar estadisticas
    8. Exportar datos normalizados
    9. Salir

Escribe el numero de la opcion deseada y presiona Enter. El programa
vuelve al menu despues de cada accion, hasta que eliges "9. Salir".

## Archivos de datos de prueba incluidos

- `data/transactions_good.json`: 3 transacciones validas, una de cada
  sistema de origen (A, B y C).
- `data/transactions_bad.json`: 9 transacciones, 8 invalidas (una por
  cada motivo de invalidez posible) y 1 valida con monto negativo.
- `data/transactions_mixed.json`: mezcla de validas e invalidas para
  probar el flujo completo.

## Sistemas de origen soportados

| Sistema | Campos crudos |
|---|---|
| A | id, amount, currency, status, date |
| B | transaction, value, coin, state, created_at |
| C | reference, total, currency_code, status_code, timestamp |

## Modelo normalizado (formato final)

```json
{
    "id": "",
    "amount": 0.0,
    "currency": "USD",
    "status": "COMPLETED",
    "date": "YYYY-MM-DD",
    "source": ""
}
```

## Estructura del proyecto