# Reglas de Negocio

Cada regla tiene un código único y estable `RN-NN` para trazabilidad. Toda regla `RN-NN` debe tener, como mínimo, un test automatizado (JUnit 5 + AssertJ) que la respalde. Las reglas confirmadas en el Discovery son RN-01 a RN-06; RN-07 a RN-15 completan el dominio (estados, transiciones, reprogramación, tolerancia y errores) y se marcan como derivadas.

Formato de cada regla: **enunciado**, **justificación**, **invariante verificable**, **cómo se testea**.

---

## Dominio: Agenda y recursos

### RN-01 — Recurso doble obligatorio
**Enunciado:** un turno sólo puede confirmarse si en su franja horaria existe **a la vez** un `Profesional` disponible **y** un `Sillon/box` libre. Si falta cualquiera de los dos, el turno no se crea.
**Justificación:** es el invariante central del proyecto y el hueco competitivo detectado; sin ambos recursos el turno es físicamente irrealizable.
**Invariante verificable:** todo `Turno` persistido en estado activo tiene `profesionalId` y `sillonId` no nulos, y ambos recursos están libres en `[inicio, fin)` al momento de confirmar.
**Cómo se testea:** test que intenta crear un turno con profesional ocupado y sillón libre (espera rechazo), con profesional libre y sillón ocupado (espera rechazo) y con ambos libres (espera éxito).

### RN-02 — Duración derivada de la prestación
**Enunciado:** la duración del turno se **deriva del tipo de prestación** (p. ej. limpieza 30 min, endodoncia 60 min); no es un valor fijo global ni editable por turno.
**Justificación:** el catálogo de prestaciones define cuánto ocupa cada tipo de atención; de ahí sale `fin`.
**Invariante verificable:** `Turno.fin = Turno.inicio + Prestacion.duracionMinutos`, y `Prestacion.duracionMinutos > 0`.
**Cómo se testea:** test parametrizado que, para cada prestación del seed, verifica que `fin − inicio == duracionMinutos`; test que intenta fijar una duración manual distinta (espera que el valor derivado prevalezca / error de validación).

### RN-03 — Anti-solapamiento estricto (fin == inicio permitido)
**Enunciado:** prohibido el solapamiento **estricto**; un turno puede iniciar en el **minuto exacto** en que finaliza el anterior (fin == inicio es válido). Para un mismo profesional o un mismo sillón, el intervalo `[inicio, fin)` no puede intersectarse con el de otro turno activo.
**Justificación:** evita dobles reservas sin impedir el encadenado eficiente de la agenda.
**Invariante verificable:** para todo par de turnos activos del mismo recurso, `fin(A) <= inicio(B)` **o** `fin(B) <= inicio(A)`.
**Cómo se testea:** test de caso límite donde `fin(A) == inicio(B)` (espera **éxito**, encadenado) y test donde `inicio(B) = fin(A) − 1 min` (espera **rechazo**, solapamiento). Se testea sobre profesional por separado de sillón.

### RN-04 — Cancelación libera el cupo de inmediato
**Enunciado:** al cancelar un turno, **ambos recursos** (profesional y sillón) vuelven a estar disponibles de inmediato para nuevas reservas.
**Justificación:** es la resolución del caso de uso "cancelar y que el cupo se libere inmediatamente"; recupera valor de cupos vacíos.
**Invariante verificable:** un turno en estado `CANCELADO` no participa en la verificación de solapamiento ni bloquea la creación de otro turno en la misma franja del mismo recurso.
**Cómo se testea:** crear turno → cancelarlo → crear otro turno en la misma franja con el mismo profesional y mismo sillón (espera éxito). Además, verificar que la consulta de disponibilidad vuelve a ofrecer el cupo.

### RN-15 — Reprogramación atómica
**Enunciado:** reprogramar un turno equivale a liberar la franja vieja y reservar la nueva de forma **atómica**: si la nueva franja no tiene ambos recursos libres, la reprogramación falla y el turno original queda intacto.
**Justificación:** evita perder el turno original ante un error a mitad de la operación.
**Invariante verificable:** tras una reprogramación fallida, el turno conserva `inicio`, `fin`, `profesionalId` y `sillonId` originales (o bien la operación revierte por completo).
**Cómo se testea:** test que intenta reprogramar a una franja ocupada (espera rechazo y turno original sin cambios) y a una franja libre (espera éxito y liberación de la franja vieja).

---

## Dominio: Estados y transiciones

### RN-07 — Estados válidos del turno
**Enunciado:** un turno sólo puede estar en uno de estos estados: `PENDIENTE`, `CONFIRMADO`, `CANCELADO`, `REALIZADO`, `AUSENTE`.
**Justificación:** define el ciclo de vida mínimo y evita estados libres.
**Invariante verificable:** `Turno.estado ∈ {PENDIENTE, CONFIRMADO, CANCELADO, REALIZADO, AUSENTE}`.
**Cómo se testea:** test que intenta asignar un estado inválido (espera error) y test parametrizado sobre el conjunto permitido.

### RN-08 — Transiciones permitidas
**Enunciado:** transiciones válidas: `PENDIENTE → CONFIRMADO`, `PENDIENTE → CANCELADO`, `CONFIRMADO → CANCELADO`, `CONFIRMADO → REALIZADO`, `CONFIRMADO → AUSENTE`. Cualquier otra transición es inválida (en particular `CANCELADO` y `REALIZADO`/`AUSENTE` son **estados finales**).
**Justificación:** un turno cancelado no puede "resucitar"; un turno realizado no vuelve a pendiente.
**Invariante verificable:** el estado final de una transición pertenece al conjunto de destinos permitidos desde el estado origen.
**Cómo se testea:** test de tabla (origen × destino) que verifica aceptación/rechazo; test explícito de que `CANCELADO → CONFIRMADO` falla.

### RN-09 — Turnos activos vs. finales (ocupación de recursos)
**Enunciado:** sólo los turnos en estado `PENDIENTE` o `CONFIRMADO` **ocupan** recursos y participan de las reglas de solapamiento. Los estados `CANCELADO`, `REALIZADO` y `AUSENTE` no ocupan recursos.
**Justificación:** unifica RN-03 y RN-04 bajo un mismo criterio de "turno activo".
**Invariante verificable:** en la verificación de disponibilidad y solapamiento sólo se consideran turnos con `estado IN (PENDIENTE, CONFIRMADO)`.
**Cómo se testea:** test que crea un turno `REALIZADO` en una franja y luego un turno `CONFIRMADO` solapado (espera éxito, porque el finalizado no ocupa).

---

## Dominio: Prestaciones y catálogo

### RN-10 — Prestación activa requerida
**Enunciado:** sólo pueden agendarse turnos sobre prestaciones en estado `activa`; una prestación inactiva no admite turnos nuevos.
**Justificación:** permite retirar prestaciones del catálogo sin romper turnos históricos.
**Invariante verificable:** el `Prestacion` referenciado por un turno nuevo tiene `activa == true`.
**Cómo se testea:** test que intenta agendar con prestación inactiva (espera rechazo) y con activa (espera éxito).

### RN-11 — Recurso activo requerido
**Enunciado:** sólo pueden asignarse turnos a `Profesional` y `Sillon` en estado `activo`.
**Justificación:** un profesional o box dado de baja no puede recibir turnos nuevos; los históricos se conservan.
**Invariante verificable:** al crear/reprogramar, `Profesional.activo == true` y `Sillon.activo == true`.
**Cómo se testea:** test que intenta crear turno con profesional inactivo (rechazo) y con sillón inactivo (rechazo).

---

## Dominio: Recordatorios y notificaciones

### RN-05 — Recordatorio automático
**Enunciado:** al crearse (o reprogramarse) un turno activo se programa automáticamente **un** recordatorio por WhatsApp, con anticipación configurable, para reducir el ausentismo. El recordatorio se cancela si el turno se cancela.
**Justificación:** ataca la principal causa de pérdida de ingresos (ausentismo).
**Invariante verificable:** todo turno activo tiene a lo sumo un `Recordatorio` vigente con `programadoPara = inicio − anticipacion` y `programadoPara < inicio`; al cancelar el turno, el recordatorio pasa a `CANCELADO`.
**Cómo se testea:** test que crea un turno y verifica que existe un recordatorio programado en la fecha esperada; test que cancela el turno y verifica que el recordatorio quedó `CANCELADO`.

### RN-12 — Recordatorio ligado a la reprogramación
**Enunciado:** al reprogramar un turno, el recordatorio existente se reprograma a la nueva franja (o se genera uno nuevo y se cancela el anterior); nunca quedan dos recordatorios vigentes para el mismo turno.
**Justificación:** evitar recordatorios duplicados u obsoletos que confunden al paciente.
**Invariante verificable:** para cada turno activo existe exactamente un recordatorio en estado `PROGRAMADO`.
**Cómo se testea:** test que reprograma un turno y cuenta recordatorios vigentes (espera exactamente 1, apuntando a la nueva fecha).

---

## Dominio: Legal y datos

### RN-06 / RN-LG — Protección de datos (Ley 25.326) y datos sintéticos
**Enunciado:** el tratamiento de datos personales de pacientes se rige por la **Ley 25.326** de Protección de Datos Personales (Argentina). Está **prohibido almacenar datos sensibles reales** en repositorios, seeds, fixtures o entornos de pruebas: sólo se admiten **datos sintéticos/ficticios**.
**Justificación:** es una restricción legal y ética desde el día 1 (Discovery, punto 9).
**Invariante verificable:** los seeds y fixtures usan nombres, teléfonos y documentos ficticios (dominio `@example.test`, documentos `0000000X`); el modelo no almacena datos clínicos sensibles (diagnósticos, imágenes, historia clínica) en el MVP.
**Cómo se testea:** test/chequeo que valida que los fixtures del seed no provienen de datos reales (convención de dominio de email `.test` y patrones documentales) y que no hay columnas de datos clínicos en el esquema; revisión en CI del contenido del repositorio.

> **Nota:** RN-06 (legal) cruza todos los dominios: cualquier entidad que almacene datos personales queda alcanzada por esta regla.

---

## Dominio: Errores y validaciones globales

### RN-13 — Intervalo bien formado
**Enunciado:** todo turno debe tener `inicio < fin`, con intervalo semiabierto `[inicio, fin)`.
**Justificación:** un intervalo inválido rompe la lógica de solapamiento.
**Invariante verificable:** `inicio < fin` para todo turno persistido.
**Cómo se testea:** test que intenta crear un turno con inicio igual o posterior al fin (espera rechazo por validación).

### RN-14 — Franja dentro de la agenda configurable (tolerancia horaria)
**Enunciado:** los turnos deben caer dentro de la franja horaria de atención configurada; se admite una **tolerancia** de agendamiento de ±X minutos para ajustes de mostrador. (El valor de la franja de atención y de la tolerancia es **configurable**.)
**Justificación:** evita agendar fuera de horario de atención y da flexibilidad operativa al mostrador.
**Invariante verificable:** `franjaApertura <= Turno.inicio` y `Turno.fin <= franjaCierre`, con la tolerancia configurada aplicada a los bordes.
**Cómo se testea:** test que agenda dentro de la franja (éxito) y fuera de la franja más allá de la tolerancia (rechazo).

> **Suposición:** el valor concreto de la franja de atención y de la tolerancia no fue especificado en el Discovery. Se modela como configuración; el valor por defecto se registra como pregunta abierta en [`10_preguntas_abiertas.md`](10_preguntas_abiertas.md).

### RN-16 — Concurrencia: una sola reserva gana
**Enunciado:** ante dos intentos simultáneos de reservar el mismo recurso en la misma franja (p. ej. canal online vs. mostrador), exactamente **uno** debe tener éxito y el otro recibir un rechazo controlado; nunca ambos ni ninguno por corrupción.
**Justificación:** el riesgo principal identificado en el Discovery es el agendamiento concurrente entre canales.
**Invariante verificable:** bajo cualquier intercalación de dos transacciones sobre el mismo `(profesionalId, franja)` o `(sillonId, franja)`, el resultado final contiene a lo sumo un turno activo en esa franja.
**Cómo se testea:** test de concurrencia con dos hilos/transacciones simultáneas sobre el mismo recurso; se verifica que una commitea y la otra falla con error de dominio controlado (no con excepción de base cruda). En PostgreSQL se respalda con el **constraint de exclusión** (`EXCLUDE USING gist`); en H2 se respalda con el locking de la aplicación.

---

## Excepciones globales

- Las reglas RN-01, RN-03, RN-04, RN-09 y RN-16 se refuerzan **en la base de datos** mediante el constraint de exclusión de PostgreSQL (garantía a nivel DB, no sólo aplicación). Ver [`08_arquitectura_propuesta.md`](08_arquitectura_propuesta.md).
- Toda regla `RN-NN` debe citarse en los criterios de aceptación de las historias correspondientes en [`06_funcionalidades.md`](06_funcionalidades.md).

## Referencias

- Modelo de datos e invariantes: [`04_modelo_de_datos.md`](04_modelo_de_datos.md)
- Concurrencia: [`08_arquitectura_propuesta.md`](08_arquitectura_propuesta.md)
- Decisiones: [`09_decisiones_y_supuestos.md`](09_decisiones_y_supuestos.md)
