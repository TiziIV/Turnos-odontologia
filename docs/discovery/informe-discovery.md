# Discovery — turnos-odontologia

**Fecha**: 2026-10-15
**Fuentes investigadas**: 15 proveedores (ver `discovery/sources/`)
**Artefacto canónico**: `discovery/discovery.md`

> **Regla de evidencia**: este informe no agrega datos que no estén respaldados por las
> 15 notas de `discovery/sources/`. Donde una nota no respalda una celda, en la Sección A se
> escribe literalmente **No evidenciado** y en la Sección B se puntúa `0<sup>NE</sup>` (misma
> convención: vacío de evidencia, no ausencia probada). Las limitaciones de evidencia de la
> fase de scraping están documentadas en la Sección 0 (nota de evidencia) y en la Sección A.

---

## Sección 0 — Consolidación de los 11 puntos de Discovery

**1. Problema**
Pérdida de ingresos por ausentismo, solapamiento de turnos entre profesionales y sillones
odontológicos, y falta de automatización de recordatorios en consultorios de Argentina.

**2. Usuarios**
Pacientes, odontólogos generales y especialistas, y recepcionistas/secretarias del consultorio.

**3. Casos de uso**
Reserva online 24/7; agendamiento de turno por secretaria evitando solapamiento (por
profesional y por sillón/box); cancelación con liberación inmediata de cupo; confirmación
vía WhatsApp.

**4. Competidores**
Los 15 proveedores listados (Dentalink, DentalSoft, Doctocliq, DentiDesk, OdontoSaaS,
Reservo, Clinic Cloud, XDental, DentalData, Medilink, AgendaPro, Nubimed, Dentap,
OdontoCloud, Nimbo Clinic).

**5. Funcionalidades necesarias (MVP)**
Gestión de agenda con duración por prestación; asignación simultánea de profesional y
sillón; prevención de solapamientos; cancelación/reprogramación; recordatorio automático.

**6. Funcionalidades opcionales**
Odontograma interactivo 3D; periodontograma avanzado; integración de radiología digital;
IA de diagnóstico.

**7. Reglas de negocio**
(a) un turno requiere simultáneamente profesional disponible Y sillón/box libre en esa
franja; (b) la duración depende del tipo de prestación (limpieza 30m, endodoncia 60m);
(c) prohibido el solapamiento estricto — un turno puede iniciar en el minuto exacto en que
finaliza el anterior.

**8. Integraciones**
WhatsApp Business API, Mercado Pago (señas), Google Calendar.

**9. Restricciones**
Ley 25.326 de Protección de Datos Personales (Argentina); no almacenar datos sensibles
reales en repositorios o pruebas.

**10. Riesgos**
Agendamiento simultáneo concurrente de turnos online y recepción presencial.

**11. Preguntas abiertas**
Disponibilidad de API oficial de WhatsApp para consultorios pequeños vs. soluciones no
oficiales.

### Nota de evidencia (fase de scraping)

Durante la fase de investigación se registraron las siguientes limitaciones, que condicionan
la lectura de la Sección A:

- `https://dentaldata.com.ar/` → el dominio **no resuelve** (`Transport error`). Nota sin datos.
- `https://dentap.co/` → el dominio **no resuelve** (NXDOMAIN). Nota sin datos.
- `https://odontosaas.com/` → devolvió sólo el *shell* de una SPA React (sin features ni
  pricing reales); sólo se recuperaron meta tags. Sin pricing.
- `https://xdental.com.br/` → dominio **estacionado/reutilizado** (redirige a un sitio
  ajeno); el producto real está en `xdentalcontrole.com.br` (fue la URL usada).
- `https://odontocloud.com.ar/` → **no existe** (NXDOMAIN); el OdontoCloud real está en
  `odontocloud.com.br` (fue la URL usada).
- **Sin pricing público**: Dentalink, OdontoSaaS, DentiDesk, Nimbo Clinic, Medilink,
  XDental, OdontoCloud (y los 2 sin datos: DentalData, Dentap).
- **Con pricing público**: DentalSoft (ARS 30.000/60.000), Doctocliq (USD 19/29/49),
  Reservo (Bs 99/149/229), Clinic Cloud (29€/49€/79€), Nubimed (27,40€/50,10€),
  AgendaPro (ARS, en `/ar/planes`).

---

## Sección A — Tabla comparativa de los 15 sistemas

Notas al pie:
- † OdontoSaaS: SPA React; sólo se recuperó el shell HTML + meta tags (features/pricing reales no accesibles).
- ‡ DentalData: dominio no resuelve (`Transport error`); sin datos.
- § Dentap: dominio no resuelve (NXDOMAIN); sin datos.
- ¶ XDental: `xdental.com.br` es dominio estacionado/reutilizado; se investigó `xdentalcontrole.com.br`.
- ‖ OdontoCloud: `odontocloud.com.ar` no existe (NXDOMAIN); se investigó `odontocloud.com.br`.

| Sistema | URL investigada | Origen/País | Problema que resuelve | Usuarios objetivo | Pricing público | Reserva online 24/7 | Duración por prestación | Profesional + sillón simultáneo | Prevención de solapamiento | Cancelación/reprogramación | Recordatorios automáticos | Multi-sucursal/multiprofesional | Integraciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dentalink | https://www.softwaredentalink.com/ | LATAM (Chile, Colombia, México, España) | Gestión integral de clínica dental: agenda, fichas clínicas, cobros y seguros en un solo lugar | Consultorios dentales de todos los tamaños (independientes a clínicas con varios profesionales y sucursales) | No evidenciado (sólo "solicita tu cotización") | Sí (link público de reserva) | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí (confirmación correo/WhatsApp/llamada; recordatorios email) | Sí (multicentro, multi-sucursal, comisiones por odontólogo) | No evidenciado |
| DentalSoft | https://dentalsoft.com.ar/ | Argentina (La Plata / Rosario) | Reducir ausencias, ordenar historias clínicas, automatizar turnos y dar presencia web profesional | Clínicas y profesionales odontológicos de Argentina (1 a 10+ profesionales; incluye secretarias) | Sí — ARS 30.000/mes (Gestión) y ARS 60.000/mes (Pro), + plan Gratis | Sí (turnos online 24/7) | No evidenciado | No evidenciado | Sí (detección automática de solapamiento) | Sí (si el paciente confirma/cancela, la agenda se actualiza sola) | Sí (WhatsApp y email automáticos) | Sí (multi-sucursal y multiprofesional) | Sí (Google Calendar; MercadoPago; WhatsApp) |
| Doctocliq | https://doctocliq.com/ | LATAM (+20 países; adaptaciones fiscales Perú, México, Ecuador, Colombia) | Suite todo-en-uno que centraliza pacientes, agenda, finanzas y marketing para recuperar y fidelizar pacientes | Doctores, odontólogos y clínicas multi-especialidad; propietarios, doctores, asistentes y recepcionistas | Sí — USD 19/29/49/mes (Individual/Básico/Avanzado), + plan Gratis | Sí (link de agendamiento + Soyla IA 24/7) | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí (WhatsApp, email y SMS) | Sí (sedes adicionales + usuarios doctor) | Sí (Google Calendar; WhatsApp; pago por link en Perú) |
| DentiDesk | https://dentidesk.com/ | Chile (Santiago); opera LatAm | Simplificar y optimizar la gestión clínica dental, reduciendo tiempos de espera | Clínicas dentales y odontólogos (equipo clínico y administrativo); también universidades y sindicatos | No evidenciado (sólo prueba 15 días y demo) | Parcial (botón/link de agendamiento online; 24/7 no explicitado) | No evidenciado (publica intervalo de agendamiento 15/30/40 min, no duración por prestación) | No evidenciado | No evidenciado | Sí a nivel manual (modifica y reprograma; confirmar/anular desde correo; sin liberación automática de cupo) | Sí por email (WhatsApp automático "próximamente") | Sí (multi-sucursal destacada) | Sí (SII de Chile; Alegra para República Dominicana) |
| OdontoSaaS † | https://odontosaas.com/ | Brasil (pt-BR, BRL) | Sistema odontológico completo para gestión de clínicas (agenda inteligente, prontuario, financiero, marketing, IA) | No evidenciado | No evidenciado (sólo "teste grátis 7 días") | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| Reservo | https://reservo.lat/ | Bolivia (Bs; LatAm) | Reservas online 24h sin llamadas ni cruces de horarios, para ahorrar trabajo administrativo | Profesionales y negocios multi-rubro (barbería, salud, gimnasio, consultoría; clínicas) — no exclusivo odontología | Sí — Bs 99/149/229/mes (Emprendedor/Negocio/Equipo) | Sí (agenda online 24 h) | Sí ("establece la duración de cada cita") | No evidenciado | Sí (bloqueo automático contra dobles reservas) | No evidenciado | Sí (email o WhatsApp) | Multiprofesional sí (agenda independiente por miembro); multi-sucursal no evidenciado | No evidenciado |
| Clinic Cloud | https://clinic-cloud.com/ | España (ecosistema Doctoralia) | Gestión integral de la clínica de principio a fin desde un solo lugar | Clínicas y consultas médicas de España (segmenta por momento del negocio; franquicias en Enterprise) | Sí — 29€/49€/79€/mes (Mini/Pro/Max), + Enterprise a convenir | Sí (reserva online 24/7 + Doctoralia) | No evidenciado | No evidenciado | No evidenciado (sí "optimiza huecos") | No evidenciado | Sí (WhatsApp, SMS y email con recordatorios y confirmaciones) | Sí (multi-profesional y multi-sede) | Sí (Doctoralia) |
| XDental ¶ | https://www.xdentalcontrole.com.br/ | Brasil (Brasilia) | Gestión completa de consultorios y clínicas odontológicas sin controles en papel/Excel/PDF | Dentistas y clínicas odontológicas de Brasil (profesionales individuales, consultorios, clínicas y hospitales) | No evidenciado (sólo "solicitar orçamento" y demo gratis) | No evidenciado | Sí (duración de tiempo configurable por atendimiento) | No evidenciado | No evidenciado | No evidenciado | Sí (SMS desde la agenda con actualización automática de estado; email marketing) | Multiprofesional sí (múltiples agendas por especialista/especialidad); multi-sucursal no evidenciado | Sí (NFS-e/NF-e; integración contable; certificado digital) |
| DentalData ‡ | https://dentaldata.com.ar/ | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| Medilink | https://www.softwaremedilink.com/ | LATAM (Chile, Colombia, México); grupo Healthatom | Optimizar la operación del centro de salud unificando procesos (agenda, inasistencia, tareas manuales) | Centros de salud y consultas de LatAm, por tamaño (Esencial/Pro/Titanium) y por especialidad | No evidenciado (planes sin importes; precio según cantidad de médicos) | Sí (agendamiento online) | Parcial (gestiona las horas del día por profesional y por paciente) | No evidenciado ("gestión de recursos" como pista, sin detalle) | No evidenciado | No evidenciado | Sí (email ilimitado + WhatsApp; confirmaciones como add-on) | Sí (gestión de sucursales / multisucursal) | Sí (Google Calendar; Google Analytics 4; Bsale; Meta) |
| AgendaPro | https://agendapro.com/ (AR: /ar/planes) | LatAm / Argentina (n°1 AR) | Organizar citas, cobrar sin fricción y hacer crecer el negocio (multi-vertical) | Negocios de belleza/bienestar y salud (salones, spa, clínicas, kinesiología, psicología, etc.); 1 a 20+ profesionales | Sí — ARS 13.900/33.900/44.900/314.900/mes (Individual/Básico/Premium/Pro) | Sí (reservas 24/7) | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí (WhatsApp y email) | Sí (multi-sucursal y multiprofesional) | Sí (Google Reserve/GMB; Google Analytics; Meta Pixel) |
| Nubimed | https://nubimed.com/ | España | Gestión integral de la clínica en la nube (agenda, citas online, recordatorios, historia clínica, facturación) | Clínicas y profesionales médicos de España, con vertical dental | Sí — 27,40€/mes (LITE) y 50,10€/mes (PREMIUM); MULTICENTRO a consultar | Sí (cita online 24h) | No evidenciado | No evidenciado (sí sala de espera y lista de espera) | No evidenciado | Parcial (confirmar/cancelar desde el recordatorio; cobertura de huecos vía lista de espera) | Sí (email/SMS/WhatsApp) | Sí (multicentro, multi-profesional) | Sí (WhatsApp; IA en la comunicación) |
| Dentap § | https://dentap.co/ | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| OdontoCloud ‖ | http://www.odontocloud.com.br/ | Brasil (São Paulo; Score Web) | Gestión odontológica gerencial y operacional unificada, sin otros controles en papel/Excel/PDF | Clínicas y consultorios odontológicos de Brasil, del recién graduado a grandes redes; incluye laboratorios de prótesis | No evidenciado (precio único; sólo cotización) | No evidenciado | No evidenciado | No evidenciado | Sí (alertas automáticas de conflictos de agendamiento) | Sí (cancelar y reagendar desde telemarketing) | Sí (SMS, WhatsApp y email automáticos con confirmación del paciente) | Sí (multi-unidad; agendas por profesional) | No evidenciado |
| Nimbo Clinic | https://www.nimbo-x.com/ | LatAm (México, Argentina, Ecuador, Perú); Ecaresoft Inc. | Solución todo-en-uno para administrar clínicas (expedientes, agenda, facturación, reputación) | Clínicas y centros médicos de LatAm (incluye dentistas); organización de más de 10 médicos | No evidenciado (modelo modular, "solicita los precios") | Sí (agendamiento online vía portal web) | Parcial ("configura los tiempos de tu equipo médico") | Sí (en vertical de infusión: agenda considerando "un médico o de un cuarto o sillón") | No evidenciado | No evidenciado | Sí (WhatsApp y email) | Sí (agenda multi-médico; productos/servicios por sucursal) | Sí (Stripe para cobro de citas; Google Calendar) |

**Lectura de la tabla**: la reserva online y los recordatorios automáticos son las features
más extendidas entre los proveedores. Las celdas en **No evidenciado** se concentran justamente
en los criterios diferenciales del proyecto: duración por prestación configurable y asignación
simultánea de profesional + sillón/box.

---

## Sección B — Matriz de decisión ponderada

> Esta sección se recalculó por completo con un esquema de **7 dimensiones y pesos fijados por la
> cátedra**. Los puntajes **no son comparables** con la versión anterior (eran otros criterios) y
> el ranking se reordenó de punta a punta. Cada celda se puntuó exclusivamente con lo respaldado
> por las notas de `discovery/sources/`.

### B.1 Dimensiones y pesos (esquema obligatorio)

| # | Dimensión | Peso | Por qué (1 línea) |
|---|---|---|---|
| 1 | Gestión de turnos y automatización | 25% | Corazón operativo del proyecto: agenda digital, reserva online, duración, solapamiento, recordatorios y multi-agenda |
| 2 | Funcionalidad odontológica clínica | 20% | Separa a los sistemas dentales nativos de las suites de clínica general |
| 3 | Integraciones locales y WhatsApp | 15% | Conectividad real con el ecosistema local (WhatsApp, pagos, fiscal, obras sociales) |
| 4 | Administración, cobros y facturación | 15% | Sostiene la operación económica del consultorio (caja, presupuestos, comisiones) |
| 5 | Experiencia del paciente | 10% | Portal, autogestión y telemedicina reducen carga administrativa y ausentismo |
| 6 | Seguridad, exportación y trazabilidad | 10% | Requisito para datos clínicos sensibles y para la confianza del consultorio |
| 7 | Precio y facilidad de adopción | 5% | Importa para la PyME argentina, pero no es el eje del dominio |

### B.2 Definiciones operativas (para que el puntaje sea reproducible)

1. **Gestión de turnos y automatización (25%)**: agenda digital, reserva/agendamiento online, duración por prestación, prevención de solapamiento, asignación de recursos simultáneos (profesional + sillón), reprogramación/cancelación, recordatorios automáticos y multi-agenda/multiprofesional.
2. **Funcionalidad odontológica clínica (20%)**: odontograma, periodontograma, historia clínica dental, módulo de ortodoncia, imágenes/radiología, estética facial, plantillas y presupuestos de tratamiento y firma electrónica dental.
3. **Integraciones locales y WhatsApp (15%)**: WhatsApp (Business/API), Mercado Pago y pagos locales, Google Calendar, Google Reserve/GMB, facturación fiscal local (SII Chile, NFS-e Brasil, AFIP/ARCA Argentina), obras sociales/prepagas/convenios y conexión con Doctoralia u otros marketplaces.
4. **Administración, cobros y facturación (15%)**: facturación, cobros y cajas, presupuestos, financiamiento/cuotas, seguros/convenios, inventario, comisiones y liquidaciones a profesionales, reportes de gestión y multicentro.
5. **Experiencia del paciente (10%)**: portal/área del paciente, autogestión de la cita, telemedicina/videoconsulta, encuestas de satisfacción/NPS, fidelización y email marketing y lista de espera.
6. **Seguridad, exportación y trazabilidad (10%)**: certificaciones (ISO 27001, HIPAA, GDPR, OIV), respaldos y cifrado, trazabilidad/auditoría, exportación de datos y reportes y control de acceso por rol.
7. **Precio y facilidad de adopción (5%)**: pricing público y transparente, accesibilidad PyME, prueba gratis/onboarding, migración asistida y modelo de cobro (por profesional/sucursal).

### B.3 Fórmula y convención de evidencia

**Escala**: 0–5 por dimensión. Se puntúa **sólo con lo respaldado por la nota**; nada de conocimiento previo sobre la empresa.

- **Puntaje ponderado** (sin normalizar) = Σ(peso_% × puntaje_0a5); máximo posible = 500.
- **Score normalizado /100** = Σ(peso_% × puntaje_0a5) / 5; con todas las dimensiones en 5 da 100.

**Convención de evidencia faltante (NE)** — nota al pie:

> `NE` = el sitio no publica evidencia; es un **vacío de evidencia, no una ausencia probada**.

Donde la nota no respalda el criterio se puntúa `0<sup>NE</sup>`. Ante duda razonable entre dos
valores se eligió el menor (regla de prudencia) y se anotó la duda en la lectura.

### B.4 Matriz de decisión (15 sistemas, ordenados por ranking)

Las celdas `0<sup>NE</sup>` no están respaldadas por la nota (ver B.3). Los 3 sistemas sin datos
(OdontoSaaS, DentalData, Dentap) quedan con `0<sup>NE</sup>` en las 7 dimensiones.

| Sistema | D1 (25) | D2 (20) | D3 (15) | D4 (15) | D5 (10) | D6 (10) | D7 (5) | Puntaje ponderado | Score /100 | Ranking |
|---|---|---|---|---|---|---|---|---|---|---|
| DentalSoft | 4 | 4 | 4 | 5 | 3 | 1 | 5 | 380 | 76.0 | 1 |
| Doctocliq | 3 | 5 | 3 | 5 | 3 | 1 | 4 | 355 | 71.0 | 2 |
| Dentalink | 3 | 4 | 2 | 5 | 3 | 4 | 1 | 335 | 67.0 | 3 |
| Nubimed | 3 | 3 | 3 | 5 | 4 | 2 | 4 | 335 | 67.0 | 4 |
| Clinic Cloud | 3 | 3 | 3 | 5 | 3 | 1 | 4 | 315 | 63.0 | 5 |
| DentiDesk | 2 | 5 | 2 | 4 | 3 | 1 | 2 | 290 | 58.0 | 6 |
| OdontoCloud | 4 | 2 | 1 | 4 | 2 | 3 | 2 | 275 | 55.0 | 7 |
| Nimbo Clinic | 3 | 2 | 2 | 4 | 4 | 2 | 1 | 270 | 54.0 | 8 |
| XDental | 3 | 2 | 2 | 4 | 2 | 3 | 2 | 265 | 53.0 | 9 |
| Medilink | 3 | 0<sup>NE</sup> | 4 | 5 | 3 | 1 | 2 | 260 | 52.0 | 10 |
| AgendaPro | 3 | 0<sup>NE</sup> | 3 | 5 | 3 | 1 | 4 | 255 | 51.0 | 11 |
| Reservo | 4 | 0<sup>NE</sup> | 1 | 0<sup>NE</sup> | 1 | 0<sup>NE</sup> | 4 | 145 | 29.0 | 12 |
| OdontoSaaS | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0 | 0.0 | 13 |
| DentalData | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0 | 0.0 | 13 |
| Dentap | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0<sup>NE</sup> | 0 | 0.0 | 13 |

### B.5 Lectura de resultados

- **Qué cambió respecto del foco "agendamiento"**: el esquema anterior concentraba ~62% del peso
  en criterios de agenda (solapamiento 20 + recordatorios 15 + reserva online 15 + duración 12).
  El nuevo baja la gestión de turnos a un 25% y traslada masa crítica a los ejes clínico (20%),
  administrativo/facturación (15%) e integraciones locales (15%). Como consecuencia, el ranking
  dejó de premiar casi en exclusiva a las herramientas de reservas y pasó a ordenar suites
  dentales/administrativas.
- **Sistemas que suben por su peso clínico/administrativo**: **Doctocliq** (6 → 2) por
  odontograma/periodontograma/estética facial/firma electrónica + facturación multi-país;
  **Dentalink** (10 → 3) por odontograma + periodontograma + ortodoncia + rayos X, seguridad
  enterprise (ISO 27001/HIPAA/GDPR) y liquidaciones; **DentiDesk** (11 → 6) por sus fichas de
  especialidad (periodoncia, ortodoncia, cirugía) y facturación SII. **Nubimed** se sostiene 4.º
  por su combo dental nativo + facturación/liquidaciones.
- **Sistemas que bajan**: **Reservo** (2 → 12, la mayor caída) y **AgendaPro** (5 → 11) porque son
  herramientas multi-rubro sin funcionalidad dental ni módulos administrativos/seguridad;
  **Nimbo Clinic** (3 → 8) cae porque su señal de sillón sólo aparece en su vertical de infusión y
  no publica odontograma/periodontograma ni precio.
- **Empate técnico**: Dentalink y Nubimed terminan ambos en 335; se desempata por D1 y luego por
  D2 (Dentalink 3/4 vs. Nubimed 3/3), por eso Dentalink queda 3.º.
- **Aclaración obligatoria**: el ranking mide **cuánta evidencia pública** hay en cada sitio,
  **no la calidad real** del producto. Un `0<sup>NE</sup>` indica que el criterio no está
  publicado (los tools B2B suelen reservar esas features para la demo), no que la función no
  exista. Los tres ceros del fondo (OdontoSaaS, DentalData, Dentap) son vacíos de evidencia: dos
  dominios no resuelven y una SPA no sirvió contenido.

---

## Sección C — Análisis competitivo

### Segmentación del mercado

Se distinguen tres capas:

1. **Odontológico puro**: DentalSoft, Dentalink, DentiDesk, XDental, OdontoCloud y Nubimed
   (con vertical dental nativa: odontograma/periodontograma). Son los competidores más
   cercanos al dominio, aunque con distinto foco (DentalSoft hacia el turno/agenda; Dentalink
   y Medilink hacia gestión clínica/financiera enterprise; XDental y OdontoCloud hacia gestión
   integral con suites fiscales/legales).
2. **Clínicas generales**: Doctocliq, Clinic Cloud, Medilink y Nimbo Clinic. Cubren agenda y
   recordatorios para múltiples especialidades; la odontología es una vertical más.
3. **Agenda genérica / multi-rubro**: Reservo y AgendaPro. No son odontológicos; sirven como
   referencia de UX de reservas y de modelo de precios, no como competidores directos.

### Qué hace (casi) todo el mundo

Reserva/agendamiento online, recordatorios automáticos (WhatsApp/SMS/email), agenda digital y
multi-profesional aparecen en la gran mayoría de las notas. Son **features de entrada**, no
diferenciadores: cualquiera que evalúe el mercado las da por sentadas.

### Qué NO evidencia casi nadie (el hueco)

El hueco competitivo está en el **corazón operativo del agendamiento odontológico**:

- **Asignación simultánea de profesional + sillón/box**: no aparece como concepto explícito en
  casi ninguna nota. La única excepción parcial es **Nimbo Clinic**, que en su vertical de
  clínicas de infusión menciona agendar considerando "un médico o de un cuarto o sillón"; no hay
  evidencia de que traslade ese modelo al agendamiento dental de sillón. **Medilink** menciona
  "gestión de recursos" como pista, sin detalle.
- **Duración configurable por prestación como eje del agendamiento**: sólo **XDental**
  (duración por atendimiento) y **Reservo** (duración de cada cita) lo evidencian; **DentiDesk**
  publica un *intervalo* de agendamiento (15/30/40 min), que no es lo mismo que duración por
  tipo de prestación; **Nimbo** ("configura los tiempos") y **Medilink** ("horas por profesional
  y por paciente") lo evidencian de forma parcial.
- **Anti-solapamiento explícito**: sólo **DentalSoft** lo evidencia de forma explícita
  ("detección automática de solapamiento"); **OdontoCloud** lo hace como "alertas automáticas de
  conflictos de agendamiento" y **Reservo** como bloqueo contra dobles reservas (genérico).

En síntesis: nadie comunica públicamente **el recurso doble (profesional + sillón) como
invariante del turno**, combinado con duración por prestación. Ese es el corredor del proyecto.

### Localización

- **Argentina / LatAm reales**: DentalSoft (AR nativo), AgendaPro (AR nativo), Medilink y
  Dentalink (LatAm, grupo Healthatom), Doctocliq y Nimbo Clinic (LatAm multi-país), Reservo
  (Bolivia), DentiDesk (Chile), OdontoCloud y XDental (Brasil).
- **España / internacional**: Clinic Cloud (España, ligado a Doctoralia) y Nubimed (España).
  Ambos tienen cumplimiento fiscal español (Verifactu/TicketBAI) y no están planteados para la
  normativa argentina (obras sociales/prepagas), aunque Doctoralia opera en Argentina y vuelve a
  Clinic Cloud un competidor indirecto plausible.
- **Sin datos**: DentalData y Dentap (dominios caídos), OdontoSaaS (SPA vacía).

### Modelo de pricing

Predomina la suscripción mensual por cantidad de profesionales y/o sucursales. Rangos
detectados donde hay precio público: DentalSoft ARS 30.000–60.000; AgendaPro ARS
13.900–314.900; Reservo Bs 99–229; Doctocliq USD 19–49; Clinic Cloud 29€–79€; Nubimed
27,40€–50,10€. El resto (Dentalink, DentiDesk, Medilink, Nimbo, XDental, OdontoCloud,
OdontoSaaS) cobra por cotización ("solicitar demo"), típico de venta B2B enterprise. Los planes
"Gratis/prueba" existen como gancho (DentalSoft 3 meses, Doctocliq free, pruebas de 7–30 días).

### Riesgo competitivo y ventana de oportunidad

El riesgo es que vendors enterprise (Dentalink/Medilink) o genéricos baratos (Reservo,
AgendaPro) ya cubren reserva online y recordatorios, y que los dentales puros (XDental,
OdontoCloud) cubren duración/anti-conflicto por separado. Nuestra ventana está en el **corredor
de agendamiento con recurso doble**: modelar el turno como intersección de disponibilidad de
**profesional** y de **sillón/box**, con **duración derivada del tipo de prestación** y
anti-solapamiento estricto, en un producto pensado para la **realidad PyME argentina**
(obras sociales, precios en ARS, soporte local). Ningún proveedor comunica ese paquete completo.

---

## Sección D — MVP recomendado

Alcance derivado de la Sección 0 (los 5 puntos "necesarios") cruzado con el hueco de la
Sección C.

### Alcance IN (priorizado)

1. **Gestión de agenda con duración por prestación** — base del modelo; la duración del turno
   se deriva del tipo de prestación (p. ej. limpieza 30m, endodoncia 60m).
2. **Asignación simultánea de profesional y sillón/box** — recurso doble obligatorio por turno;
   es el hueco competitivo detectado en la Sección C.
3. **Prevención de solapamientos** — invariante que bloquea doble asignación de cualquiera de
   los dos recursos en la misma franja.
4. **Cancelación/reprogramación con liberación inmediata de cupo** — caso de uso explícito.
5. **Recordatorio automático** — ataca el ausentismo (principal pérdida de ingresos).

### Alcance OUT / backlog post-MVP

Los 4 funcionalidades opcionales quedan fuera de la v1:
- Odontograma interactivo 3D.
- Periodontograma avanzado.
- Integración de radiología digital.
- IA de diagnóstico.

### Reglas de negocio no negociables (invariantes verificables)

1. **Recurso doble**: un turno sólo puede confirmarse si en su franja horaria existe a la vez
   profesional disponible **y** sillón/box libre. Si falta alguno de los dos, el turno no se crea.
2. **Duración por prestación**: la duración del turno es una función del tipo de prestación
   (limpieza 30m, endodoncia 60m, y así por cada prestación definida); no es un valor fijo global.
3. **Anti-solapamiento estricto**: para un mismo profesional o un mismo sillón, un turno puede
   iniciar **en el minuto exacto** en que finaliza el anterior, pero nunca antes; el intervalo
   `[inicio, fin)` no puede intersectarse con ningún otro turno del mismo recurso.

### Integraciones del MVP (orden sugerido)

Del punto 8 de la Sección 0, en este orden de valor:
1. **WhatsApp Business API** — soporta el caso de uso #4 (confirmación vía WhatsApp) y el
   recordatorio automático (funcionalidad necesaria #5).
2. **Google Calendar** — sincronización de agenda; bajo esfuerzo, alto valor percibido.
3. **Mercado Pago (señas)** — cobro de seña; utilizable después de estabilizar el flujo de
   turnos (depende de la decisión sobre política de seña).

### Restricciones legales/técnicas desde el día 1

- **Ley 25.326 de Protección de Datos Personales (Argentina)**: tratamiento de datos personales
  de pacientes conforme a la ley.
- **No almacenar datos sensibles reales** en repositorios ni en entornos de prueba; usar datos
  sintéticos o anonimizados en desarrollo y testing.

### Riesgo principal y mitigación

**Riesgo**: agendamiento simultáneo concurrente de turnos online y recepción presencial (dos
actores pueden intentar tomar el mismo recurso en la misma franja al mismo tiempo).
**Mitigación de alto nivel**: tratar la creación de turno como una operación atómica con
control de concurrencia a nivel de recurso (profesional y sillón) — reserva transaccional /
bloqueo por franja — y verificación de disponibilidad en el momento de confirmar, no sólo al
mostrar el calendario.

### Criterios de aceptación del MVP

- [ ] Un turno no puede crearse si falta disponibilidad de **profesional** o de **sillón/box** en la franja.
- [ ] La duración del turno se calcula automáticamente según el tipo de prestación seleccionado.
- [ ] Dos turnos del mismo profesional (o del mismo sillón) no pueden solaparse; se permite
      encadenar exacto (fin de uno = inicio del siguiente).
- [ ] Una cancelación libera el cupo de ambos recursos de forma inmediata, dejándolo disponible
      para una nueva reserva.
- [ ] La reserva online 24/7 y la agenda de recepción comparten la misma fuente de disponibilidad.
- [ ] Al crearse un turno, se programa un recordatorio automático (WhatsApp) según la
      anticipación configurada.
- [ ] Un intento de doble reserva concurrente (online vs. recepción) sobre el mismo recurso
      resuelve con éxito para uno y rechazo controlado para el otro.
- [ ] No hay datos sensibles reales en el repositorio ni en los entornos de prueba.

---

## Cierre

### Supuestos

- Que los 15 proveedores listados son una muestra representativa del mercado relevante para
  consultorios odontológicos de Argentina.
- Que "No evidenciado" implica un **vacío de evidencia** (el sitio no lo publica), no una
  ausencia real de la funcionalidad; los productos B2B suelen reservar features finas para la demo.
- Que la operación modelada es sobre sillón/box como recurso físico discreto, más allá de lo que
  comuniquen los competidores.
- Que las restricciones legales se limitan a la Ley 25.326 para la v1.

### Preguntas abiertas

- **#11 (del Discovery)**: ¿Existe API oficial de WhatsApp para consultorios pequeños o se
  depende de soluciones no oficiales (riesgo de bloqueo y cumplimiento)?
- ¿La duración por prestación debe ser configurable por el consultorio (por odontólogo) o un
  catálogo fijo del sistema?
- ¿El sillón/box es una entidad de primera clase (con su propia agenda) o un atributo opcional
  del turno? ¿Puede haber turnos sin sillón (p. ej. teleconsulta)?
- ¿Cómo se comporta la anti-solapamiento ante sobreturnos/urgencias (que DentalSoft sí contempla)?
- ¿La seña con Mercado Pago es obligatoria para confirmar el turno o un extra opcional?
- ¿Se requiere multi-sucursal en la v1 o alcanza con un solo consultorio (multi-profesional)?
- ¿OdontoSaaS, DentalData y Dentap deben reintentarse con un navegador headless / URL corregida
  antes de descartarlos como competidores?

### Fuentes

Notas de investigación (esquema fijo de 8 campos):

- `discovery/sources/dentalink.md`
- `discovery/sources/dentalsoft.md`
- `discovery/sources/doctocliq.md`
- `discovery/sources/dentidesk.md`
- `discovery/sources/odontosaas.md`
- `discovery/sources/reservo.md`
- `discovery/sources/clinic-cloud.md`
- `discovery/sources/xdental.md`
- `discovery/sources/dentaldata.md`
- `discovery/sources/medilink.md`
- `discovery/sources/agenda-pro.md`
- `discovery/sources/nubimed.md`
- `discovery/sources/dentap.md`
- `discovery/sources/odontocloud.md`
- `discovery/sources/nimbo-clinic.md`

Discrepancias de dominio documentadas:

- **XDental**: consigna `xdental.com.br` (dominio estacionado/reutilizado) → producto real en
  `xdentalcontrole.com.br`.
- **OdontoCloud**: consigna `odontocloud.com.ar` (NXDOMAIN) → producto real en
  `odontocloud.com.br`.
- (Adicionales) **DentalData** (`dentaldata.com.ar`, no resuelve) y **Dentap** (`dentap.co`,
  NXDOMAIN): sin datos.

### Fecha

2026-10-15.
