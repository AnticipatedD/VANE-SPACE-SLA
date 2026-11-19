#!/usr/bin/env python3
"""
VANE-SPACE-SLA - M2M OAuth Isolation Gateway
Machine-to-Machine OAuth 2.0 Zero-Trust Authentication & Isolation Layer
Author: MD ABUL HOSSAIN
"""
import os
import json
import time
import hmac
from typing import Dict, Optional
import jwt
import structlog

logger = structlog.get_logger()

class AccessToken:
    def __init__(self, token_str: str, expires_at: float):
        self.token_str = token_str
        self.expires_at = expires_at

    def is_expired(self) -> bool:
        """Evaluates token lifecycle bounds against absolute epoch times."""
        return time.time() >= self.expires_at

class ClientCredentials:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

class IsolationMatrix:
    def __init__(self) -> None:
        # Strict permission mappings bypassing raw dictionary structures
        self._access_matrix: Dict[str, list] = {
            "telemetry_validator": ["read", "write"],
            "voice_agent_node": ["read"]
        }

    def can_access(self, client_identity: str, requested_scope: str) -> bool:
        """Determines boundary authorization across isolated system scopes."""
        allowed_scopes = self._access_matrix.get(client_identity, [])
        return requested_scope in allowed_scopes

class M2MOAuthGateway:
    def __init__(self) -> None:
        signing_key = os.environ.get("M2M_SIGNING_KEY")
        if not signing_key:
            raise ValueError("M2M_SIGNING_KEY runtime variable must be initialized by the operator.")
        self.signing_key: str = signing_key
        self.matrix = IsolationMatrix()

    def _verify_client_secret(self, creds: ClientCredentials) -> bool:
        """Compare the supplied client secret with its environment-managed value."""
        secret_name = f"M2M_CLIENT_SECRET_{creds.client_id.upper().replace('-', '_')}"
        expected_secret = os.environ.get(secret_name)
        return bool(
            expected_secret
            and creds.client_secret
            and hmac.compare_digest(creds.client_secret, expected_secret)
        )

    def generate_token(self, creds: ClientCredentials, scope: str) -> Optional[str]:
        """Issue a short-lived token only after scope and client-secret verification."""
        if not self.matrix.can_access(creds.client_id, scope):
            logger.error("Scope authorization denied for client identity", client=creds.client_id, scope=scope)
            return None
        if not self._verify_client_secret(creds):
            logger.error("Client credential verification failed", client=creds.client_id)
            return None

        payload = {
            "iss": "vane-space-auth",
            "sub": creds.client_id,
            "scope": scope,
            "exp": time.time() + 3600
        }
        return jwt.encode(payload, self.signing_key, algorithm="HS256")

    def validate_token(self, token_str: str) -> bool:
        """Validates incoming tokens against structural signatures."""
        try:
            claims = jwt.decode(
                token_str,
                self.signing_key,
                algorithms=["HS256"],
                issuer="vane-space-auth",
            )
            client_id = claims.get("sub")
            scope = claims.get("scope")
            return (
                isinstance(client_id, str)
                and isinstance(scope, str)
                and self.matrix.can_access(client_id, scope)
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            logger.error("Token verification failure caught", reasons=str(e))
            return False

def health_check() -> Dict[str, object]:
    """Return a non-secret readiness snapshot for the M2M signing dependency."""
    configured = bool(os.environ.get("M2M_SIGNING_KEY"))
    return {
        "status": "ok" if configured else "error",
        "checks": {
            "m2m_signing_key": "configured" if configured else "missing",
        },
    }


def main() -> int:
    """Emit a machine-readable readiness status for CLI health probes."""
    result = health_check()
    print(json.dumps(result))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
