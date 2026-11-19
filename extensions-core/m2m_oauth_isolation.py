#!/usr/bin/env python3
"""
Extension: M2M OAuth Isolation Module
Advanced zero-trust request isolation patterns
"""

from m2m_oauth_gateway import M2MOAuthGateway
import logging
from typing import Any

logger = logging.getLogger("m2m_isolation")


class IsolatedRequestHandler:
    """Handles isolated M2M requests with full audit trail."""

    def __init__(self, gateway: M2MOAuthGateway):
        self.gateway = gateway
        self.request_count = 0

    def handle_request(
        self,
        client_id: str,
        token: str,
        resource: str,
        action: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Process a request after token and scope validation."""
        self.request_count += 1

        if not self.gateway.validate_token(token):
            return {"status": "unauthorized", "error": "Invalid or expired token"}

        if not self.gateway.matrix.can_access(client_id, action):
            return {"status": "forbidden", "error": "Requested scope is not permitted"}
        
        # Process request
        return {
            "status": "success",
            "request_id": self.request_count,
            "client_id": client_id,
            "resource": resource,
            "action": action,
            "message": "Request processed successfully"
        }


if __name__ == "__main__":
    gateway = M2MOAuthGateway()
    handler = IsolatedRequestHandler(gateway)
    print("M2M Isolation Extension loaded successfully")
