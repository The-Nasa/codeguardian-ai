# Documentación — CodeGuardian AI

Repositorio: https://github.com/The-Nasa/codeguardian-ai

Este directorio conserva las decisiones de planificación del agente revisor multilenguaje con GitHub Actions, GitHub Agentic Workflows y OpenAI Codex. El núcleo local del sprint 1 se desarrolla en el paquete codeguardian.

## Índice

1. [Visión y arquitectura general](01-vision-arquitectura.md)
2. [Arquitectura híbrida](02-arquitectura-hibrida.md)
3. [Políticas y perfil Standard](03-politicas-standard.md)
4. [Plan de implementación del MVP](04-plan-implementacion-mvp.md)
5. [Especificación técnica](05-especificacion-tecnica.md)

## Estado
- Arquitectura y perfil Standard: acordados como diseño.
- MVP Python: pendiente de implementación.
- Soporte multilenguaje y distribución entre repositorios: planeados.

## Principios
- Validaciones técnicas reproducibles + recomendaciones de Codex.
- IA sin permisos de escritura directa.
- Política confiable, SHA fijo y reportes auditables.
- Ningún merge o despliegue automático en MVP.

## Uso
Copiar `docs/` al repositorio y revisar cada documento mediante pull requests. Registrar nuevas decisiones y actualizar este índice conforme evolucione el proyecto.

## Continuación del diseño
6. [Diseño interno del motor de revisión](06-diseno-motor-revision.md)
7. [Plan de ejecución del primer sprint](07-plan-primer-sprint.md)

Documento 07: arranque del núcleo local autorizado.
