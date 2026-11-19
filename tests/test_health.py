"""Health-check tests for the M2M OAuth gateway."""

import json
from m2m_oauth_gateway import health_check, main


def test_health_check_reports_ok_when_signing_key_is_configured(monkeypatch):
    monkeypatch.setenv("M2M_SIGNING_KEY", "test-only-signing-key")

    assert health_check() == {
        "status": "ok",
        "checks": {"m2m_signing_key": "configured"},
    }


def test_health_check_reports_error_when_signing_key_is_missing(monkeypatch):
    monkeypatch.delenv("M2M_SIGNING_KEY", raising=False)

    assert health_check() == {
        "status": "error",
        "checks": {"m2m_signing_key": "missing"},
    }


def test_health_cli_emits_json_and_returns_success(monkeypatch, capsys):
    monkeypatch.setenv("M2M_SIGNING_KEY", "a-test-signing-key-for-health-probe")
    assert main() == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ok"
    assert payload["checks"]["m2m_signing_key"] == "configured"


def test_health_cli_returns_failure_when_signing_key_is_missing(monkeypatch, capsys):
    monkeypatch.delenv("M2M_SIGNING_KEY", raising=False)
    assert main() == 1
    assert json.loads(capsys.readouterr().out)["status"] == "error"
