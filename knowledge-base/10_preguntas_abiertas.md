# Preguntas Abiertas

## Inconsistencias detectadas

### IN-01 — Alcance mono-tenant vs. multi-sucursal del mercado
**Fuente A (Discovery, Sección A/C) dice:** casi todos los competidores ofrecen multi-sucursal/multiprofesional como feature estándar.
**Fuente B (decisión P0-scale locked) dice:** el sistema es **mono-tenant**, un solo consultorio, sin multi-sucursal.
**Impacto:** la KB y el modelo asumen un único consultorio; si la cátedra pidiera multi-sucursal, el modelo de datos y el auth habría que rehacerlos.
**Resolución propuesta:** mantener mono-tenant (decisión explícita para enfocar el anti-solapamiento); registrar multi-sucursal como backlog post-MVP.

### IN-02 — Matriz B del informe de Discovery no aplica a la KB
**Fuente A (`docs/discovery/informe-discovery.md`, Sección B) dice:** una matriz de decisión ponderada (7 dimensiones) que rankeó a 15 competidores.
**Fuente B (alcance de esta KB) dice:** la matriz B era un **ejercicio comparativo de competidores** de la cátedra, no un requisito del sistema.
**Impacto:** incluirla en la KB confundiría el alcance del producto con el análisis de mercado.
**Resolución propuesta:** excluida deliberadamente de la KB. El análisis competitivo se resume sólo como contexto en [`01`](01_vision_y_objetivos.md) y [`09`](09_decisiones_y_supuestos.md).

### IN-03 — Duración por prestación: catálogo fijo vs. configurable por odontólogo
**Fuente A (Discovery) dice:** la duración depende del tipo de prestación.
**Fuente B (Discovery, preguntas abiertas) dice:** no se aclara si es configurable por el consultorio/odontólogo o un catálogo fijo del sistema.
**Impacto:** si debe ser configurable por odontólogo, el modelo necesita una tabla de duración por (profesional, prestación).
**Resolución propuesta:** modelar la duración a nivel de `Prestacion` (catálogo del consultorio) y dejar la variante por profesional como evolución (ver P-03).

### IN-04 — ¿El sillón es entidad de primera clase o atributo opcional?
**Fuente A (Discovery, preguntas abiertas) dice:** abierto: ¿sillón con agenda propia o atributo opcional? ¿Puede haber turnos sin sillón?
**Fuente B (RN-01 locked) dice:** el turno exige **simultáneamente** profesional Y sillón.
**Impacto:** si existieran turnos sin sillón (teleconsulta), RN-01 y el modelo (FK obligatoria) se relajan.
**Resolución propuesta:** sillón como entidad de primera clase con FK obligatoria en la v1 (ver P-04).

### IN-05 — Sobreturnos y urgencias vs. anti-solapamiento estricto
**Fuente A (Discovery) dice:** DentalSoft contempla sobreturnos; el Discovery pregunta cómo se comporta la anti-solapamiento ante urgencias.
**Fuente B (RN-03 locked) dice:** solapamiento estricto prohibido, sin excepciones.
**Impacto:** si se requieren sobreturnos/urgencias, hace falta una vía controlada que relaje RN-03.
**Resolución propuesta:** v1 sin sobreturnos (RN-03 estricto); registrar como evolución (ver P-05).

---

## Preguntas abiertas (priorizadas)

| Prioridad | Pregunta | Bloquea | Decisor |
|---|---|---|---|
| Alta | **¿Existe API oficial de WhatsApp Business para consultorios pequeños o se depende de soluciones no oficiales** (riesgo de bloqueo y cumplimiento)? | Épica 5 (Recordatorios) — diseño del adaptador | Equipo técnico + cátedra |
| Alta | **¿El MVP incluye el cobro de la seña vía Mercado Pago**, o queda como integración post-MVP? ¿La seña es obligatoria para confirmar el turno? | Épica 3/5 — flujo de confirmación y modelo | Product Owner / cátedra |
| Media | ¿El rol **Administrador del consultorio** existe como rol propio, o la recepcionista concentra la administración del catálogo? | Épica 2 — RBAC y seguridad | Product Owner |
| Media | ¿La **duración por prestación** es un catálogo fijo del consultorio o configurable **por odontólogo**? | Modelo de datos (§Prestacion) | Cátedra / dominio |
| Media | ¿Se admiten **turnos sin sillón** (p. ej. teleconsulta) en la v1, o el sillón es obligatorio? | Modelo y RN-01 | Cátedra / dominio |
| Media | ¿Cuál es la **franja horaria de atención** y la **tolerancia** de agendamiento por defecto (RN-14)? | Validaciones de agenda | Consultorio / cátedra |
| Baja | ¿Cuál es la **anticipación por defecto** del recordatorio (RN-05)? | Configuración y tests | Consultorio |
| Baja | ¿Se requieren **sobreturnos/urgencias** que relajen RN-03, o el anti-solapamiento es absoluto? | RN-03, modelo de estados | Cátedra / dominio |

### P-01 — WhatsApp: API oficial vs. no oficial
**Pregunta:** ¿el proyecto puede usar la WhatsApp Business API oficial (requiere cuenta de negocio aprobada) o se acepta una biblioteca no oficial (con riesgo de bloqueo y de cumplimiento)?
**Por qué importa:** define el adaptador de infraestructura, los requisitos de aprobación y la viabilidad del flujo de recordatorios/confirmación.

### P-02 — Seña con Mercado Pago
**Pregunta:** ¿la seña por Mercado Pago entra en el MVP y es obligatoria para confirmar, o es un extra opcional post-MVP?
**Por qué importa:** si es obligatoria, el flujo de reserva depende de un webhook de pago y cambia el estado de confirmación y el modelo (transacción de pago).

### P-03 — Configurabilidad de la duración
**Pregunta:** ¿la duración por prestación se fija por consultorio o varía por odontólogo?
**Por qué importa:** determina si `duracionMinutos` vive en `Prestacion` o en una tabla `(profesional, prestacion) → duración`.

### P-04 — Sillón obligatorio
**Pregunta:** ¿todo turno requiere sillón, o hay atenciones sin box?
**Por qué importa:** decide si `Turno.sillonId` es obligatorio (RN-01) o nullable.

### P-05 — Sobreturnos/urgencias
**Pregunta:** ¿se necesita un mecanismo de sobreturno o urgencia que rompa el anti-solapamiento estricto?
**Por qué importa:** afecta RN-03 y el modelo de estados.

> **Nota metodológica:** por regla dura, nada de esto se inventa; los valores no confirmados se modelan como **configurables** o quedan pendientes acá.

## Referencias

- Decisiones y supuestos: [`09_decisiones_y_supuestos.md`](09_decisiones_y_supuestos.md)
- Reglas: [`05_reglas_de_negocio.md`](05_reglas_de_negocio.md)
