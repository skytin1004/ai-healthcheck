# ai-healthcheck

[![Python package](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![License: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub contributors](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 语言
[中文](../zh/README.md) | [法语](../fr/README.md) | [日语](../ja/README.md) | [韩语](../ko/README.md) | [西班牙语](../es/README.md)

OpenAI 的轻量级健康检查 — 不需要重型 SDK。

- 最少的数据平面调用，载荷小，超时短
- 清晰、可预测的行为（始终返回 `HealthResult`）
- 安装体积小（仅使用 `requests`）
- 非常适合应用启动探针和 CI/CD 冒烟测试

## 安装

```bash
pip install ai-healthcheck
```

## 快速开始

设置您的凭证（使用环境变量的示例），然后调用检查。

```python
import os
from ai_healthcheck import check_openai

res = check_openai(
    endpoint=os.environ["OPENAI_ENDPOINT"],  # 例如，https://api.openai.com
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-5-mini",
    # 可选：如果您的账户使用组织，则限定到该组织范围
    # org_id=os.environ.get("OPENAI_ORG_ID"),
)
print(res)
```

### 示例输出

```python
# HealthResult(provider='openai',
#              endpoint='https://api.openai.com',
#              ok=True,
#              status_code=200,
#              message='OpenAI 可访问。凭据和模型似乎有效。')
```

## 使用方法

```python
from ai_healthcheck import check_openai

res = check_openai(
    endpoint="https://api.openai.com",
    api_key="***",
    model="gpt-5-mini",
    # 可选的组织标题
    # org_id="org_12345",
    timeout=10.0,
)
print(res.ok, res.status_code, res.message)
```

行为:
- 200 -> ok=True
- 其他（401/403 和其他非 2xx，或网络错误）-> ok=False 并带详细信息

## 注意事项

- 仅使用 `requests`，无 SDK 依赖。
- 不设置自定义的 User-Agent 头（保持请求最小化）。

## 故障排查

- 404：API 密钥可能有效，但端点/路径或模型名称可能不正确。请确认端点（例如，只包含一次 `/v1`）和模型。
- 401/403：认证/权限错误。检查 API 密钥和账户访问权限。

## CI/CD 和启动探针

在您的流水线或应用启动中使用这些检查，快速失败并提供明确指导。

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## 贡献

欢迎贡献！请在 GitHub 上创建 Issues 和 Pull Requests。