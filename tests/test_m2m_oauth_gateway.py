import time
from m2m_oauth_gateway import M2MOAuthGateway, ClientCredentials, AccessToken

def test_access_token_expiry_bounds():
    token = AccessToken("sample", expires_at=time.time() - 10)
    assert token.is_expired() is True

def test_m2m_gateway_token_lifecycle(monkeypatch):
    monkeypatch.setenv("M2M_SIGNING_KEY", "secure-testing-secret-key-distribution-matrices")
    monkeypatch.setenv("M2M_CLIENT_SECRET_TELEMETRY_VALIDATOR", "secret123")
    gateway = M2MOAuthGateway()
    
    valid_creds = ClientCredentials("telemetry_validator", "secret123")
    invalid_creds = ClientCredentials("malicious_hacker_node", "secret123")
    
    token = gateway.generate_token(valid_creds, "write")
    bad_token = gateway.generate_token(invalid_creds, "write")
    
    assert token is not None
    assert bad_token is None
    assert gateway.validate_token(token) is True

def test_m2m_gateway_rejects_wrong_client_secret(monkeypatch):
    monkeypatch.setenv("M2M_SIGNING_KEY", "secure-testing-secret-key-distribution-matrices")
    monkeypatch.setenv("M2M_CLIENT_SECRET_TELEMETRY_VALIDATOR", "expected-secret")
    gateway = M2MOAuthGateway()
    creds = ClientCredentials("telemetry_validator", "wrong-secret")
    assert gateway.generate_token(creds, "write") is None


def test_m2m_gateway_rejects_token_with_wrong_issuer(monkeypatch):
    import jwt

    monkeypatch.setenv("M2M_SIGNING_KEY", "secure-testing-secret-key-distribution-matrices")
    gateway = M2MOAuthGateway()
    token = jwt.encode(
        {"iss": "untrusted-issuer", "sub": "telemetry_validator", "scope": "write", "exp": time.time() + 60},
        gateway.signing_key,
        algorithm="HS256",
    )
    assert gateway.validate_token(token) is False
