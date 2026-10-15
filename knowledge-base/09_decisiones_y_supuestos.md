# Decisiones y Supuestos

## Decisiones documentadas

| ID | Decisión | Alternativas | Motivo | Consecuencias |
|---|---|---|---|---|
| DD-01 | **API/backend puro** (sin UI obligatoria) | (a) Fullstack web; (b) API pura; (c) Desktop | La consigna de cátedra define la implementación a nivel de **lógica de dominio + API, con tests automatizados** (P0-sys = b) | No se entrega interfaz; se asume un cliente externo consumidor de la API |
| DD-02 | **Mono-tenant** (un consultorio, <50 personas) | (a) Mono-tenant; (b) Multi-tenant multi-clínica | Decisión explícita para enfocar el esfuerzo en la prevención de solapamientos (P0-scale = a) | Sin aislamiento por organización ni multi-sucursal en la v1; migrar a multi-tenant luego implica trabajo de modelo y auth |
| DD-03 | **Python 3.12+ + FastAPI/Pydantic** | Selección anterior Java/Spring, sustituida; Node/TS quedó descartado en la fundación | Indicación docente del 2026-10-01 confirmada por Juan el 2026-10-15 | SQLAlchemy, Alembic y pytest; historia preservada en el registro de ajuste |
| DD-04 | **PostgreSQL** como base productiva y de integración | Motores sin constraint de exclusión | Garantía de exclusión sobre ambos recursos | PostgreSQL real necesario para integración y concurrencia |
| DD-05 | **pytest**: unitarios puros con fakes; integración en PostgreSQL real | H2 era parte del stack Java anterior y queda sustituido | Separar pruebas de reglas y pruebas de persistencia | Un fake no demuestra constraints ni concurrencia |
| DD-06 | **Constraint de exclusión** (`EXCLUDE USING gist` sobre `tsrange`) | (a) Sólo validación en aplicación; (b) Sólo constraint DB; (c) ambos | Garantía dura contra el solapamiento concurrente, no dependiente de la aplicación (RN-16) | Acopla la persistencia a PostgreSQL; se documenta y se testea por separado con Testcontainers |
| DD-07 | **Arquitectura hexagonal limpia** | MVC acoplado a framework | Aísla RN-NN de FastAPI/Pydantic/SQLAlchemy | ORM sólo en infraestructura; DTOs Pydantic sólo en frontera |
| DD-08 | **Transacción por caso de uso + locking** (optimista + pesimista) | (a) Sin locking; (b) locking optimista; (c) pesimista; (d) ambos + constraint | El riesgo principal es el agendamiento concurrente entre canales | Complejidad de manejo de errores de concurrencia (traducir `StaleDataError`/`23P01` a `409`) |
| DD-09 | **Recordatorios por scheduler + WhatsApp** en MVP | (a) WhatsApp; (b) email; (c) SMS | El caso de uso pide confirmación por WhatsApp y ataca el ausentismo | Depende de la disponibilidad de WhatsApp Business API (ver pregunta abierta) |
| DD-10 | **JWT stateless con RBAC** | (a) JWT; (b) sesión en servidor | API pura sin UI; sencillo de escalar y testear | Hay que gestionar expiración/refresh y validar firma de webhooks aparte |

### DD-01 — API/backend puro (detalle)
**Decisión:** el sistema se entrega como API REST + dominio y tests; no incluye interfaz gráfica.
**Contexto:** hubo que decidir el tipo de sistema (P0-sys).
**Alternativas consideradas:** fullstack web; desktop.
**Justificación:** la consigna de cátedra fija la implementación en lógica de dominio + API con tests automatizados.
**Trade-offs aceptados:** sin UI propia; cualquier cliente debe construirse aparte.

### DD-02 — Mono-tenant (detalle)
**Decisión:** un solo consultorio, sin multi-tenancy.
**Contexto:** P0-scale = (a). Evita dispersar el foco del TP.
**Alternativas consideradas:** multi-tenant multi-clínica.
**Justificación:** mantener la concentración en la prevención de solapamientos.
**Trade-offs aceptados:** no sirve tal cual para varias clínicas; requeriría cambios de modelo/auth para escalar.

### DD-03 — Stack corregido por consigna docente
**Decisión vigente:** Python 3.12+, FastAPI/Pydantic, SQLAlchemy, Alembic y pytest.
**Origen:** indicación docente del 2026-10-01 en el chat de metodología, confirmada por Juan el 2026-10-15.
**Historia:** la fundación había elegido Java 21/Spring Boot 3 y afirmado que JUnit/AssertJ eran obligatorios. Esa interpretación quedó sustituida; no representa la consigna vigente. No se modifica el Discovery ni se recrea evidencia pasada.
**Trazabilidad:** [ajuste-stack-python.md](../docs/decisiones/ajuste-stack-python.md).

### DD-04 — PostgreSQL
**Decisión:** PostgreSQL en producción e integración. El constraint de exclusión y `btree_gist` siguen siendo la defensa de persistencia planificada.

### DD-05 — Pruebas separadas por capa
**Decisión:** pytest para unitarios de dominio y aplicación con fakes. pytest sobre PostgreSQL real para repositorios, transacciones, constraint y concurrencia. Pasar los unitarios no demuestra la garantía concurrente.

### DD-06 — Constraint de exclusión
**Decisión:** reforzar RN-01/RN-03/RN-16 con `EXCLUDE USING gist`.
**Alternativas consideradas:** sólo validación de aplicación.
**Justificación:** el riesgo de doble reserva concurrente exige garantía a nivel DB.
**Trade-offs aceptados:** dependencia de PostgreSQL en infraestructura; se prueba con PostgreSQL real (Docker Compose o Testcontainers para Python).

## Supuestos inferidos

Todos los supuestos se marcan con **Suposición:** en la KB. Resumen:

### SU-01 — Rol Administrador del consultorio
**Suposición:** existe un rol *Administrador del consultorio* que configura prestaciones, sillones y profesionales.
**Origen:** inferido; no aparece explícito en los 11 puntos del Discovery.
**Riesgo si es falso:** el catálogo no tendría quién lo administre (o lo haría la recepcionista).
**Cómo validar:** preguntar si la recepcionista concentra administración (ver [`10`](10_preguntas_abiertas.md)).

### SU-02 — Reserva de invitado (paciente sin cuenta)
**Suposición:** la reserva online 24/7 admite pacientes no registrados (invitado), sin login previo.
**Origen:** inferido del caso de uso "reservar online 24/7 sin llamar".
**Riesgo si es falso:** habría que exigir registro y el flujo de reserva cambia.
**Cómo validar:** decidir política de identidad del paciente en el flujo público.

### SU-03 — Recurso sillón obligatorio
**Suposición:** todo turno ocupa **obligatoriamente** un sillón; no hay turnos sin sillón (p. ej. teleconsulta) en la v1.
**Origen:** RN-01 define el recurso doble como invariante. El Discovery deja abierto si puede haber turnos sin sillón.
**Riesgo si es falso:** habría que permitir `sillonId` nulo y relajar RN-01.
**Cómo validar:** confirmar con el dominio si existen atenciones sin box (telemedicina).

### SU-04 — Estados y transiciones del turno
**Suposición:** los estados `PENDIENTE | CONFIRMADO | CANCELADO | REALIZADO | AUSENTE` y las transiciones de RN-08 modelan el ciclo de vida mínimo.
**Origen:** inferido del caso de uso de confirmación por WhatsApp y de la necesidad de distinguir realizados/cancelados.
**Riesgo si es falso:** el modelo de estados podría necesitar más granularidad (p. ej. `REPROGRAMADO`, `EN_SALA`).
**Cómo validar:** revisar con la cátedra/consultorio el ciclo de vida esperado.

### SU-05 — Franja horaria y tolerancia configurables
**Suposición:** la franja de atención y la tolerancia de agendamiento (RN-14) son configurables y sus valores concretos no los fija la KB.
**Origen:** el Discovery no especifica horarios ni tolerancias.
**Riesgo si es falso:** reglas de agendamiento incorrectas.
**Cómo validar:** definir defaults con el consultorio (ver [`10`](10_preguntas_abiertas.md)).

### SU-06 — Cliente externo de la API
**Suposición:** al ser backend puro, la interfaz la provee un cliente externo que consume la API.
**Origen:** DD-01 (API pura).
**Riesgo si es falso:** haría falta construir una UI dentro del alcance.
**Cómo validar:** confirmar con la cátedra si se espera algún cliente de referencia.

### SU-07 — Recordatorio por WhatsApp con anticipación configurable
**Suposición:** la anticipación del recordatorio es un parámetro configurable (valor por defecto no fijado en la KB).
**Origen:** RN-05 exige recordatorio "según anticipación configurada".
**Riesgo si es falso:** no hay valor operativo acordado.
**Cómo validar:** definir la anticipación con el consultorio.

### SU-08 — Seña con Mercado Pago fuera del camino crítico del MVP
**Suposición:** el cobro de seña vía Mercado Pago es un extra planificado, no un requisito bloqueante para confirmar el turno en la v1.
**Origen:** el Discovery lista Mercado Pago como integración pero deja abierto si la seña es obligatoria.
**Riesgo si es falso:** el flujo de confirmación tendría que incorporar el pago.
**Cómo validar:** decidir la política de seña (ver [`10`](10_preguntas_abiertas.md)).

### SU-09 — Datos de seed ficticios
**Suposición:** los seeds y fixtures son sintéticos y cumplen RN-LG/Ley 25.326.
**Origen:** restricción legal del Discovery (punto 9).
**Riesgo si es falso:** incumplimiento legal.
**Cómo validar:** chequeo automatizado de convenciones de datos ficticios (dominio `.test`, documentos `0000000X`).

## Referencias

- Preguntas abiertas: [`10_preguntas_abiertas.md`](10_preguntas_abiertas.md)
- Arquitectura: [`08_arquitectura_propuesta.md`](08_arquitectura_propuesta.md)
