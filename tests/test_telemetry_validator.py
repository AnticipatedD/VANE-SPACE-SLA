import pytest
from telemetry_validator import AnomalyDetector, MultiGateTelemetryValidator

def test_anomaly_detector_statistical_bounds():
    """Asserts mathematical standard deviation boundary evaluation states logic paths."""
    detector = AnomalyDetector(window_size=5)
    
    # Load identical statistical baseline elements
    for _ in range(4):
        detector.add_value(10.0)
        
    # Standard values should sit inside tolerance distributions cleanly
    assert detector.add_value(10.1) is False
    
    # Massive parameter variations must yield positive anomaly execution assertions
    assert detector.add_value(50.0) is True

def test_multi_gate_validator_confidence_routing():
    """Asserts validator blocks isolate low confidence values cleanly."""
    validator = MultiGateTelemetryValidator(tolerance=0.90)
    
    healthy_frame = {"metric_value": 12.5, "confidence_score": 0.98}
    unhealthy_frame = {"metric_value": 12.5, "confidence_score": 0.85}
    
    assert validator.process_telemetry_frame(healthy_frame) is True
    assert validator.process_telemetry_frame(unhealthy_frame) is False
