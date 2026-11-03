# codeguardian-ai
AI-powered multilingual code reviewer using GitHub Actions

## Desarrollo local

Con Python 3.12 o posterior, desde la raíz del repositorio:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install ".[test]"
.venv/Scripts/python -m pytest
```

El archivo codeguardian.yml muestra una política Standard. El llamador verifica
la procedencia antes de marcar una política como aprobada. El núcleo valida el
esquema y comprueba que las capas locales preserven los requisitos heredados.
Los esquemas se distribuyen dentro del paquete en codeguardian/schemas.

## Revisión técnica local

Instala las herramientas con `pip install ".[review]"`. Desde el entorno
instalado, indica un checkout confiable y limpio, el SHA base y el SHA de HEAD.
Pasa una copia aprobada de codeguardian.yml ubicada fuera del checkout revisado.

```powershell
python -m codeguardian.review C:/ruta/demo --base $baseSha --head $headSha --policy C:/ruta/codeguardian.yml --trusted
```

Ruff revisa archivos Python modificados y pytest ejecuta la suite del proyecto.
La salida JSON incluye el SHA, la versión de política y los resultados.
PASS y WARNING devuelven 0, FAIL devuelve 1 e INCOMPLETE devuelve 2. Una
suite sin tests o que no pueda ejecutarse deja la revisión INCOMPLETE.
Los límites locales iniciales son 30 s para Ruff y 120 s para pytest.

El modo local ejecuta código de tests con los permisos del usuario. Úsalo
solo con código de confianza. La ejecución para PR externos requiere un
entorno aislado y queda para la integración con GitHub.

## Check técnico en GitHub Actions

El workflow Python CI inicia el check **CodeGuardian Technical** al abrir,
actualizar o reabrir un PR. El piloto cubre ramas del mismo repositorio
dirigidas a la rama por defecto. Protege esa rama y limita el acceso de
escritura a colaboradores de confianza antes de activar el piloto. Los forks
y Dependabot quedan como INCOMPLETE antes de descargar código.

El motor y la política provienen del commit base. El análisis usa el SHA
exacto del PR, visible en el resumen y en el artefacto codeguardian-review.
GitHub asocia el check nativo al contexto del evento pull_request. PASS y
WARNING completan el job con éxito. FAIL e INCOMPLETE fallan el job.

Para la primera ejecución, incorpora primero el motor, la política y el
workflow a la rama por defecto. Después abre un PR interno de prueba y
comprueba el resumen y el JSON. Activa la regla de check obligatorio después
de validar ese PR y decidir cómo se aceptarán contribuciones desde forks.

## Piloto manual de Gemini

El workflow CodeGuardian Gemini Pilot revisa hasta 20 archivos cambiados y
24 KB de diff Python de un PR interno abierto. La inferencia es independiente
del check técnico. El resultado se consulta en la ejecución de Actions como
vista previa. El diff se envía a la API de Gemini.

Para activarlo, incorpora codex-review.md y su lock generado a main.
En Settings → Secrets and variables → Actions crea GEMINI_API_KEY con una
clave de un proyecto Free Tier de Google AI Studio con acceso a gemini-3.5-flash-lite.
Después ve a Actions → CodeGuardian Gemini Pilot → Run workflow, elige main
y proporciona el número de un PR interno de prueba que siga abierto.

Usa datos sintéticos en la primera ejecución. Comprueba que el resultado
cita el SHA y que Ruff y pytest conservan su propio check. Si el PR recibió
commits después de iniciar la revisión, vuelve a ejecutar el piloto.

Regenera el lock con gh-aw v1.0.1 y este comando:

```powershell
gh aw compile codex-review --strict --action-tag 0627fdbe4beb5f3b71aa569f8d97150b87f2111a
```

## Revisión automática de Gemini

Gemini se ejecuta al abrir, actualizar, reabrir o marcar como listo un PR
interno hacia main. Cada ejecución elegible usa la cuota de Gemini. Los
borradores, forks y PR de Dependabot quedan fuera de la revisión automática.
El piloto conserva los límites de 20 archivos cambiados y 24 KB de diff Python.
Run workflow sigue disponible para reintentar desde main.

Cuando cambia el commit del PR, el comentario previo se marca como obsoleto.
Si Gemini completa la revisión del nuevo commit, actualiza ese comentario
con el nuevo SHA y los hallazgos. El check técnico sigue siendo independiente.
