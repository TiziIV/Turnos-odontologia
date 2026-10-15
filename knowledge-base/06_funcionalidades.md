# Funcionalidades

Historias de usuario organizadas por **épica**. Formato: `US-NNN`. Cada historia cita las reglas `RN-NN` que la respaldan.

---

## Épica 1: Acceso y seguridad

### US-001 — Login de usuario del consultorio
**Como** integrante del consultorio (odontólogo/recepcionista/administrador)
**Quiero** autenticarme con email y contraseña
**Para** acceder a las funciones habilitadas para mi rol.

**Criterios de aceptación**:
- [ ] Con credenciales válidas devuelve un token (JWT) con el rol embebido.
- [ ] Con credenciales inválidas devuelve `401` sin filtrar cuál campo falló.
- [ ] La contraseña se almacena hasheada, nunca en texto plano.

**Reglas relacionadas**: RN-LG

### US-002 — Autorización por rol
**Como** administrador
**Quiero** que cada endpoint exija el rol adecuado
**Para** que un paciente no pueda operar sobre datos de otros ni administrar el catálogo.

**Criterios de aceptación**:
- [ ] Un paciente recibe `403` al intentar modificar el catálogo o turnos ajenos.
- [ ] La matriz RBAC de [`03`](03_actores_y_roles.md) se respeta en todos los endpoints.

**Reglas relacionadas**: —

---

## Épica 2: Catálogo del consultorio

### US-003 — Configurar prestaciones con duración
**Como** administrador del consultorio
**Quiero** crear y editar prestaciones con su duración en minutos
**Para** que la agenda calcule automáticamente la duración de cada turno.

**Criterios de aceptación**:
- [ ] Toda prestación tiene `duracionMinutos > 0`.
- [ ] El código de prestación es único.
- [ ] Se puede desactivar una prestación sin borrar turnos históricos.

**Reglas relacionadas**: RN-02, RN-10

### US-004 — Configurar sillones/boxes
**Como** administrador del consultorio
**Quiero** gestionar los sillones/boxes del consultorio
**Para** poder asignarlos como segundo recurso de cada turno.

**Criterios de aceptación**:
- [ ] El código de sillón es único.
- [ ] Un sillón inactivo no puede recibir turnos nuevos.

**Reglas relacionadas**: RN-01, RN-11

### US-005 — Configurar profesionales
**Como** administrador del consultorio
**Quiero** gestionar los odontólogos y su especialidad
**Para** asignarlos como primer recurso de cada turno.

**Criterios de aceptación**:
- [ ] La matrícula es única.
- [ ] Un profesional inactivo no puede recibir turnos nuevos.

**Reglas relacionadas**: RN-01, RN-11

---

## Épica 3: Reserva de turnos

### US-006 — Reserva online 24/7 del paciente
**Como** paciente
**Quiero** reservar un turno online en cualquier momento
**Para** no tener que llamar al consultorio en horario de atención.

**Criterios de aceptación**:
- [ ] La disponibilidad consultada refleja profesional **y** sillón libres en la franja (recurso doble).
- [ ] La duración del turno se deriva de la prestación elegida.
- [ ] El turno creado queda en estado `PENDIENTE` o `CONFIRMADO` y ocupa ambos recursos.
- [ ] No se permite encadenar un turno que se pise con otro del mismo recurso.

**Reglas relacionadas**: RN-01, RN-02, RN-03, RN-13, RN-14

### US-007 — Agendamiento en mostrador
**Como** recepcionista
**Quiero** agendar turnos desde el mostrador
**Para** atender pacientes presenciales sobre la misma agenda que el canal online.

**Criterios de aceptación**:
- [ ] El mostrador y el canal online comparten la misma fuente de disponibilidad.
- [ ] Un intento de agendar una franja ya ocupada se rechaza con error controlado.
- [ ] El canal del turno queda registrado (`MOSTRADOR`) para trazabilidad.

**Reglas relacionadas**: RN-01, RN-03, RN-09, RN-16

### US-008 — Consulta de agenda por profesional
**Como** odontólogo
**Quiero** ver mi agenda de turnos
**Para** saber qué pacientes atiendo y en qué box.

**Criterios de aceptación**:
- [ ] La agenda lista los turnos activos del profesional ordenados por inicio.
- [ ] Cada turno muestra paciente, prestación, sillón y franja.

**Reglas relacionadas**: RN-09

---

## Épica 4: Cancelación y reprogramación

### US-009 — Cancelación con liberación inmediata
**Como** paciente (o recepcionista)
**Quiero** cancelar un turno
**Para** que el cupo de profesional y sillón se libere al instante.

**Criterios de aceptación**:
- [ ] Tras cancelar, ambos recursos vuelven a ofrecerse como disponibles.
- [ ] Se puede crear un turno nuevo en la misma franja y recurso de inmediato.
- [ ] El recordatorio asociado queda cancelado.

**Reglas relacionadas**: RN-04, RN-08, RN-09, RN-05

### US-010 — Reprogramación atómica
**Como** recepcionista
**Quiero** reprogramar un turno a otra franja
**Para** reubicar al paciente sin perder el turno original si la nueva franja está ocupada.

**Criterios de aceptación**:
- [ ] Si la nueva franja no tiene ambos recursos libres, la operación falla y el turno original queda intacto.
- [ ] Si tiene éxito, la franja vieja se libera y el recordatorio se reprograma.
- [ ] Nunca quedan dos recordatorios vigentes para el mismo turno.

**Reglas relacionadas**: RN-15, RN-04, RN-12

---

## Épica 5: Recordatorios y reducción del ausentismo

### US-011 — Recordatorio automático por WhatsApp
**Como** paciente
**Quiero** recibir un recordatorio antes de mi turno
**Para** no olvidarme y asistir.

**Criterios de aceptación**:
- [ ] Al crear un turno activo se programa exactamente un recordatorio.
- [ ] El envío ocurre según la anticipación configurada.
- [ ] Si el turno se cancela, el recordatorio se cancela.

**Reglas relacionadas**: RN-05, RN-12

### US-012 — Confirmación por WhatsApp
**Como** paciente
**Quiero** confirmar mi turno respondiendo el mensaje
**Para** avisar que voy a asistir.

**Criterios de aceptación**:
- [ ] El webhook de WhatsApp actualiza el estado del turno a `CONFIRMADO` cuando el paciente confirma.
- [ ] Una confirmación sobre un turno cancelado no lo reactiva (estado final).

**Reglas relacionadas**: RN-08, RN-05

---

## Épica 6: Concurrencia y consistencia (transversal)

### US-013 — Doble reserva concurrente resuelta
**Como** responsable del consultorio
**Quiero** que dos intentos simultáneos sobre el mismo recurso no generen doble reserva
**Para** garantizar que nunca haya solapamiento aunque online y mostrador coincidan.

**Criterios de aceptación**:
- [ ] Ante dos reservas concurrentes sobre `(profesional, franja)` o `(sillon, franja)`, una gana y otra recibe rechazo controlado.
- [ ] No se produce corrupción ni excepción cruda de base de datos hacia el cliente.

**Reglas relacionadas**: RN-16, RN-01, RN-03

---

## Referencias

- Reglas: [`05_reglas_de_negocio.md`](05_reglas_de_negocio.md)
- Flujos: [`07_flujos_principales.md`](07_flujos_principales.md)
