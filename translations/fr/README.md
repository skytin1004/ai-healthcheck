# ai-healthcheck

[![Python package](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![License: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub contributors](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Langues
[Chinois](../zh/README.md) | [Français](./README.md) | [Japonais](../ja/README.md) | [Coréen](../ko/README.md) | [Espagnol](../es/README.md)

Contrôles de santé légers pour OpenAI — pas besoin de SDK lourds.

- Appels minimaux au plan de données avec de petites charges utiles et des délais d'attente courts
- Comportement clair et prévisible (retourne toujours `HealthResult`)
- Petite empreinte d'installation (utilise uniquement `requests`)
- Parfait pour les probes de démarrage d'application et les tests sommaires CI/CD

## Installation

```bash
pip install ai-healthcheck
```

## Démarrage rapide

Définissez vos identifiants (exemple utilisant des variables d'environnement), puis lancez le contrôle.

```python
import os
from ai_healthcheck import check_openai

res = check_openai(
    endpoint=os.environ["OPENAI_ENDPOINT"],  # par exemple, https://api.openai.com
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-5-mini",
    # Optionnel : limiter à une organisation si votre compte en utilise une
    # org_id=os.environ.get("OPENAI_ORG_ID"),
)
print(res)
```

### Exemple de sortie

```python
# RésultatDeSanté(fournisseur='openai',
#              point_daccès='https://api.openai.com',
#              ok=True,
#              code_statut=200,
#              message='OpenAI accessible. Les identifiants et le modèle semblent valides.')
```

## Utilisation

```python
from ai_healthcheck import check_openai

res = check_openai(
    endpoint="https://api.openai.com",
    api_key="***",
    model="gpt-5-mini",
    # En-tête d'organisation facultatif
    # org_id="org_12345",
    timeout=10.0,
)
print(res.ok, res.status_code, res.message)
```

Comportement :
- 200 -> ok=True
- sinon (401/403 et autres codes non 2xx, ou erreurs réseau) -> ok=False avec détails

## Notes

- Utilise uniquement `requests` ; pas de dépendance SDK.
- Aucun en-tête User-Agent personnalisé n'est défini (garde les requêtes minimales).

## Résolution des problèmes

- 404 : La clé API peut être valide, mais l’endpoint/le chemin ou le nom du modèle est probablement incorrect. Vérifiez l’endpoint (par exemple, n’incluez `/v1` qu’une seule fois) et le modèle.
- 401/403 : Erreurs d’authentification/permissions. Vérifiez la clé API et l’accès au compte.

## CI/CD et probes de démarrage

Utilisez ces contrôles dans vos pipelines ou au démarrage de l’application pour échouer rapidement avec des instructions claires.

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir des issues et des pull requests sur GitHub.