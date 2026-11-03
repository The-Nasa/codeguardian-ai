# 04 — Plan de implementación del MVP

> Estado: planificación · Duración estimada: 5 semanas (5–10 h/semana, revisable)

## Objetivo de la primera entrega
Revisar un PR Python con Ruff, pytest y Codex; consolidar hallazgos, publicar reporte y emitir un check que respete el perfil Standard.

## Incluido / excluido
| Incluido | Excluido del MVP |
|---|---|
| PR opened/synchronize | Push directo a rama principal |
| Ruff y pytest | Dashboard web |
| Codex con gh-aw | Autocorrección y auto-merge |
| Quality Gate y reporte | Despliegues a AWS |
| Configuración mínima | Soporte Java/TS completo |
| Contratos de adaptadores | Distribución multirepo probada |

## Estructura objetivo
```text
codeguardian-ai/
├── .github/workflows/
│   ├── code-review.md
│   ├── code-review.lock.yml
│   └── python-ci.yml
├── codeguardian/
│   ├── core/{config,detector,policy_engine,findings}.py
│   ├── analyzers/{base,python_analyzer}.py
│   └── reporting/{aggregator,reporter}.py
├── rules/{global,python}/
├── schemas/{config.schema.json,finding.schema.json}
├── tests/{unit,integration,fixtures}/
├── examples/python-demo/
├── docs/
├── codeguardian.yml
├── pyproject.toml
└── README.md
```
Los nombres son propuestos; se ajustarán durante implementación. `.lock.yml` es salida generada, no editada a mano.

## Plan por semanas
### Semana 1 — Fundamentos
- Crear estructura del paquete y documentación.
- Definir contratos de configuración, hallazgos y adaptadores.
- Pruebas unitarias de validación de política.
- **Salida:** esquema validado y proyecto instalable localmente.

### Semana 2 — Análisis técnico
- Integrar Ruff y pytest como adaptadores.
- Capturar errores, timeouts y resultados.
- Normalizar findings y pruebas.
- **Salida:** análisis técnico reproducible sin IA.

### Semana 3 — Codex / Agentic Workflows
- Verificar versión de `gh-aw`, motor y autenticación.
- Crear workflow Markdown y compilar `.lock.yml`.
- Diseñar instrucciones con contexto acotado y safe outputs.
- **Salida:** revisión de PR de demostración sin permisos de escritura en el job del agente.

### Semana 4 — Reporte y Quality Gate
- Consolidar resultados técnicos y de IA.
- Deduplicar y publicar resumen/check.
- Probar PASS, WARNING, FAIL e INCOMPLETE.
- **Salida:** flujo completo en un PR.

### Semana 5 — Seguridad y aceptación
- Pruebas con PR externos, inyección de instrucciones y secretos ficticios.
- Verificar cancelación por SHA, permisos y presupuesto.
- Documentar instalación, limitaciones y demo.
- **Salida:** MVP evaluable para portafolio.

## Escenarios de prueba
1. Código correcto → PASS.
2. Error de formato → WARNING según política.
3. pytest falla → FAIL.
4. Codex detecta posible error no confirmado → WARNING.
5. Codex falla y es requerido → INCOMPLETE.
6. PR intenta modificar políticas protegidas → no se aceptan cambios de política.
7. PR malicioso intenta ejecutar instrucciones en agente → no obtiene permisos.
8. PR actualizado → descartar resultado obsoleto.

## Definition of Done
- CI y revisión IA tienen resultados visibles.
- Reporte incluye evidencia, SHA y versión de política.
- No se filtran secretos.
- Tests unitarios e integración pasan.
- Documentación permite reproducir el MVP.

## Dependencias
Git, GitHub CLI, extensión `github/gh-aw`, Python, GitHub Actions, motor Codex configurado y credenciales apropiadas para su modalidad de ejecución. Confirmar disponibilidad, cuotas y costos antes de habilitar runs.
