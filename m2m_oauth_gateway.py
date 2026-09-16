#!/usr/bin/env python3
"""
VANE-SPACE-SLA - M2M OAuth Isolation Gateway
Machine-to-Machine OAuth 2.0 Zero-Trust Authentication & Isolation Layer
Author: MD ABUL HOSSAIN
"""
import os
import time
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
        self.signing_key = os.environ.get("M2M_SIGNING_KEY")
        if not self.signing_key:
            raise ValueError("M2M_SIGNING_KEY runtime variable must be initialized by the operator.")
        self.matrix = IsolationMatrix()

    def generate_token(self, creds: ClientCredentials, scope: str) -> Optional[str]:
        """Issues short-lived cryptographically signed M2M access claims."""
        if not self.matrix.can_access(creds.client_id, scope):
            logger.error("Scope authorization denied for client identity", client=creds.client_id, scope=scope)
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
            jwt.decode(token_str, self.signing_key, algorithms=["HS256"])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            logger.error("Token verification failure caught", reasons=str(e))
            return False
