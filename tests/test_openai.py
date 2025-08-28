from ai_healthcheck import check_openai
import ai_healthcheck.openai as openai_mod

class DummyResp:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text


def test_openai_success(monkeypatch):
    def fake_post(url, headers=None, json=None, timeout=None):
        return DummyResp(200, "ok")

    monkeypatch.setattr(openai_mod.requests, "post", fake_post)

    res = check_openai(
        endpoint="https://api.openai.com",
        api_key="key",
        model="gpt-4o-mini",
    )
    assert res.ok is True
    assert res.status_code == 200


def test_openai_401_returns_false(monkeypatch):
    def fake_post(url, headers=None, json=None, timeout=None):
        return DummyResp(401, "Unauthorized")

    monkeypatch.setattr(openai_mod.requests, "post", fake_post)

    res = check_openai(
        endpoint="https://api.openai.com",
        api_key="key",
        model="gpt-4o-mini",
    )
    assert res.ok is False
    assert res.status_code == 401
    assert "authentication/permission" in res.message


def test_openai_400_returns_false(monkeypatch, caplog):
    def fake_post(url, headers=None, json=None, timeout=None):
        return DummyResp(400, "Bad Request: InvalidParam")

    monkeypatch.setattr(openai_mod.requests, "post", fake_post)

    with caplog.at_level("WARNING"):
        res = check_openai(
            endpoint="https://api.openai.com",
            api_key="key",
            model="gpt-4o-mini",
        )
    assert res.ok is False
    assert res.status_code == 400
    assert "HTTP 400" in res.message


def test_openai_network_error_returns_false(monkeypatch):
    def fake_post(url, headers=None, json=None, timeout=None):
        raise RuntimeError("dns fail")

    monkeypatch.setattr(openai_mod.requests, "post", fake_post)

    res = check_openai(
        endpoint="https://api.openai.com",
        api_key="key",
        model="gpt-4o-mini",
    )
    assert res.ok is False
    assert res.status_code is None


def test_openai_404_returns_false_with_guidance(monkeypatch):
    def fake_post(url, headers=None, json=None, timeout=None):
        return DummyResp(404, "Not Found: bad path")

    monkeypatch.setattr(openai_mod.requests, "post", fake_post)

    res = check_openai(
        endpoint="https://api.openai.com",
        api_key="key",
        model="gpt-4o-mini",
    )
    assert res.ok is False
    assert res.status_code == 404
    assert "404" in res.message
    assert ("endpoint" in res.message) or ("model" in res.message)
