import random
from vane_space_init import run_multi_gate_telemetry_check, verify_granite_syntax_gate

def test_syntax_gate_fail():
    result = verify_granite_syntax_gate("average = (num1 + num2 + num3 / 3")
    assert result["validation_gate"] == "FAIL"

def test_syntax_gate_pass():
    result = verify_granite_syntax_gate("average = (num1 + num2 + num3) / 3")
    assert result["validation_gate"] == "PASS"

def test_telemetry_check_keys():
    random.seed(42)
    report = run_multi_gate_telemetry_check({"stream_id": "TEST"}, seed=42)
    assert "operational_status" in report
    assert "measured_latency_ms" in report
    assert "verifiable_confidence_score" in report
    assert report["operational_status"] in ["VERIFIED_TRUTH_BOUND", "STOCHASTIC_DRIFT_INTERCEPTED"]
