# ai-healthcheck

[![Python package](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![License: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub contributors](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Idiomas
[Chinese](../zh/README.md) | [French](../fr/README.md) | [Japanese](../ja/README.md) | [Korean](../ko/README.md) | [Spanish](./README.md)

Comprobaciones de salud ligeras para OpenAI — sin necesidad de SDKs pesados.

- Llamadas mínimas al plano de datos con cargas útiles pequeñas y tiempos de espera cortos
- Comportamiento claro y predecible (siempre devuelve `HealthResult`)
- Huella de instalación pequeña (sólo usa `requests`)
- Perfecto para sondas de inicio de aplicaciones y pruebas rápidas de CI/CD

## Instalación

```bash
pip install ai-healthcheck
```

## Inicio rápido

Configure sus credenciales (ejemplo usando variables de entorno), luego ejecute la comprobación.

```python
import os
from ai_healthcheck import check_openai

res = check_openai(
    endpoint=os.environ["OPENAI_ENDPOINT"],  # p. ej., https://api.openai.com
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-5-mini",
    # Opcional: limitar a una organización si su cuenta usa una
    # org_id=os.environ.get("OPENAI_ORG_ID"),
)
print(res)
```

### Salida de ejemplo

```python
# ResultadoSalud(proveedor='openai',
#              endpoint='https://api.openai.com',
#              ok=True,
#              código_estado=200,
#              mensaje='OpenAI accesible. Las credenciales y el modelo parecen válidos.')
```

## Uso

```python
from ai_healthcheck import check_openai

res = check_openai(
    endpoint="https://api.openai.com",
    api_key="***",
    model="gpt-5-mini",
    # Encabezado de organización opcional
    # org_id="org_12345",
    timeout=10.0,
)
print(res.ok, res.status_code, res.message)
```

Comportamiento:
- 200 -> ok=True
- de lo contrario (401/403 y otros códigos distintos de 2xx, o errores de red) -> ok=False con detalles

## Notas

- Usa sólo `requests`; sin dependencia de SDK.
- No se establece un encabezado User-Agent personalizado (para mantener las solicitudes mínimas).

## Solución de problemas

- 404: La clave API puede ser válida, pero es probable que el endpoint/ruta o el nombre del modelo sean incorrectos. Verifique el endpoint (por ejemplo, incluya `/v1` sólo una vez) y el modelo.
- 401/403: Errores de autenticación/permisos. Verifique la clave API y el acceso a la cuenta.

## CI/CD y sondas de inicio

Use estas comprobaciones en sus pipelines o al iniciar su aplicación para fallar rápido con indicaciones claras.

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abra issues y pull requests en GitHub.