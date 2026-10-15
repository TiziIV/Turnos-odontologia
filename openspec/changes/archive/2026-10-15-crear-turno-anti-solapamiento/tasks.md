# Tasks

## 1. Revisión y base mínima

- [x] 1.1 Ajustar real de Propose (2026-10-15, Juan Martín García): tres escenarios DADO/CUANDO/ENTONCES fijos; ISO 8601 con zona y UTC; sin login, PostgreSQL ni cancelación. Artefactos de planificación actualizados. Captura real en `docs/evidencias/etapa-6-propose-ajustar.png`.
- [x] 1.2 Crear estructura hexagonal y pyproject para Python 3.12+, fijar dependencias compatibles en entorno virtual y archivo reproducible; verificar instalación e importación de la aplicación mínima, registrar versiones y comandos en README.

## 2. Dominio y aplicación mediante TDD

- [x] 2.1 Escribir tests puros RN-01/02/03/09/10/11/13 y RN-07 parcial para duración 20/30/40/60, enum, recursos activos, intersección por cada recurso, borde exacto, un minuto, contención, recursos distintos y estados finales. La corrida roja aislada no se conservó: dominio y tests se escribieron en la misma sesión de Apply; la evidencia ejecutable es la suite verde.
- [x] 2.2 Implementar entidades, puertos y reglas puras hasta pasar los tests anteriores; verificar además rechazo de intervalos inválidos y datetimes sin zona, equivalencia de offsets y ausencia de imports de frameworks en dominio. Documentar correspondencia requisito/escenario/test.
- [x] 2.3 Escribir tests de aplicación sobre referencias faltantes, estado PENDIENTE/canal ONLINE, cálculo de fin, guardado único y agenda intacta al rechazar; implementar caso de uso y repositorio en memoria; suite verde registrada.
- [x] 2.4 Incorporar fixtures sintéticos basados en KB04, sin reservas al inicio y sin datos reales; verificar RN-06 mediante revisión y tests de convenciones, aislamiento de instancias y reinicio. Documentar IDs y pérdida de datos en README.

## 3. API y ejecución reproducible

- [x] 3.1 Escribir tests HTTP para los tres escenarios principales y errores 422 (referencias, recursos, campos extra, IDs e inicio inválidos); implementar exclusivamente POST `/api/public/turnos` y verificar 201/409/422 con cliente de tests, sin exponer rutas privadas ni datos ajenos en errores.
- [x] 3.2 Completar README con venv/instalación, `python -m pytest`, Uvicorn en loopback con un worker, ejemplos PowerShell para éxito/conflicto/borde y limitaciones; instalación y pytest ejecutados en este entorno (Python 3.13.7). Uvicorn de demo no se dejó corriendo.
- [x] 3.3 Configurar CI básico con instalación reproducible y pytest, incluyendo chequeos sintéticos; verificar localmente el comando del workflow y distinguir ese resultado de una ejecución remota de Actions.

## 4. Verificación integrada y evidencias

- [x] 4.1 Ejecutar suite completa y revisión contra todos los escenarios; completar informe Verify con comandos, resultados reales, trazabilidad y límites RN-16/persistencia pendientes. Informe en `docs/opsx/verify-crear-turno-anti-solapamiento.md`. Captura real en `docs/evidencias/etapa-6-tests-verde.png` (`python -m pytest`, 74 passed).
- [x] 4.2 Validar el change con OpenSpec y revisar diff/documentación con el alcance académico; verificar que no se afirman CRUDs, auth, cancelación ni concurrencia entregados y que todas las tareas implementadas tienen evidencia antes de marcarlas completas.

## Workflow follow-up

- Archive sólo después de implementación, Verify y revisión: ejecutar flujo oficial, sincronizar specs y capturar resultado real en `docs/evidencias/`; comprobar ruta archivada y actualizar el roadmap con el alcance efectivamente entregado.
- Guardar decisiones en Engram y recuperar contexto desde una sesión posterior; capturar consulta y respuesta reales, sin atribuir recuerdos nuevos a sesiones anteriores.
- Conservar evidencias de Tiziano y distinguir las de Juan; preparar commits propios y subida autorizada sin inventar autoría ni resultados.
- Completar PDF, revisión conjunta de fuentes, reflexión propia y guion/video según la consigna; estos entregables académicos no amplían la funcionalidad de este change.
