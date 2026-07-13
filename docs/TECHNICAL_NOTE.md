# Nota Técnica — Refactorización a Sistema Agéntico con Skills

Este documento explica la refactorización de `Transaction Normalizer`
desde su arquitectura tradicional (módulos llamados directamente
desde `main.py`) hacia una arquitectura de **Agente + Skills**.

## 1. Qué partes del proyecto fueron refactorizadas

| Antes | Después |
|---|---|
| `main.py` llamaba directamente a `detector.py`, `normalizer.py`, `validator.py`, `metrics.py`, `exporter.py` | `main.py` solo habla con `agent.py`; el Agente coordina las Skills |
| `detector.py` (raíz) | `skills/detect_transaction/skill.py` |
| `normalizer.py` (raíz) | `skills/normalize_transaction/skill.py` |
| `validator.py` (raíz) | `skills/validate_transaction/skill.py` |
| `metrics.py` (raíz) | `skills/metrics/skill.py` |
| `exporter.py` (raíz) | `skills/export_json/skill.py` |
| Modelo normalizado duplicado dentro de `normalizer.py` y `validator.py` | Modelo unificado en `models/transaction.py` |
| Sin personalización | `TransactionAgent(enable_validation, enable_metrics, enable_export, enable_summary)` cambia realmente el comportamiento |
| Sin resumen | Skill nueva: `skills/summary/skill.py` |

`config.py`, `file_manager.py` e `interface.py` **no se movieron ni se
convirtieron en Skills**, porque son infraestructura o presentación,
no lógica de negocio (ver punto 2).

## 2. Qué responsabilidades fueron separadas

Se separaron tres capas, cada una con una razón de ser distinta:

- **Infraestructura** (`file_manager.py`, `config.py`): entrada/salida
  y rutas. No representa decisiones de negocio.
- **Presentación** (`interface.py`): qué se imprime y cómo se pide
  información al usuario. No decide nada sobre transacciones.
- **Negocio, encapsulado en Skills** (`skills/`): cada responsabilidad
  de negocio (detectar, normalizar, validar, medir, exportar,
  resumir) vive en su propio archivo `skill.py`, documentado con su
  propio `SKILL.md`, y es reutilizable de forma independiente en
  otro proyecto.
- **Coordinación** (`agent.py`): decide qué Skills ejecutar y en qué
  orden, sin contener ninguna regla de negocio él mismo.

## 3. Cómo mejoró la arquitectura respecto a la versión anterior

- **Antes**, `main.py` conocía la existencia de los 5 módulos de
  negocio y los llamaba directamente; agregar una regla nueva o una
  responsabilidad nueva implicaba tocar `main.py`.
- **Ahora**, `main.py` solo conoce a `TransactionAgent`. Agregar una
  Skill nueva (como se hizo con `summary`, que no existía en el
  proyecto original) no requiere modificar `main.py`, solo `agent.py`.
- **Reutilización**: cada Skill puede copiarse a otro proyecto junto
  con su `SKILL.md`, sin arrastrar el resto del sistema — algo que no
  era posible cuando la lógica estaba dispersa en módulos acoplados
  al flujo del menú.
- **Personalización real**: antes no existía manera de "apagar" una
  parte del sistema sin comentar código. Ahora, `enable_metrics=False`
  (por ejemplo) desactiva esa Skill de forma controlada, con un
  mensaje explícito (`SkillDisabledError`) en vez de un fallo
  silencioso o un `if` disperso por el código.
- **Sin duplicación de modelo**: el modelo normalizado y sus valores
  válidos (`VALID_STATUSES`, `VALID_CURRENCIES`) vivían repetidos en
  `normalizer.py` y `validator.py`; ahora viven una sola vez en
  `models/transaction.py`.

## 4. Qué decisiones fueron tomadas por el desarrollador

- El modelo de datos normalizado (sección "Modelo normalizado" del
  README) — sin cambios respecto al proyecto original.
- Los estados y monedas válidos, y sus equivalencias de mapeo — sin
  cambios respecto al proyecto original.
- Los 7 criterios de invalidez de una transacción, y su orden de
  verificación — sin cambios respecto al proyecto original.
- **Decisión pendiente de confirmar**, heredada del proyecto original:
  los montos negativos se siguen aceptando como válidos, ya que no
  están en la lista de criterios de invalidez definida por el
  desarrollador.
- **Decisión nueva de esta refactorización**: qué significa
  "deshabilitar" cada Skill (ver `agent.py`, sección de docstring del
  módulo). En particular, que deshabilitar la validación implica que
  todas las transacciones mapeadas se acepten sin convertir sus
  valores, en vez de simplemente no ejecutar nada.
- **Decisión nueva de esta refactorización**: agregar la Skill
  `summary`, que no existía en el proyecto original, porque el
  enunciado de la refactorización la exige explícitamente para poder
  demostrar `enable_summary`.
- La numeración del menú (agregar la opción "9. Mostrar resumen" y
  mover "Salir" al 10) fue necesaria para poder exponer la Skill
  `summary` al usuario; es una decisión de interfaz, no de negocio.

## 5. Cómo fue utilizada la IA como herramienta de apoyo

La IA se usó como asistente técnico durante toda la refactorización,
iteración por iteración:

- Propuso la estructura de `agent.py` y el patrón de `AgentContext` /
  estado en el Agente.
- Ayudó a mover cada módulo a su carpeta de Skill correspondiente,
  ajustando únicamente los imports necesarios (sin tocar la lógica).
- Propuso el mecanismo de `SkillDisabledError` para que deshabilitar
  una Skill fuera explícito y manejable, en vez de devolver `None` en
  silencio.
- Redactó los 6 archivos `SKILL.md`, siguiendo el formato pedido
  (objetivo, responsabilidades, entrada, salida, restricciones,
  ejemplo, relación con otras Skills), a partir de leer el código real
  de cada Skill.
- Ayudó a diagnosticar y corregir errores de terminal (PowerShell vs.
  CMD) durante la creación de la estructura de carpetas.

En ningún momento la IA decidió el modelo de datos, las reglas de
normalización, las reglas de validación, ni qué Skills debía tener el
proyecto (la lista de Skills obligatorias venía dada por el
desarrollador desde el enunciado inicial).

## 6. Ejemplo concreto de una sugerencia de la IA que fue modificada por el desarrollador

Durante la Iteración 1 de esta refactorización, la IA propuso crear el
sistema agéntico como un **proyecto completamente nuevo y separado**
(`transaction-agent/`, en una carpeta distinta a `transaction-normalizer/`),
interpretando un enunciado anterior que hablaba de "crear" una nueva
arquitectura. Se llegó a generar la estructura completa de ese
proyecto separado (`agent.py`, `skills/`, `models/`, etc.) y el
desarrollador incluso llegó a crearla en su máquina.

El desarrollador corrigió esta interpretación: el objetivo real era
**refactorizar el proyecto `transaction-normalizer` existente desde
adentro**, agregando `agent.py` y `skills/` junto a los archivos ya
existentes, para poder comparar directamente el "antes" y el
"después" dentro del mismo repositorio, sin duplicar la lógica de
negocio en dos proyectos independientes.

Tras la corrección, la IA:
- Descartó