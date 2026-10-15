# turnos-odontologia — Base de Conocimiento

Base de conocimiento del sistema de gestión de turnos para un consultorio odontológico (mono-tenant, API/backend puro). Generada a partir del informe de Discovery (`docs/discovery/informe-discovery.md`) y de las decisiones estratégicas del proyecto.

## Índice de Archivos

| Archivo | Contenido |
|---|---|
| [01_vision_y_objetivos.md](01_vision_y_objetivos.md) | Propósito, problema raíz, objetivos por actor y alcance IN/OUT del MVP |
| [02_descripcion_general.md](02_descripcion_general.md) | Stack (Java 21 / Spring Boot 3 / PostgreSQL / H2 / JUnit 5 / AssertJ), arquitectura general, integraciones y naturaleza mono-tenant + backend puro |
| [03_actores_y_roles.md](03_actores_y_roles.md) | Actores, matriz RBAC (rol × recurso), rutas públicas vs. autenticadas |
| [04_modelo_de_datos.md](04_modelo_de_datos.md) | Entidades con atributos y tipos, ERD Mermaid, invariantes y seed data sintética |
| [05_reglas_de_negocio.md](05_reglas_de_negocio.md) | Reglas `RN-NN` con justificación, invariante verificable y cómo se testean |
| [06_funcionalidades.md](06_funcionalidades.md) | Historias de usuario por épica con criterios de aceptación |
| [07_flujos_principales.md](07_flujos_principales.md) | Flujos extremo a extremo (auth, reserva, mostrador, cancelación, recordatorio) + diagramas Mermaid |
| [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md) | Patrones, estructura de directorios, concurrencia (locking + constraint de exclusión), tests, env vars y seguridad |
| [09_decisiones_y_supuestos.md](09_decisiones_y_supuestos.md) | Decisiones de diseño (DD-XX) con alternativas/trade-offs y supuestos inferidos (SU-XX) |
| [10_preguntas_abiertas.md](10_preguntas_abiertas.md) | Inconsistencias detectadas (IN-XX) y preguntas abiertas priorizadas |

## Quick Start para Desarrolladores

1. Entender el dominio → [01](01_vision_y_objetivos.md), [03](03_actores_y_roles.md)
2. Entender los datos → [04](04_modelo_de_datos.md)
3. Entender las reglas → [05](05_reglas_de_negocio.md)
4. Entender la arquitectura → [02](02_descripcion_general.md), [08](08_arquitectura_propuesta.md)
5. Implementar → [07](07_flujos_principales.md), [06](06_funcionalidades.md)
6. Antes de codificar → [10](10_preguntas_abiertas.md)

## Resumen Ejecutivo

Sistema backend puro (Java 21 + Spring Boot 3, PostgreSQL, tests con JUnit 5 + AssertJ sobre H2) para un solo consultorio odontológico. Su núcleo es el **turno como recurso doble**: cada turno requiere simultáneamente un profesional y un sillón/box libres en su franja, con duración derivada del tipo de prestación y prohibición estricta de solapamiento (se admite encadenado exacto). El principal riesgo —agendamiento concurrente entre el canal online y el mostrador— se resuelve con transacciones, locking y un **constraint de exclusión de PostgreSQL** (`EXCLUDE USING gist` con `tsrange`). Los datos clínicos y personales se rigen por la Ley 25.326, con seeds y pruebas exclusivamente sintéticos.
