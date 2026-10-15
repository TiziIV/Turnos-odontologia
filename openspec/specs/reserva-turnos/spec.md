# reserva-turnos Specification

## Purpose

Permitir crear reservas de invitado que ocupen simultáneamente un profesional y un sillón, respetando la duración de la prestación y evitando solapamientos en la demostración local secuencial.

Ajustar 2026-10-15 (Juan Martín García): escenarios de demostración obligatorios — reserva válida (`Camino feliz`), rechazo por solapamiento de profesional o sillón (`Error por solapamiento de profesional o sillón`), y borde inicio igual al fin anterior (`Borde inicio igual al fin anterior`). Política temporal confirmada: ISO 8601 con zona y comparación en UTC. Apply MUST NOT agregar login, PostgreSQL ni cancelación; los estados finales en fixtures no implican un endpoint de cancelar.

## Requirements

### Requirement: Crear una reserva válida

El sistema SHALL aceptar `POST /api/public/turnos` con `pacienteId`, `profesionalId`, `sillonId`, `prestacionId` e `inicio`, crear un turno PENDIENTE de canal ONLINE y devolver HTTP 201 con identificador, referencias, inicio, fin, estado y canal (RN-01, RN-07 parcial). Todas las referencias MUST existir; profesional, sillón y prestación MUST estar activos (RN-10/11).

#### Scenario: Camino feliz
- **GIVEN** (DADO) paciente 1 existente, profesional 1 y sillón 1 activos y libres, y LIMPIEZA activa de 30 minutos
- **WHEN** (CUANDO) se solicita la reserva para `2026-11-02T09:00:00-03:00`
- **THEN** (ENTONCES) se devuelve 201 con un turno PENDIENTE, ONLINE, inicio `2026-11-02T12:00:00Z` y fin `2026-11-02T12:30:00Z`, guardado una sola vez

#### Scenario: Referencias o recursos no habilitados
- **GIVEN** (DADO) una referencia inexistente de paciente/profesional/sillón/prestación, o un profesional/sillón/prestación inactivo (casos parametrizados)
- **WHEN** (CUANDO) se solicita crear el turno
- **THEN** (ENTONCES) se devuelve 422 sin agregar ni modificar turnos

### Requirement: Evitar solapamiento por cualquiera de los recursos

El sistema SHALL rechazar con HTTP 409 y código `TURNO_SOLAPADO` toda reserva cuyo intervalo intersecte estrictamente un turno activo del mismo profesional O del mismo sillón (RN-01/03). Sólo PENDIENTE y CONFIRMADO ocupan recursos (RN-09). Si A termina exactamente cuando B inicia, ambos intervalos MUST admitirse. Un rechazo MUST conservar todos los turnos existentes.

#### Scenario: Error por solapamiento de profesional o sillón
- **GIVEN** (DADO) A activo de 09:00 a 09:30 del 2 de noviembre de 2026, con offset -03:00, profesional 1 y sillón 1
- **WHEN** (CUANDO) B comienza 09:15 y dura 30 minutos usando (profesional 1, sillón 2) o (profesional 2, sillón 1), con los demás recursos libres
- **THEN** (ENTONCES) cada caso parametrizado devuelve 409 `TURNO_SOLAPADO`, A permanece idéntico y B no se guarda

#### Scenario: Borde inicio igual al fin anterior
- **GIVEN** (DADO) A activo de 09:00 a 09:30 con profesional 1 y sillón 1, el 2 de noviembre de 2026 con offset -03:00
- **WHEN** (CUANDO) B comienza exactamente 09:30 por 30 minutos, compartiendo sólo profesional, sólo sillón o ambos recursos (casos parametrizados)
- **THEN** (ENTONCES) B se crea con 201 y A permanece idéntico

#### Scenario: Un minuto de intersección y contención total
- **GIVEN** (DADO) A activo de 09:00 a 09:30 y recursos alternativos libres
- **WHEN** (CUANDO) B comparte profesional o sillón y ocupa 09:29–09:59, 08:50–09:50 o 09:00–09:20 del mismo día y offset (casos parametrizados)
- **THEN** (ENTONCES) cada caso devuelve 409 sin modificar la agenda

#### Scenario: Recursos diferentes y estados finales
- **GIVEN** (DADO) A de 09:00 a 09:30 y una solicitud B en la misma franja
- **WHEN** (CUANDO) B tiene ambos recursos distintos, o A está CANCELADO, REALIZADO o AUSENTE compartiendo recursos (casos parametrizados)
- **THEN** (ENTONCES) B se crea con 201; los estados finales provienen de fixtures, sin implicar endpoints de transición

### Requirement: Derivar duración y preservar intervalo válido

El sistema SHALL calcular `fin = inicio + duracionMinutos` según la prestación; la duración MUST ser un entero positivo y `inicio < fin` (RN-02/13). El cliente MUST NOT definir fin, duración, estado ni canal; las entradas adicionales SHALL rechazarse con 422.

#### Scenario: Duración de catálogo
- **GIVEN** (DADO) CONSULTA 20, LIMPIEZA 30, EXTRACCION 40 y ENDO 60 minutos
- **WHEN** (CUANDO) se reserva cada prestación con ambos recursos libres
- **THEN** (ENTONCES) fin menos inicio equivale a su duración respectiva

#### Scenario: Duración inválida o modificación manual
- **GIVEN** (DADO) una prestación de duración cero o negativa, o una solicitud que incluye fin/duración/estado/canal manuales
- **WHEN** (CUANDO) se intenta crear el turno
- **THEN** (ENTONCES) se rechaza sin guardar; en la frontera HTTP se devuelve 422

### Requirement: Comparar instantes con zona horaria

El sistema SHALL exigir `inicio` ISO 8601 con offset explícito o Z y normalizarlo a UTC para salida y comparación (confirmado en Ajustar 2026-10-15). Una fecha sin zona o mal formada, IDs no enteros positivos o campos obligatorios ausentes MUST devolver 422 sin modificar la agenda. Esta política temporal corresponde a la demo en memoria; no decide tipos SQL futuros ni autoriza PostgreSQL en este change.

#### Scenario: Offsets equivalentes
- **GIVEN** (DADO) A activo con inicio `2026-11-02T09:00:00-03:00` por 30 minutos
- **WHEN** (CUANDO) B usa el mismo recurso e inicio `2026-11-02T12:00:00Z`
- **THEN** (ENTONCES) B es rechazado con 409 por representar el mismo instante

#### Scenario: Entrada inválida
- **GIVEN** (DADO) inicio sin zona, fecha inválida, ID inválido o campo requerido ausente (casos parametrizados)
- **WHEN** (CUANDO) se envía la solicitud
- **THEN** (ENTONCES) se devuelve 422 sin crear turnos

### Requirement: Demostración exclusivamente sintética y local

La demo SHALL usar únicamente catálogos y pacientes ficticios (RN-06), iniciar sin reservas y documentar sus identificadores, ejecución en loopback con un proceso y pérdida de turnos al reiniciar. La documentación MUST delimitar la garantía secuencial y declarar RN-16, persistencia durable, auth y flujos restantes como pendientes.

#### Scenario: Reinicio de la demo
- **GIVEN** (DADO) una instancia de demo con una reserva creada
- **WHEN** (CUANDO) se reinicia el proceso
- **THEN** (ENTONCES) se restauran los catálogos ficticios iniciales sin reservas, según lo explicado en README

#### Scenario: Datos de demostración
- **GIVEN** (DADO) el catálogo de pacientes de ejemplo
- **WHEN** (CUANDO) se inspeccionan fixtures y ejemplos publicados
- **THEN** (ENTONCES) contienen datos sintéticos, emails `@example.test` y documentos `0000000X`, sin datos clínicos reales
