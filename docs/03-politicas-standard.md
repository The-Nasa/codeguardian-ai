# 03 — Contrato de políticas y Quality Gate Standard

> Estado: especificación conceptual; no es un archivo de configuración ejecutable.

## Contrato por repositorio
Archivo previsto: `codeguardian.yml`. Secciones:

| Campo | Tipo conceptual | Propósito |
|---|---|---|
| `version` | entero | Versión de esquema |
| `profile` | enum | `standard` |
| `languages` | lista | Lenguajes declarados o detectados |
| `paths` | objeto | Includes/excludes |
| `rules` | lista/objeto | Reglas adicionales y excepciones aprobadas |
| `analyzers` | objeto | Herramientas habilitadas y obligatorias |
| `ai` | objeto | Activación, presupuesto, límites |
| `quality_gate` | objeto | Checks obligatorios y política de fallo |
| `reporting` | objeto | Comentario, check, artefactos |

### Precedencia de políticas
1. Controles de seguridad globales no desactivables.
2. Reglas de organización aprobadas.
3. Reglas por lenguaje.
4. Reglas locales del repositorio (solo pueden endurecer controles protegidos).

La configuración enviada dentro de un PR no puede reducir los permisos o cambiar el Quality Gate de ese mismo PR. Validar esquema y rechazar campos desconocidos.

## Catálogo inicial
| ID | Regla | Evaluador | Standard |
|---|---|---|---|
| CG-STYLE-001 | Formato y convenciones | Ruff / ESLint / Checkstyle | Warning |
| CG-QUAL-001 | Complejidad excesiva | Linter + Codex | Warning |
| CG-TYPE-001 | Errores de tipos en scope obligatorio | mypy / tsc | Block si se habilita como obligatorio |
| CG-TEST-001 | Suite de tests requerida | pytest / Jest / JUnit | Block |
| CG-SEC-001 | Secreto confirmado en cambios | Detector de secretos | Block |
| CG-SEC-002 | Riesgo de inyección | Escáner + Codex | Block solo con evidencia verificable y política explícita |
| CG-ARCH-001 | Violación de arquitectura | Codex | Warning |
| CG-DOC-001 | Documentación desactualizada | Codex | Warning |
| CG-DEVOPS-001 | Validación de infraestructura | Herramienta específica | Block si requerida |

## Severidad vs decisión
- `critical`: impacto crítico, sujeto a evidencia.
- `high`: fallo importante de seguridad o funcionalidad.
- `medium`: mantenibilidad, diseño o tipos no obligatorios.
- `low`: estilo y mejoras menores.

Severidad no implica bloqueo por sí misma. El bloqueo requiere regla obligatoria, evidencia verificable y una ejecución válida.

## Estados
| Estado lógico | Semántica | Publicación |
|---|---|---|
| PASS | Todas las validaciones requeridas exitosas | Check success |
| WARNING | Requisitos cumplidos; hay recomendaciones | Check success + advertencias |
| FAIL | Incumplimiento verificado de requisito obligatorio | Check failure |
| INCOMPLETE | No se pudo ejecutar una verificación requerida | Check no exitoso (failure o action_required según integración validada) |

**Nota:** GitHub Checks no tiene necesariamente un estado de conclusión literal `warning` o `incomplete`; esos son estados internos de CodeGuardian. Traducirlos a conclusiones GitHub válidas y a branch protection.

## Formato de hallazgo
| Campo | Tipo conceptual |
|---|---|
| `rule_id` | cadena estable |
| `source` | herramienta / codex |
| `severity` | critical/high/medium/low |
| `file`, `line` | ubicación opcional |
| `title`, `evidence`, `recommendation` | texto |
| `confidence` | estimación cualitativa, no probabilidad calibrada |
| `fingerprint` | clave estable para deduplicación |
| `commit_sha` | SHA revisado |
| `verification` | verified / suspected / not_applicable |

## Reglas de publicación
- Un resumen actualizable por PR y SHA.
- Anotaciones solo para rutas y líneas válidas del diff.
- Deduplicar hallazgos por regla, ubicación y evidencia.
- Guardar JSON estructurado; SARIF solo cuando su semántica sea adecuada.
- No publicar secretos encontrados; redactar contenido sensible.
- Rechazar hallazgos de IA que no cumplan el esquema.

## Excepciones
Solo responsables autorizados pueden aprobar excepciones, con motivo, fecha, regla, alcance y expiración. Ningún comentario libre en el PR constituye una excepción automática.

## Matriz de aceptación
| Escenario | Esperado |
|---|---|
| Tests obligatorios fallan | FAIL |
| Solo recomendación Codex | WARNING |
| Codex no disponible y requerido | INCOMPLETE |
| Política de PR intenta desactivar seguridad | Rechazo de configuración no confiable |
| PR nuevo commit | Invalidar resultado antiguo |
| Escáner encuentra secreto confirmado | FAIL con datos redactados |
