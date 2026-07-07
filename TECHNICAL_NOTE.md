# Nota Tecnica — Transaction Normalizer

Este documento registra las decisiones tecnicas y de negocio tomadas
por el desarrollador durante la construccion de Transaction
Normalizer. El objetivo es dejar explicito que el modelo de datos, las
reglas de normalizacion y los criterios de validacion son decisiones
del desarrollador, no de la IA usada como asistente.

## 1. Arquitectura

El proyecto se dividio en modulos con una sola responsabilidad cada
uno:

- `file_manager.py`: solo lee archivos del disco y los convierte en
  listas de diccionarios. No conoce el modelo normalizado.
- `detector.py`: solo determina el sistema de origen de una
  transaccion cruda, en base a sus claves.
- `normalizer.py`: solo hace el mapeo ESTRUCTURAL (renombrar campos)
  segun el sistema detectado. No transforma valores.
- `validator.py`: convierte los valores (estado, moneda, fecha, monto)
  al formato final y decide si la transaccion es valida o invalida.
- `metrics.py`: calcula estadisticas sobre datos ya procesados.
- `exporter.py`: escribe el resultado final a un archivo JSON.
- `interface.py`: unicamente presentacion (menu, mensajes en
  pantalla). No contiene logica de negocio.
- `main.py`: orquesta el flujo y mantiene el estado en memoria
  (`AppState`).

Esta separacion se eligio para que cada archivo se pueda leer,
probar y modificar de forma aislada, y para que agregar un nuevo
sistema de origen o una nueva regla de validacion no obligue a tocar
modulos que no tienen relacion con ese cambio.

## 2. Modelo normalizado (decision del desarrollador)

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

Este es el unico formato que usa el resto del programa a partir de
`validator.py` en adelante.

## 3. Estados validos (decision del desarrollador)

Unicos estados de salida permitidos: `COMPLETED`, `PENDING`, `FAILED`.

El mapeo de texto crudo a estado final vive en
`configs/status_mapping.json`, para poder ajustarlo sin tocar codigo:

| Entrada | Salida |
|---|---|
| completed, success, ok | COMPLETED |
| pending, waiting | PENDING |
| error, failed | FAILED |

**Asuncion que requiere confirmacion del desarrollador:** el Sistema C
envia `status_code` como numero (ejemplo: `1`). El enunciado original
no especifico la equivalencia numerica, asi que se asumio, a modo de
ejemplo, `1 = COMPLETED`, `0 = PENDING`, `-1 = FAILED`. Esta
equivalencia debe ser revisada y confirmada (o corregida) por el
desarrollador en `configs/status_mapping.json`.

## 4. Monedas validas (decision del desarrollador)

Unicas monedas de salida permitidas: `USD`, `EUR`, `GTQ`.

El mapeo vive en `configs/currency_mapping.json`:

| Entrada | Salida |
|---|---|
| us$, usd, dollar | USD |
| euro, eur, € | EUR |
| gtq, quetzal, q | GTQ |

## 5. Fechas

Formato final: `YYYY-MM-DD`. La conversion se hace probando, en
orden, los formatos definidos en `configs/supported_formats.json`
(`%Y-%m-%d`, `%d/%m/%Y`, `%Y/%m/%d`), usando `datetime.strptime()`
para la validacion real (no expresiones regulares), tal como lo pidio
el desarrollador.

## 6. Criterios de transaccion invalida (decision del desarrollador)

Una transaccion se marca como invalida, y NO detiene el programa, si
ocurre cualquiera de estos casos (verificados en este orden en
`validator.validate_transaction`):

1. Falta el identificador.
2. Falta el monto.
3. Falta la fecha.
4. La fecha es invalida (no coincide con ningun formato soportado).
5. La moneda no es soportada.
6. El estado no puede convertirse.
7. El monto no es numerico.

**Decision pendiente de confirmar por el desarrollador:** los montos
negativos (ejemplo: `-50`) actualmente se aceptan como validos, ya
que el enunciado original no los incluyo explicitamente en la lista
de criterios de invalidez (solo pidio "contemplar" ese caso borde sin
que el programa se caiga, lo cual si se cumple). Si el criterio de
negocio es que un monto negativo deba ser invalido, ese cambio debe
agregarse explicitamente en `validator.py`.

## 7. Casos borde contemplados

| Caso | Manejo |
|---|---|
| Archivo vacio (0 bytes) | `FileReadError` especifico, no crashea |
| JSON invalido | `FileReadError` especifico, no crashea |
| Lista vacia de transacciones | Se procesa sin error, 0 validas y 0 invalidas |
| Campos faltantes | Transaccion marcada invalida con motivo |
| Moneda desconocida | Transaccion marcada invalida |
| Estado desconocido | Transaccion marcada invalida |
| Fecha imposible / con formato no soportado | Transaccion marcada invalida |
| Monto negativo | Aceptado como valido (ver punto 6) |
| Monto con formato incorrecto | Transaccion marcada invalida |
| Identificadores repetidos | Detectados y reportados en las estadisticas (opcion 7) |
| Sistema de origen desconocido | `detector.py` devuelve `UNKNOWN`; `normalizer.py` devuelve campos vacios; `validator.py` la marca invalida por falta de identificador |

## 8. Lo que la IA propuso vs. lo que decidio el desarrollador

La IA (usada como asistente durante el desarrollo) propuso:

- Estructura de modulos y nombres de funciones.
- Implementacion de la logica de lectura de archivos, deteccion,
  mapeo, conversion de tipos y presentacion en consola.
- Manejo de excepciones y mensajes de error.

El desarrollador decidio y esta nota lo documenta explicitamente:

- El modelo de datos final (seccion 2).
- Los estados y monedas validos, y sus equivalencias (secciones 3 y 4).
- El formato de fecha final y la libreria de validacion a usar.
- Los criterios exactos de que hace invalida una transaccion
  (seccion 6), incluyendo las dos decisiones marcadas como
  "pendientes de confirmar" arriba, que quedan abiertas
  intencionalmente para que el desarrollador las cierre con su
  propio criterio.