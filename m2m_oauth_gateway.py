#!/usr/bin/env python3
"""
VANE-SPACE-SLA - M2M OAuth Isolation Gateway
Machine-to-Machine OAuth 2.0 Zero-Trust Authentication & Isolation Layer
Author: MD ABUL HOSSAIN
"""

import os
import json
import time
import uuid
import logging
import hmac
import hashlib
from typing import Dict, Any, Optional, Tuple
from enum import Enum
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
)
logger = logging.getLogger("m2m_oauth_gateway")


class AuthenticationMethod(Enum):
    """Supported M2M authentication methods."""
    CLIENT_CREDENTIALS = "client_credentials"
    JWT_BEARER = "urn:ietf:params:oauth:grant-type:jwt-bearer"
    MUTUAL_TLS = "mutual_tls"


class IsolationLevel(Enum):
    """Data isolation levels."""
    STRICT = "strict"
    MODERATE = "moderate"
    RELAXED = "relaxed"


@dataclass
class ClientCredentials:
    """M2M client credentials."""
    client_id: str
    client_secret: str
    scope: str
    audience: str
    isolation_level: IsolationLevel = IsolationLevel.STRICT
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AccessToken:
    """OAuth 2.0 access token."""
    token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    scope: str = ""
    issued_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str = ""
    claims: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.expires_at:
            exp_time = datetime.fromisoformat(self.issued_at.replace('Z', '+00:00')) + timedelta(seconds=self.expires_in)
            self.expires_at = exp_time.isoformat()

    def is_expired(self) -> bool:
        """Check if token is expired."""
        expiry = datetime.fromisoformat(self.expires_at.replace('Z', '+00:00'))
        return datetime.now(timezone.utc) > expiry

    def to_header(self) -> str:
        """Format for Authorization header."""
        return f"{self.token_type} {self.token}"


@dataclass
class IsolationMatrix:
    """Data isolation domain matrix."""
    matrix_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    client_id: str = ""
    allowed_resources: list = field(default_factory=list)
    allowed_actions: list = field(default_factory=list)
    denied_resources: list = field(default_factory=list)
    isolation_level: IsolationLevel = IsolationLevel.STRICT
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def can_access(self, resource: str, action: str) -> bool:
        """Check if client can access resource with action."""
        # Check deny list first (explicit deny)
        if resource in self.denied_resources:
            return False
        
        # Strict isolation: only allow explicitly listed resources
        if self.isolation_level == IsolationLevel.STRICT:
            return resource in self.allowed_resources and action in self.allowed_actions
        
        # Moderate: allow most resources except denied
        elif self.isolation_level == IsolationLevel.MODERATE:
            return action in self.allowed_actions
        
        # Relaxed: allow everything except explicitly denied
        else:
            return resource not in self.denied_resources


class M2MOAuthGateway:
    """Machine-to-Machine OAuth 2.0 Gateway with Zero-Trust Isolation."""

    def __init__(self, issuer_id: str = "vane-m2m-gateway", signing_key: Optional[str] = None):
        self.issuer_id = issuer_id
        self.signing_key = signing_key or os.getenv("M2M_SIGNING_KEY", "demo-signing-key-12345")
        self.gateway_id = f"gateway-{str(uuid.uuid4())[:8]}"
        
        # Internal stores
        self.registered_clients: Dict[str, ClientCredentials] = {}
        self.issued_tokens: Dict[str, AccessToken] = {}
        self.isolation_matrices: Dict[str, IsolationMatrix] = {}
        self.audit_log: list = []
        
        logger.info(f"M2MOAuthGateway initialized: {self.gateway_id}")

    def register_client(self, client_id: str, scope: str, audience: str,
                       isolation_level: IsolationLevel = IsolationLevel.STRICT) -> ClientCredentials:
        """Register new M2M client."""
        if client_id in self.registered_clients:
            logger.warning(f"Client {client_id} already registered")
            return self.registered_clients[client_id]
        
        # Generate secure client secret
        client_secret = self._generate_secure_secret()
        
        credentials = ClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            audience=audience,
            isolation_level=isolation_level
        )
        
        self.registered_clients[client_id] = credentials
        
        # Create isolation matrix
        isolation_matrix = IsolationMatrix(
            client_id=client_id,
            isolation_level=isolation_level,
            allowed_resources=[],
            allowed_actions=["read", "write", "delete"]
        )
        self.isolation_matrices[client_id] = isolation_matrix
        
        self._audit_log("CLIENT_REGISTERED", {"client_id": client_id, "isolation_level": isolation_level.value})
        logger.info(f"Client registered: {client_id}")
        
        return credentials

    def _generate_secure_secret(self) -> str:
        """Generate cryptographically secure client secret."""
        random_bytes = os.urandom(32)
        return hashlib.sha256(random_bytes).hexdigest()

    def authenticate_client(self, client_id: str, client_secret: str,
                           method: AuthenticationMethod = AuthenticationMethod.CLIENT_CREDENTIALS) -> Tuple[bool, Optional[AccessToken]]:
        """Authenticate M2M client and issue token."""
        
        # Verify client registration
        if client_id not in self.registered_clients:
            self._audit_log("AUTH_FAILED", {"client_id": client_id, "reason": "unknown_client"})
            logger.warning(f"Authentication failed: unknown client {client_id}")
            return False, None
        
        credentials = self.registered_clients[client_id]
        
        # Verify secret
        if not hmac.compare_digest(credentials.client_secret, client_secret):
            self._audit_log("AUTH_FAILED", {"client_id": client_id, "reason": "invalid_secret"})
            logger.warning(f"Authentication failed: invalid secret for {client_id}")
            return False, None
        
        # Generate access token
        token = self._generate_access_token(client_id, credentials)
        
        self.issued_tokens[token.token] = token
        self._audit_log("TOKEN_ISSUED", {
            "client_id": client_id,
            "token_id": token.token[:16],
            "expires_in": token.expires_in
        })
        
        logger.info(f"Access token issued for client: {client_id}")
        return True, token

    def _generate_access_token(self, client_id: str, credentials: ClientCredentials) -> AccessToken:
        """Generate cryptographically signed access token."""
        token_id = str(uuid.uuid4())
        
        # Create token payload
        payload = {
            "jti": token_id,
            "iss": self.issuer_id,
            "sub": client_id,
            "aud": credentials.audience,
            "scope": credentials.scope,
            "isolation_level": credentials.isolation_level.value,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600
        }
        
        # Create signature
        payload_json = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            self.signing_key.encode(),
            payload_json.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Combined token format
        token_value = f"{token_id}.{signature}"
        
        return AccessToken(
            token=token_value,
            expires_in=3600,
            scope=credentials.scope,
            claims=payload
        )

    def verify_token(self, token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Verify access token validity."""
        if token not in self.issued_tokens:
            self._audit_log("TOKEN_VERIFICATION_FAILED", {"reason": "token_not_found"})
            return False, None
        
        access_token = self.issued_tokens[token]
        
        if access_token.is_expired():
            self._audit_log("TOKEN_VERIFICATION_FAILED", {"reason": "token_expired"})
            return False, None
        
        return True, access_token.claims

    def authorize_request(self, client_id: str, resource: str, action: str) -> Tuple[bool, str]:
        """Check if client is authorized for resource + action."""
        if client_id not in self.isolation_matrices:
            msg = f"Client {client_id} has no isolation matrix"
            self._audit_log("AUTHORIZATION_FAILED", {"client_id": client_id, "reason": "no_matrix"})
            return False, msg
        
        matrix = self.isolation_matrices[client_id]
        
        if not matrix.can_access(resource, action):
            msg = f"Access denied: {client_id} cannot {action} on {resource}"
            self._audit_log("AUTHORIZATION_FAILED", {
                "client_id": client_id,
                "resource": resource,
                "action": action
            })
            return False, msg
        
        self._audit_log("AUTHORIZATION_SUCCESS", {
            "client_id": client_id,
            "resource": resource,
            "action": action
        })
        return True, "Authorized"

    def grant_resource_access(self, client_id: str, resource: str) -> bool:
        """Grant client access to specific resource."""
        if client_id not in self.isolation_matrices:
            logger.warning(f"Client {client_id} has no isolation matrix")
            return False
        
        self.isolation_matrices[client_id].allowed_resources.append(resource)
        self._audit_log("RESOURCE_ACCESS_GRANTED", {"client_id": client_id, "resource": resource})
        logger.info(f"Resource access granted: {client_id} -> {resource}")
        return True

    def revoke_resource_access(self, client_id: str, resource: str) -> bool:
        """Revoke client access to specific resource."""
        if client_id not in self.isolation_matrices:
            return False
        
        matrix = self.isolation_matrices[client_id]
        if resource in matrix.allowed_resources:
            matrix.allowed_resources.remove(resource)
        matrix.denied_resources.append(resource)
        
        self._audit_log("RESOURCE_ACCESS_REVOKED", {"client_id": client_id, "resource": resource})
        logger.info(f"Resource access revoked: {client_id} -> {resource}")
        return True

    def get_isolation_matrix(self, client_id: str) -> Optional[IsolationMatrix]:
        """Retrieve client's isolation matrix."""
        return self.isolation_matrices.get(client_id)

    def _audit_log(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log security-relevant events."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gateway_id": self.gateway_id,
            "event_type": event_type,
            "details": details
        }
        self.audit_log.append(log_entry)

    def get_audit_log(self, limit: int = 100) -> list:
        """Retrieve audit log entries."""
        return self.audit_log[-limit:]

    def get_metrics(self) -> Dict[str, Any]:
        """Get gateway metrics and statistics."""
        return {
            "gateway_id": self.gateway_id,
            "registered_clients": len(self.registered_clients),
            "active_tokens": sum(1 for t in self.issued_tokens.values() if not t.is_expired()),
            "expired_tokens": sum(1 for t in self.issued_tokens.values() if t.is_expired()),
            "audit_log_entries": len(self.audit_log),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def main() -> None:
    """Demonstration of M2M OAuth Gateway."""
    logger.info("=" * 100)
    logger.info("VANE-SPACE-SLA M2M OAuth Isolation Gateway")
    logger.info("=" * 100)
    
    # Initialize gateway
    gateway = M2MOAuthGateway(issuer_id="vane-m2m-gateway")
    
    # Register clients
    logger.info("\nRegistering M2M clients...")
    client1_creds = gateway.register_client(
        client_id="client-001",
        scope="read write delete",
        audience="https://api.vane-enterprise.com",
        isolation_level=IsolationLevel.STRICT
    )
    
    client2_creds = gateway.register_client(
        client_id="client-002",
        scope="read",
        audience="https://api.vane-enterprise.com",
        isolation_level=IsolationLevel.MODERATE
    )
    
    # Grant resource access
    logger.info("\nGranting resource access...")
    gateway.grant_resource_access("client-001", "/api/telemetry/sensors")
    gateway.grant_resource_access("client-001", "/api/config/voice-agents")
    gateway.grant_resource_access("client-002", "/api/telemetry/sensors")
    
    # Authenticate clients
    logger.info("\nAuthenticating clients...")
    success, token1 = gateway.authenticate_client(
        client_id="client-001",
        client_secret=client1_creds.client_secret,
        method=AuthenticationMethod.CLIENT_CREDENTIALS
    )
    
    if success and token1:
        logger.info(f"Client 001 authenticated. Token: {token1.token[:32]}...")
        logger.info(f"Token expires at: {token1.expires_at}")
    
    success, token2 = gateway.authenticate_client(
        client_id="client-002",
        client_secret=client2_creds.client_secret
    )
    
    if success and token2:
        logger.info(f"Client 002 authenticated. Token: {token2.token[:32]}...")
    
    # Test authorization
    logger.info("\nTesting authorization...")
    auth_ok, msg = gateway.authorize_request("client-001", "/api/telemetry/sensors", "read")
    logger.info(f"Client 001 read /api/telemetry/sensors: {msg}")
    
    auth_ok, msg = gateway.authorize_request("client-002", "/api/config/voice-agents", "write")
    logger.info(f"Client 002 write /api/config/voice-agents: {msg}")
    
    # Get metrics
    logger.info("\n" + "=" * 100)
    logger.info("GATEWAY METRICS")
    logger.info("=" * 100)
    metrics = gateway.get_metrics()
    logger.info(json.dumps(metrics, indent=2))
    
    # Show audit log
    logger.info("\n" + "=" * 100)
    logger.info("AUDIT LOG (last 10 entries)")
    logger.info("=" * 100)
    for entry in gateway.get_audit_log(10):
        logger.info(f"{entry['timestamp']} | {entry['event_type']}: {entry['details']}")


if __name__ == "__main__":
    main()
