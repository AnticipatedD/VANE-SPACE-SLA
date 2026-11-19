"""Health-check tests for the M2M OAuth gateway."""

from m2m_oauth_gateway import health_check


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
