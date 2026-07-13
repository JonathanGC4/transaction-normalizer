# Skill: Export JSON

## Objetivo

Escribir las transacciones normalizadas y válidas en un archivo JSON
dentro de la carpeta `output/`.

## Responsabilidades

- Crear la carpeta de destino si no existe.
- Serializar la lista de transacciones a JSON, con indentación
  legible.
- Reportar un error claro si no se pudo escribir el archivo (por
  ejemplo, por permisos insuficientes).

## Lo que esta Skill NO hace

- No decide qué transacciones exportar; eso lo decide quien la llama
  (el Agente le pasa explícitamente qué lista exportar).
- No valida ni transforma los datos: exporta las transacciones tal
  como las recibe.

## Entrada esperada

- `transactions`: lista de transacciones normalizadas (normalmente,
  las transacciones válidas).
- `output_path`: ruta del archivo de salida (ejemplo:
  `output/normalized.json`).

## Salida esperada

No devuelve ningún valor. Como efecto, crea (o sobrescribe) el archivo
indicado en `output_path` con el contenido de `transactions` en
formato JSON.

## Restricciones

- Solo debe exportar transacciones que ya cumplan el modelo
  normalizado; es decisión del Agente pasarle únicamente
  `valid_transactions`.
- Debe lanzar `ExportError` (no dejar propagar excepciones genéricas
  de `OSError`) para que quien la use pueda manejar el error de forma
  consistente.

## Ejemplo de uso

```python
from skills.export_json.skill import export_transactions, ExportError

try:
    export_transactions(valid_transactions, "output/normalized.json")
except ExportError as error:
    print(f"No se pudo exportar: {error}")
```

## Relación con otras Skills

Recibe su entrada de `validate_transaction` (a través del Agente).
Es independiente de `metrics` y `summary`.