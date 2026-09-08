#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Main Entry Point
Author: MD ABUL HOSSAIN
Description: Orchestrates multi-gate telemetry validation demonstration
"""

import os
from dotenv import load_dotenv
from vane_space.logging_config import configure_logging
from vane_space.telemetry import (
    verify_granite_syntax_gate,
    run_multi_gate_telemetry_check
)
from vane_space.errors import ConfigError, TelemetryValidationError

load_dotenv()
logger = configure_logging("vane_space_init")


def validate_env() -> None:
    """
    Validate that required environment variables are set.
    
    Raises:
        ConfigError: If required env vars are missing or empty
    """
    required = [
        "IBM_SAAS_ACCOUNT_ID",
        "EU_EXPERT_ID",
        "VANE_ACCOUNT_ID",
    ]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise ConfigError(
            f"Missing or empty required environment variables: {', '.join(missing)}"
        )
    logger.info(f"✓ Environment validation passed ({len(required)} required vars found)")


def get_config() -> dict:
    """
    Retrieve application configuration from environment.
    
    Returns:
        Dictionary with configuration values
    """
    return {
        "node_id": "VANE_SECURE_NODE",
        "framework": "Vane-Space-SLA (V1.0)",
        "saas_account_id": os.getenv("IBM_SAAS_ACCOUNT_ID", "myibm-account"),
        "eu_expert_id": os.getenv("EU_EXPERT_ID", "MYEUEXPERTID"),
        "reseller_lic": os.getenv("CONTRACT_RESELLER_ID", "myibm-reseller"),
        "service_bpa": os.getenv("CONTRACT_SERVICE_BPA", "myibm-bpa"),
        "customer_index": os.getenv("CUSTOMER_INDEX", "myibm-customer"),
        "eu_cellar_id": os.getenv("EU_CELLAR_DOC_ID", "myibm-cellar"),
    }


def main() -> None:
    """
    Main entry point for VANE-SPACE-SLA demonstration.
    Executes multi-gate telemetry validation pipeline.
    """
    try:
        # Validate environment configuration
        validate_env()
        config = get_config()

        logger.info(f"Initializing: {config['framework']}")
        logger.info(f"EU Expert ID: {config['eu_expert_id']}")
        logger.info(f"Node ID: {config['node_id']}")

        # Syntax validation gate
        faulty_code = "average = (num1 + num2 + num3 / 3"
        syntax_audit = verify_granite_syntax_gate(faulty_code)
        logger.info(f"Syntax gate: {syntax_audit['validation_gate']}")
        if syntax_audit['validation_gate'] == "FAIL":
            logger.warning(f"Error detected: {syntax_audit['error_detected']}")
            logger.info(f"Remediation: {syntax_audit['granite_remediation']}")

        # Multi-gate telemetry validation
        logger.info("\n" + "="*60)
        logger.info("Starting Multi-Gate Telemetry Validation Pipeline")
        logger.info("="*60 + "\n")

        for i in range(1, 4):
            try:
                payload = {
                    "stream_id": f"SAT-SEC03-{i:03d}",
                    "solar_current_amps": None  # Placeholder
                }
                report = run_multi_gate_telemetry_check(payload)
                logger.info(f"✓ Transaction {i:03d} → {report['operational_status']}")
                logger.info(f"  Latency: {report['measured_latency_ms']}ms")
                logger.info(f"  Confidence: {report['verifiable_confidence_score']}")

            except TelemetryValidationError as e:
                logger.warning(f"✗ Transaction {i:03d} flagged: {str(e)}")
                continue

        logger.info("\n" + "="*60)
        logger.info("Multi-Gate Telemetry Validation Complete")
        logger.info("="*60)

    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
