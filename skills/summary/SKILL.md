# Skill: Summary

## Objetivo

Generar un resumen legible en texto plano del resultado de una
ejecución del sistema, para que el usuario entienda de un vistazo qué
se procesó, sin tener que leer el detalle transacción por transacción.

## Responsabilidades

- Calcular el total de transacciones procesadas, válidas e inválidas.
- Determinar el estado predominante entre las transacciones válidas.
- Determinar la moneda predominante entre las transacciones válidas.
- Determinar el sistema de origen con más registros (válidos e
  inválidos).
- Devolver todo esto como un string formateado, listo para imprimir.

## Lo que esta Skill NO hace

- No normaliza ni valida ningún dato.
- No reutiliza los cálculos de la Skill `metrics`: calcula sus propios
  conteos de forma independiente, para que ambas Skills puedan
  habilitarse o deshabilitarse por separado sin depender una de otra.

## Nota sobre el origen de esta Skill

A diferencia de las otras cinco, esta Skill **no proviene de ningún
módulo del proyecto original** (el menú de 9 opciones nunca tuvo un
"resumen"). Se agregó durante la refactorización porque el enunciado
la incluye explícitamente en la arquitectura y en el ejemplo de
personalización del Agente (`enable_summary`).

## Entrada esperada

- `valid_transactions`: lista de transacciones normalizadas y
  válidas.
- `invalid_transactions`: lista de diccionarios
  `{"transaction": ..., "error": ...}`.

## Salida esperada

Un string de varias líneas, por ejemplo: