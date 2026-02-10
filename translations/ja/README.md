# ai-healthcheck

[![Python package](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![License: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub contributors](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Languages
[Chinese](../zh/README.md) | [French](../fr/README.md) | [Japanese](./README.md) | [Korean](../ko/README.md) | [Spanish](../es/README.md)

OpenAI向けの軽量ヘルスチェック — 重いSDKは不要です。

- 最小限のデータプレーン呼び出し、わずかなペイロードと短いタイムアウト
- 明確で予測可能な動作（常に `HealthResult` を返す）
- 小さいインストールフットプリント（`requests` のみ使用）
- アプリケーション起動時のプローブやCI/CDのスモークテストに最適

## Installation

```bash
pip install ai-healthcheck
```

## Quickstart

環境変数を使った例など、認証情報を設定し、チェックを呼び出してください。

```python
import os
from ai_healthcheck import check_openai

res = check_openai(
    endpoint=os.environ["OPENAI_ENDPOINT"],  # 例: https://api.openai.com
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-5-mini",
    # オプション: アカウントが組織を使用している場合は、その組織に範囲を限定します
    # org_id=os.environ.get("OPENAI_ORG_ID"),
)
print(res)
```

### Sample output

```python
# HealthResult(provider='openai',
#              endpoint='https://api.openai.com',
#              ok=True,
#              status_code=200,
#              message='OpenAIに接続可能。資格情報とモデルは有効なようです。')
```

## Usage

```python
from ai_healthcheck import check_openai

res = check_openai(
    endpoint="https://api.openai.com",
    api_key="***",
    model="gpt-5-mini",
    # オプションの組織ヘッダー
    # org_id="org_12345",
    timeout=10.0,
)
print(res.ok, res.status_code, res.message)
```

動作:
- 200 -> ok=True
- それ以外（401/403やその他の非2xx、またはネットワークエラー） -> ok=False と詳細情報付き

## Notes

- `requests` のみを使用。SDK依存はありません。
- カスタムUser-Agentヘッダーは設定しません（リクエストを最小限に保つため）。

## Troubleshooting

- 404: APIキーは有効かもしれませんが、エンドポイントやパス、モデル名が間違っている可能性があります。エンドポイントを（例：`/v1` が一度だけ含まれているか）やモデル名を確認してください。
- 401/403: 認証または権限エラーです。APIキーやアカウントのアクセス権を確認してください。

## CI/CD and startup probes

これらのチェックをパイプラインやアプリ起動時に使用し、明確な指示とともに迅速に失敗させることができます。

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## Contributing

貢献は歓迎します！GitHubでissuesやプルリクエストを作成してください。