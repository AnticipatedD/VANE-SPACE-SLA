#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Multi-Gate Telemetry Validation Engine (Enhanced)
Deterministic Zero-Trust Anomaly Detection System
Author: MD ABUL HOSSAIN
"""

import math
from typing import Any, Dict, List

import structlog

logger = structlog.get_logger()


class AnomalyDetector:
    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self.history: List[float] = []

    def add_value(self, value: float) -> bool:
        """Compare each sample with prior history so anomalies cannot mask themselves."""
        if not math.isfinite(value):
            raise ValueError("Telemetry metric input must be a valid real number.")

        if len(self.history) < 3:
            self.history.append(value)
            if len(self.history) > self.window_size:
                self.history.pop(0)
            return False

        mean = sum(self.history) / len(self.history)
        variance = sum((sample - mean) ** 2 for sample in self.history) / len(self.history)
        std_dev = math.sqrt(variance)

        # Keep a 1% relative noise floor for stable/near-constant sensor baselines.
        threshold = max(3 * std_dev, abs(mean) * 0.01, 1e-9)
        is_anomalous = abs(value - mean) > threshold

        self.history.append(value)
        if len(self.history) > self.window_size:
            self.history.pop(0)

        return is_anomalous


class MultiGateTelemetryValidator:
    def __init__(self, tolerance: float = 0.95) -> None:
        self.tolerance = tolerance
        self.detector = AnomalyDetector()

    def process_telemetry_frame(self, frame: Dict[str, Any]) -> bool:
        """Processes verification structures without simulation heuristics."""
        metric = frame.get("metric_value", 0.0)
        confidence = frame.get("confidence_score", 1.0)

        if confidence < self.tolerance:
            logger.warn("Telemetry rejected due to low confidence metrics", score=confidence)
            return False

        is_anomalous = self.detector.add_value(metric)
        if is_anomalous:
            logger.error("Structural anomaly registered inside telemetry frame", value=metric)
            return False

        return True
