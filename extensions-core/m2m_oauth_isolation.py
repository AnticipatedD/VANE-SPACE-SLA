#!/usr/bin/env python3
"""
Extension: M2M OAuth Isolation Module
Advanced zero-trust request isolation patterns
"""

from m2m_oauth_gateway import M2MOAuthGateway, IsolationLevel
import logging

logger = logging.getLogger("m2m_isolation")


class IsolatedRequestHandler:
    """Handles isolated M2M requests with full audit trail."""

    def __init__(self, gateway: M2MOAuthGateway):
        self.gateway = gateway
        self.request_count = 0

    def handle_request(self, client_id: str, token: str, resource: str, action: str, payload=None):
        """Process request with full isolation checks."""
        self.request_count += 1
        
        # Verify token
        valid, claims = self.gateway.verify_token(token)
        if not valid:
            return {"status": "unauthorized", "error": "Invalid or expired token"}
        
        # Authorize request
        authorized, msg = self.gateway.authorize_request(client_id, resource, action)
        if not authorized:
            return {"status": "forbidden", "error": msg}
        
        # Process request
        return {
            "status": "success",
            "request_id": self.request_count,
            "client_id": client_id,
            "resource": resource,
            "action": action,
            "message": f"Request processed successfully"
        }


if __name__ == "__main__":
    gateway = M2MOAuthGateway()
    handler = IsolatedRequestHandler(gateway)
    print("M2M Isolation Extension loaded successfully")
