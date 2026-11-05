---
name: revisar-escenarios-turno
description: Revisa una spec de turnos odontológicos antes de implementarla. Usar cuando se escribe o se corrige una spec de agenda, reserva, enlace, espera, confirmación, cancelación o reprogramación, aunque no se nombre la palabra spec.
---

# Revisar escenarios de turno

La ficha del paciente ya existe en el catálogo sintético. No inventes otro identificador de persona.

## Procedimiento

1. Leer `knowledge-base/05_reglas_de_negocio.md`, RN-01, RN-02 y RN-03.
2. Comprobar que la spec tenga tres escenarios: uno que se acepta, uno que se rechaza por negocio y uno de borde.
3. El borde válido es `fin` de uno igual a `inicio` del siguiente. Un minuto de cruce se rechaza.
4. Si el candidato comparte profesional y sillón con un turno activo, también se rechaza. No alcanza con probar un solo recurso.
5. La duración sale de la prestación. El cliente no fija el fin.

## Criterio de revisión

Si falta el caso en que chocan los dos recursos a la vez, la spec no está lista para Apply. Corregir el papel antes de programar.
