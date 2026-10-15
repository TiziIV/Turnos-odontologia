# Control de entrega — TPI Metodología I

Revisión: 2026-10-15. Este documento distingue requisitos de resultados comprobados; una casilla pendiente no equivale a una etapa ejecutada.

## Fuentes y aclaraciones

- Consigna completa: `desarrollo-active-stack (3).pdf`, facilitada por Juan Martín (10 páginas).
- Presentaciones de SDD y Active Stack, partes 1–3, facilitadas por Juan Martín.
- Aclaraciones del profesor en el chat de C3/C4: stack del 01/10; un solo change y video centrado en metodología del 12/10; entrega del 16/10 confirmada el 15/10.
- El chat privado, sus accesos a grabaciones y archivos personales no se incorporan al repositorio.
- El trabajo de skills/MCP adjunto al chat es una actividad posterior, fuera del alcance de esta entrega.

## Fundación y ajuste del stack

- [x] Repositorio clonado y fundación documental existente identificada.
- [x] Diez documentos canónicos de KB, roadmap, reglas y registro de skills presentes.
- [x] Capturas originales de etapas 0–5 y Ajustar de la matriz presentes en `docs/evidencias/`.
- [x] Revisar ajuste autorizado a Python/FastAPI/SQLAlchemy/PostgreSQL y pytest; AGENTS.md y CLAUDE.md idénticos, JSON válido e historia Discovery conservada. Ver `decisiones/ajuste-stack-python.md`.
- [x] Resolver alcance mínimo del primer change frente a dependencias pendientes del roadmap: excepción académica aprobada, C-06 será el primer change entregado; capacidades completas anteriores siguen pendientes.
- [x] Comprobar entorno ejecutable y acceso al flujo de orquestación y a Engram. Pytest 74 passed el 2026-10-15. Engram recuperó el recuerdo #3 y el intervalo semiabierto.

## Change crear-turno-anti-solapamiento

- [x] Explore: registrar estado real, reglas, dependencias y resumen del relevamiento.
- [x] Propose: crear proposal.md, design.md, specs/ y tasks.md mediante OpenSpec.
- [x] Justificar en proposal.md la elección del change en 2–3 líneas.
- [x] Revisar Propose con Juan Martín y registrar Ajustar real con pedido, respuesta y cambios (2026-10-15: tres escenarios, ISO 8601/UTC, sin login/PostgreSQL/cancelación).
- [x] Especificar DADO/CUANDO/ENTONCES: éxito, rechazo por solapamiento y borde inicio == fin anterior.
- [x] Cubrir conflictos tanto de profesional como de sillón; duración derivada de prestación.
- [x] Guardar captura real del Ajustar en `docs/evidencias/` (`etapa-6-propose-ajustar.png`).
- [x] Apply: implementar únicamente el alcance revisado, con tests trazables a reglas y escenarios.
- [x] Verify: ejecutar pytest y comprobaciones pertinentes; guardar salida y captura real del resultado satisfactorio.
- [x] README: instalación y ejecución reproducibles desde un clon nuevo.
- [x] Archive: sincronizar specs, archivar con OpenSpec y actualizar roadmap; captura en `docs/evidencias/etapa-6-archive.png`.
- [x] Engram: guardar decisiones reales y recuperar contexto en una sesión posterior; registrar consulta, respuesta y captura (`docs/evidencias/etapa-7-engram-consulta.png`).

Los registros de terminal complementan las capturas; no las reemplazan. No generar imágenes que aparenten ejecuciones ni marcar evidencia pendiente como existente.

## Discovery y PDF

- [x] Informe Markdown con secciones A–D y matriz de siete dimensiones existente.
- [x] Revisar la tabla de al menos 15 sistemas: proveedor, país, URL y fecha; distinguir afirmaciones comerciales de funcionalidades demostradas.
- [x] Comprobar cálculos de matriz (pesos 25/20/15/15/10/10/5) y presencia de nota metodológica para datos no evidenciados: 15 totales y 15 scores correctos. Esto no acredita la veracidad de las fuentes ni valida el criterio de asignación de cada nota.
- [x] Incorporar sección explícita de verificación de al menos cinco fuentes, con afirmación, hallazgo y corrección.
- [x] Preparar resumen ejecutivo de hasta una página y referencias completas.
- [x] Exportar PDF con portada: título, materia, nombres completos de integrantes y fecha.
- [ ] Revisar visualmente todas las páginas del PDF antes de entregar.

## Reflexión, video y participación

Integrantes: García Juan Martín y Tiziano Valentini. La verificación de cinco fuentes está en el informe. La reflexión escrita la redactan los integrantes.

- [ ] Reflexión de 1–2 páginas escrita por los integrantes, revisada con asistencia si lo desean.
- [ ] Responder: información incorrecta/no verificable del Discovery y cómo se detectó; Ajustar y consecuencia de continuar; spec aprobada frente a prompt suelto; mayor/menor aporte de la fundación; participación de cada integrante.
- [ ] Distinguir el Ajustar de Tiziano en Discovery del Ajustar de Juan Martín en Propose, sin describir como hecho lo que todavía no ocurrió.
- [ ] Declarar y explicar el uso de IA.
- [ ] Guion de video de 8–12 minutos: Discovery y fundación, change y Ajustar, tests, Archive, Engram y conclusiones.
- [ ] Todos los integrantes hablan con su voz real; cámara al menos en la presentación, según consigna escrita.
- [ ] Mostrar pantalla y proceso real; priorizar metodología y función de los artefactos sobre detalle del código.
- [ ] Historial con commits propios de cada integrante y avances reales; conservar autoría original.
- [ ] Revisión final de datos ficticios, ausencia de secretos y accesibilidad del repositorio/video.
- [ ] Entregar repositorio y enlace de YouTube en el campus el viernes 16/10/2026, según anuncio del profesor para C3/C4.

## Estado al cerrar el ciclo

La fundación sigue en el commit de TiziIV. El change está archivado, la spec vigente es `openspec/specs/reserva-turnos/spec.md` y la suite local terminó en 74 passed. Falta la reflexión escrita por los integrantes, el video en YouTube y publicar esta rama: `origin/main` todavía apunta solo a la fundación.
