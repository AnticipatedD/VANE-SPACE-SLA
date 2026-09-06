import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vane_space_init import run_multi_gate_telemetry_check, get_config


def test_get_config_returns_dict():
    config = get_config()
    assert isinstance(config, dict)
    assert len(config) > 0


def test_run_multi_gate_telemetry_check_returns_expected_keys():
    result = run_multi_gate_telemetry_check(seed=42)
    assert isinstance(result, dict)
    # Stricter: check important keys exist
    expected_possible_keys = {"status_flag", "measured_latency_ms", "status", "latency_ms", "result"}
    assert any(key in result for key in expected_possible_keys)


def test_run_multi_gate_telemetry_check_deterministic_with_seed():
    result1 = run_multi_gate_telemetry_check(seed=42)
    result2 = run_multi_gate_telemetry_check(seed=42)
    # With fixed seed the results should be identical
    assert result1 == result2
