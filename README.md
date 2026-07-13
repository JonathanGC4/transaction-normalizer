# Transaction Normalizer — Sistema Agéntico con Skills

Aplicación de consola (CLI) en Python que normaliza transacciones
provenientes de múltiples sistemas de origen y permite explorarlas de
forma interactiva.

Esta es la **versión refactorizada** del proyecto académico original
`Transaction Normalizer`. Conserva exactamente la misma funcionalidad
que la versión original, pero reorganizada bajo una arquitectura de
**Agente + Skills**, donde `agent.py` coordina el flujo y cada
responsabilidad de negocio vive en su propia Skill independiente,
documentada con su propio `SKILL.md`.

Para el detalle completo de qué cambió, por qué, y cómo se usó la IA
como asistente durante la refactorización, ver `docs/TECHNICAL_NOTE.md`.

## Requisitos

- Python 3.8 o superior.
- No requiere librerías externas (ver `requirements.txt`).

## Cómo ejecutar

Desde la raíz del proyecto:

    python main.py

Al iniciar, el programa pregunta qué Skills opcionales quieres
habilitar para esa ejecución:

    Configuracion del Agente para esta ejecucion:
      Habilitar validacion de transacciones (s/n):
      Habilitar calculo de estadisticas (s/n):
      Habilitar exportacion a JSON (s/n):
      Habilitar generacion de resumen (s/n):

Después se abre el menú interactivo:

    ==========================================
    TRANSACTION NORMALIZER (Agente + Skills)
    ==========================================

    1. Cargar archivo JSON
    2. Mostrar todas las transacciones
    3. Mostrar transacciones validas
    4. Mostrar transacciones invalidas
    5. Filtrar por estado
    6. Filtrar por moneda
    7. Mostrar estadisticas
    8. Exportar datos normalizados
    9. Mostrar resumen
    10. Salir

Si eliges "n" para alguna Skill al iniciar, la opción de menú
correspondiente sigue apareciendo, pero muestra un mensaje indicando
que esa Skill está deshabilitada en vez de ejecutarse.

## Arquitectura