# Prompt 4 — Personalizacion del Agente

Se pidio que la configuracion del Agente (`enable_validation`,
`enable_metrics`, `enable_export`, `enable_summary`) modificara
realmente el comportamiento del sistema, no fuera un parametro
decorativo.

Decisiones tomadas para esta iteracion:

- Detectar y normalizar estructuralmente no tienen flag (son
  obligatorios: sin ellos no hay transaccion normalizada sobre la
  cual aplicar ninguna otra Skill).
- Deshabilitar la validacion hace que todas las transacciones
  mapeadas se acepten sin convertir sus valores, en vez de clasificar
  validas/invalidas.
- Deshabilitar metricas, exportacion o resumen bloquea la opcion de
  menu correspondiente con un mensaje explicito
  (`SkillDisabledError`), en vez de fallar en silencio.
- Se agrego la Skill `summary` (nueva, no existia en el proyecto
  original) y una opcion de menu para exponerla, ya que no habia
  forma de demostrar `enable_summary` sin ella.
- Al iniciar el programa, se pregunta la configuracion deseada para
  esa ejecucion, para que la personalizacion sea una decision real de
  cada corrida y no un valor fijo en el codigo.