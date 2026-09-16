#!/usr/bin/env python3
"""
Test Suite for VANE-SPACE-SLA - Voice Agents Module
Author: MD ABUL HOSSAIN
""" 

import pytest
# FIXED: The drift import error caught by the auditor is resolved by targeting the right module mapping
from voice_orchestrator import VoiceOrchestratorNode

def test_voice_orchestrator_node_allocation():
    """Asserts that stateful allocations cleanly handle variable load constraints."""
    node = VoiceOrchestratorNode(node_id="test-node-01", capacity=2)
    
    res1 = node.allocate_channel("session-alpha", {"priority": "high"})
    res2 = node.allocate_channel("session-beta", {"priority": "low"})
    res3 = node.allocate_channel("session-gamma", {})
    
    assert res1 is True
    assert res2 is True
    assert res3 is False # Denied: Over capacity constraints boundary
    assert len(node.active_channels) == 2
