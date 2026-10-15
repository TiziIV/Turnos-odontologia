# Visión y Objetivos

## Propósito del sistema

Gestionar de forma confiable la agenda de un consultorio odontológico garantizando que cada turno ocupe **simultáneamente un profesional y un sillón/box libres**, con duración derivada del tipo de prestación, prevención estricta de solapamientos y recordatorios automáticos que reduzcan el ausentismo.

El sistema resuelve el corazón operativo del agendamiento dental: en lugar de tratar el turno como una simple cita de un profesional, lo modela como la intersección de dos recursos físicos (profesional + sillón). Ese modelo es lo que impide el doble agendamiento y, junto con la duración por prestación y los recordatorios, ataca las tres causas raíz de pérdida de ingresos detectadas en el Discovery.

## Problema raíz

En los consultorios odontológicos de Argentina se pierden ingresos por tres motivos concretos:

1. **Ausentismo** — pacientes que no asisten y liberan tarde (o nunca) el cupo, con sillones ociosos.
2. **Solapamiento de turnos** — dos turnos que comparten profesional o sillón en la misma franja, producto de agendar en canales distintos (online vs. mostrador) sin una fuente única de disponibilidad.
3. **Falta de automatización de recordatorios** — la confirmación depende de llamados manuales que no escalan y no cubren 24/7.

## Objetivos por actor

| Actor | Objetivo principal | Objetivos secundarios |
|---|---|---|
| Paciente | Reservar, cancelar y confirmar turnos sin llamar al consultorio, 24/7 | Ver disponibilidad real, recibir recordatorio por WhatsApp, liberar el cupo al cancelar sin fricción |
| Odontólogo (general o especialista) | Consultar su agenda y atender con turnos que nunca se pisen entre sí | Conocer la duración asignada por prestación, evitar dobles reservas sobre su tiempo |
| Recepcionista / Secretaria | Agendar y reprogramar desde el mostrador evitando solapamientos por profesional y por sillón | Gestionar cupos, reprogramar con liberación inmediata, operar sobre la misma fuente de disponibilidad que el canal online |
| Administrador del consultorio | Configurar prestaciones (con duración), sillones/boxes y profesionales | Mantener el catálogo del dominio consistente y auditable |

> **Suposición:** el actor **Administrador del consultorio** no surgió de los 11 puntos del Discovery. Se incorpora porque la configuración de prestaciones, sillones y profesionales requiere un rol con permisos de escritura sobre el catálogo, distinto del rol operativo de la recepcionista.

## Alcance MVP (v1.0)

**IN — dentro del MVP:**

- Gestión de agenda con **duración por prestación** (la duración del turno se deriva del tipo de prestación, no de un valor fijo global).
- Asignación **simultánea de profesional + sillón/box** por turno (recurso doble obligatorio).
- **Prevención de solapamientos** estricta: el intervalo `[inicio, fin)` de un recurso no puede intersectarse con otro turno del mismo recurso.
- **Cancelación / reprogramación** con **liberación inmediata de cupo** (ambos recursos vuelven a estar disponibles).
- **Recordatorio automático** antes del turno (WhatsApp).
- Reserva online 24/7 por parte del paciente.

**OUT — fuera del MVP (backlog post-MVP):**

- Odontograma interactivo 3D.
- Periodontograma avanzado.
- Integración de radiología digital.
- IA de diagnóstico.

## Métricas de éxito

- **Cupos liberados correctamente**: 100% de las cancelaciones deja ambos recursos disponibles para una nueva reserva (verificable por test).
- **Cero solapamientos**: ningún turno confirmado comparte franja con otro sobre el mismo profesional o el mismo sillón (invariante de dominio + constraint de base de datos).
- **Reserva concurrente resuelta**: ante dos intentos simultáneos sobre el mismo recurso, uno gana y el otro recibe un rechazo controlado.
- **Recordatorios programados**: todo turno creado dispara exactamente un recordatorio según la anticipación configurada.
- **Trazabilidad de reglas**: cada regla de negocio `RN-XX` tiene al menos un test automatizado que la respalda.

## Referencias

- Modelo de datos: [`04_modelo_de_datos.md`](04_modelo_de_datos.md)
- Reglas de negocio: [`05_reglas_de_negocio.md`](05_reglas_de_negocio.md)
- Alcance detallado y decisiones: [`09_decisiones_y_supuestos.md`](09_decisiones_y_supuestos.md)
