# Prompt 3 — Refactorizacion correcta: dentro de transaction-normalizer

El desarrollador aclaro que el objetivo era refactorizar el proyecto
existente `transaction-normalizer` desde adentro, no crear uno nuevo.
Se recibio el enunciado definitivo, con la arquitectura de Skills como
carpetas (`skill.py` + `SKILL.md`), el diseno del Agente
(`TransactionAgent`), y el plan de 6 iteraciones:

1. Analisis del proyecto actual.
2. Crear agent.py y reorganizar el flujo.
3. Convertir cada modulo en una Skill independiente.
4. Personalizacion real del agente.
5. Documentar cada Skill con su SKILL.md.
6. Actualizar README y nota tecnica.

Cada iteracion se desarrollo por separado, probando el codigo antes
de entregarlo, verificando en cada paso que el comportamiento fuera
identico al del proyecto original (salvo la personalizacion,
agregada intencionalmente en la Iteracion 4).