# 07 — Plan de ejecución del primer sprint

> Estado: arranque local autorizado.
> Fecha: 2026-11-02 · Perfil: Standard · Base: documentos 01–06.

## Objetivo

Dejar un núcleo Python instalable localmente, con contratos versionados y validación de configuración confiable comprobada. Es el primer tramo de la iteración A del Documento 06; Ruff/pytest como analizadores se incorporan en el sprint siguiente. Usar pytest para probar el núcleo no equivale a implementar su adaptador.

Capacidad propuesta: una semana, 8–10 horas, sin fechas de inicio comprometidas. Si solo hay 5 horas disponibles, dividir este alcance en dos semanas; mantener los mismos criterios de salida.

## Decisiones que se conservan

- CI técnica independiente de Codex; ningún fallo de IA borra un resultado técnico.
- Orquestador independiente de herramientas, con adaptadores por herramienta agrupables por lenguaje (ADR-06-02).
- Configuración efectiva desde una fuente aprobada; el contenido del PR es entrada no confiable.
- Hallazgos versionados y asociados al SHA; severidad y obligatoriedad son conceptos diferentes.
- Solo evidencia verificable de una regla obligatoria produce bloqueo Standard. Una sospecha de Codex sigue siendo una recomendación.
- Análisis sin credenciales de publicación; publicación separada, validada y ligada al SHA vigente.
- Sin autocorrección, auto-merge, dashboard ni despliegue.

## Backlog ordenado

Responsables propuestos: **implementador**, quien desarrolle el núcleo; **mantenedor**, quien apruebe políticas y diseño. Son roles por asignar, no personas confirmadas.

| Orden / ID | Tarea y entregable | Depende de | Responsable | Horas | Criterio de aceptación |
|---|---|---|---|---:|---|
| 1 / S1-01 | Cerrar decisiones de arranque y registrar resolución de contratos | — | Mantenedor + implementador | 1 | Registro distingue decisiones aprobadas, propuestas y diferidas; no quedan nombres ambiguos para campos de identidad, evidencia y adaptadores. |
| 2 / S1-02 | Crear paquete, metadatos de instalación y estructura mínima del Documento 04 | S1-01 y aprobación de inicio | Implementador | 1 | Paquete instalable en entorno limpio; importación del núcleo y ejecución de tests documentadas; sin workflows activos. |
| 3 / S1-03 | Definir esquemas y modelos de identidad, configuración, Finding, AnalyzerResult y QualityDecision; documentar ReviewRequest y ReviewResult | S1-02 | Implementador | 2 | Ejemplos válidos/ inválidos; versión explícita, enums y campos requeridos; rechazo de claves desconocidas; SHA y policy_version preservados. |
| 4 / S1-04 | Implementar validación y resolución mínima de política Standard con fuentes explícitas | S1-03 | Implementador | 2 | Configuración inválida produce error explícito; fuente del PR no puede reemplazar política aprobada; reglas locales no debilitan controles protegidos. |
| 5 / S1-05 | Declarar interfaz de adaptadores y fixtures sintéticas de resultados | S1-03 | Implementador | 1 | Interfaz incluye identificación, detección, planificación, ejecución aislada y normalización; fixtures representan éxito, hallazgos, error y omisión; sin ejecutar código de PR. |
| 6 / S1-06 | Verificar aceptación, actualizar guía local y revisar trazabilidad | S1-04, S1-05 | Implementador + mantenedor | 1 | Pruebas de contratos y políticas pasan; guía reproducible; pendientes y límites documentados. |

Total previsto: 8 horas y hasta 2 horas de margen. Trabajar en ese orden para mantener cambios pequeños y revisables; no ampliar alcance si sobra margen.

## Resoluciones necesarias en S1-01

Los documentos 03/05 y 06 tienen diferencias de nombres, no una migración de esquema aprobada. Antes de crear modelos se propone:

| Diferencia | Propuesta para aprobar |
|---|---|
| repository_full_name / repository; pull_request_number / pr_number; commit_sha / head_sha | Usar repository, pr_number y head_sha del Documento 06, conservando base_sha y metadatos de ejecución del 05. Documentar equivalencias; no aceptar alias silenciosamente. |
| verification / evidence_status | Usar evidence_status con verified, suspected y unverified del 06. Resolver explícitamente not_applicable del 03 como ausencia de evaluación aplicable, sin convertirlo en evidencia verificada. |
| execute/detect frente a supports/plan/run | Usar supports, plan, run y normalize del 06; conservar requisitos, versiones, timeout y restricciones de confianza del 05. |
| blocking_rule en Finding | Calcularlo desde política efectiva; nunca confiar en el valor propuesto por IA o por el PR. |

Estas propuestas no sustituyen decisiones aprobadas: registrar la resolución y actualizar los documentos afectados antes de programar.

## Decisiones pendientes del Documento 06

La aprobación de arranque debe registrar las siete decisiones pendientes, incluso cuando se difieran con un hito explícito.

| Tema | Propuesta para este sprint | Hito de resolución |
|---|---|---|
| Autenticación y presupuesto Codex | Diferir; sin llamadas IA en sprint 1 | Antes del sprint de integración Codex |
| PR externos | Núcleo probado con datos sintéticos; propuesta de modo restringido sin tests dinámicos externos hasta validar aislamiento | Antes de activar análisis de PR externos |
| Generación/publicación de checks | Conservar separación técnico/IA; diferir mecanismo de publicación | Antes de implementar reporter/workflows |
| Versión e instalación gh-aw | Diferir selección y verificación oficial; no generar lock ni asumir sintaxis | Antes del workflow agéntico |
| Límites de ejecución | Modelar límites explícitos; 40 archivos IA sigue siendo propuesta del 02, sin valor operativo aprobado | Antes de ejecutar analizadores y, para presupuesto IA, antes de Codex |
| Repositorio demo y administrador de reglas | Proponer examples/python-demo local; mantenedor por asignar | Aprobar responsable antes de S1-04; elegir repo remoto antes de prueba integral |
| Estados internos → GitHub | Conservar PASS/WARNING exitosos y FAIL/INCOMPLETE no exitosos; diferir conclusión concreta | Antes de publicar checks y probar protección de ramas |

El cierre puede aprobar un inicio limitado al núcleo local y dejar integraciones diferidas. La autorización del arranque local consta en el registro de ejecución.

## Validación y Definition of Done

- Instalación e importación reproducibles en un entorno limpio.
- Contratos aceptan fixtures válidas y rechazan tipos, enums, campos desconocidos y campos obligatorios ausentes.
- Pruebas comprueban precedencia, intento de debilitamiento local y política propuesta desde un PR (cobertura parcial de T-09 del Documento 06).
- Fixtures distinguen hallazgo confirmado, sospecha IA y ejecución incompleta; no se afirma que el Quality Gate esté implementado.
- Contrato de adaptador no importa Ruff ni contiene lógica Python específica en el orquestador.
- Documentación, ejemplos y decisiones coinciden; no hay credenciales ni integración remota activada.
- Revisión del mantenedor completa y pendientes registrados. Las pruebas integrales T-01–T-12 del Documento 06 siguen pendientes, salvo la porción de T-09 indicada.

## Continuación prevista

Sprint 2: inspección de cambios, adaptadores Ruff/pytest, normalización y motor de decisión local con PASS, WARNING, FAIL e INCOMPLETE. Después: publicación y obsolescencia de SHA; integración Codex; aceptación de seguridad y reutilización. Los límites de confianza se aplican desde el primer componente, aunque sus pruebas integrales lleguen después.

Este plan detalla la semana de fundamentos del Documento 04 sin comprometer de nuevo la estimación global de cinco semanas. Revisar capacidad y duración restante al cerrar el sprint.

## Registro de ejecución

El usuario autorizó el arranque local del sprint 1. Se adoptaron los nombres
repository, pr_number, head_sha y evidence_status del Documento 06.
El adaptador sigue supports, plan, run y normalize. La obligatoriedad se
resuelve desde la política efectiva, fuera del contrato de hallazgo recibido.
Se usan casos sintéticos locales y queda pendiente asignar al mantenedor que
aprobará reglas para repositorios reales.

ReviewRequest vinculará la identidad con el inventario, los límites y la
política efectiva. ReviewResult conservará el SHA, versión de política,
resultados por herramienta, hallazgos, cobertura y motivos de revisión
incompleta. Ambos se materializarán al incorporar el orquestador.

La autorización cubre el núcleo local. Las decisiones de integración mantienen
los hitos de la tabla anterior.
