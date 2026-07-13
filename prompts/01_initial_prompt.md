# Prompt 1 — Especificacion inicial de Transaction Normalizer

Se entrego a la IA la especificacion completa del proyecto original:
leer transacciones desde JSON de 3 sistemas distintos, detectar el
origen, normalizar al modelo comun, validar, generar metricas, y
exponer todo mediante un menu CLI interactivo de 9 opciones.

Se dejo explicito que la IA podia proponer estructura de codigo y
funciones, pero no podia decidir el modelo de datos, las reglas de
normalizacion, ni los criterios de invalidez de una transaccion.

Resultado: proyecto `transaction-normalizer` desarrollado en 5
iteraciones (estructura y menu, deteccion y modelo, validacion,
filtros y metricas, exportacion y documentacion).