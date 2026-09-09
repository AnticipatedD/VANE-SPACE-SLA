#!/usr/bin/env python3
"""
Test Suite for VANE-SPACE-SLA - Voice Agents Module
Author: MD ABUL HOSSAIN
"""

import pytest
import os
import json
from unittest.mock import patch, MagicMock, call
from voice_agents import (
    VoiceAgent,
    VoiceOrchestrator,
    SpeechProcessor,
    AgentState,
    convert_state_to_string
)


class TestAgentState:
    """Test AgentState enumeration."""

    def test_agent_state_values(self):
        """Test AgentState enum has expected values."""
        assert hasattr(AgentState, "IDLE")
        assert hasattr(AgentState, "LISTENING")
        assert hasattr(AgentState, "PROCESSING")
        assert hasattr(AgentState, "RESPONDING")
        assert hasattr(AgentState, "ERROR")

    def test_convert_state_to_string(self):
        """Test state to string conversion."""
        assert convert_state_to_string(AgentState.IDLE) == "IDLE"
        assert convert_state_to_string(AgentState.LISTENING) == "LISTENING"
        assert convert_state_to_string(AgentState.PROCESSING) == "PROCESSING"
        assert convert_state_to_string(AgentState.RESPONDING) == "RESPONDING"
        assert convert_state_to_string(AgentState.ERROR) == "ERROR"


class TestVoiceAgent:
    """Test individual VoiceAgent functionality."""

    def test_voice_agent_init(self):
        """Test VoiceAgent initialization."""
        agent = VoiceAgent(
            agent_id="voice-agent-001",
            name="Primary Assistant",
            model="watsonx-voice-v2"
        )
        
        assert agent.agent_id == "voice-agent-001"
        assert agent.name == "Primary Assistant"
        assert agent.model == "watsonx-voice-v2"
        assert agent.state == AgentState.IDLE

    def test_voice_agent_set_state(self):
        """Test changing agent state."""
        agent = VoiceAgent(agent_id="voice-agent-001", name="Test Agent")
        
        agent.set_state(AgentState.LISTENING)
        assert agent.state == AgentState.LISTENING
        
        agent.set_state(AgentState.PROCESSING)
        assert agent.state == AgentState.PROCESSING

    def test_voice_agent_process_voice_input(self):
        """Test processing voice input."""
        agent = VoiceAgent(agent_id="voice-agent-001", name="Test Agent")
        
        result = agent.process_voice_input("What is the weather?")
        
        assert isinstance(result, dict)
        assert "transcription" in result
        assert "confidence" in result
        assert "timestamp" in result

    def test_voice_agent_generate_response(self):
        """Test generating voice response."""
        agent = VoiceAgent(agent_id="voice-agent-001", name="Test Agent")
        
        response = agent.generate_response("What is the weather?")
        
        assert isinstance(response, dict)
        assert "text" in response
        assert "audio_url" in response
        assert "duration_ms" in response

    def test_voice_agent_error_handling(self):
        """Test agent error handling."""
        agent = VoiceAgent(agent_id="voice-agent-001", name="Test Agent")
        
        agent.set_state(AgentState.ERROR)
        assert agent.state == AgentState.ERROR
        
        error_info = agent.get_error_info()
        assert isinstance(error_info, dict)

    def test_voice_agent_reset(self):
        """Test agent reset functionality."""
        agent = VoiceAgent(agent_id="voice-agent-001", name="Test Agent")
        
        agent.set_state(AgentState.PROCESSING)
        agent.reset()
        
        assert agent.state == AgentState.IDLE
        assert len(agent.conversation_history) == 0


class TestSpeechProcessor:
    """Test SpeechProcessor functionality."""

    def test_speech_processor_init(self):
        """Test SpeechProcessor initialization."""
        processor = SpeechProcessor(
            language="en-US",
            sample_rate=16000
        )
        
        assert processor.language == "en-US"
        assert processor.sample_rate == 16000

    def test_speech_to_text_conversion(self):
        """Test speech-to-text conversion."""
        processor = SpeechProcessor(language="en-US")
        
        # Simulate audio buffer
        result = processor.convert_speech_to_text(audio_buffer=b"simulated_audio")
        
        assert isinstance(result, dict)
        assert "text" in result
        assert "confidence" in result

    def test_text_to_speech_conversion(self):
        """Test text-to-speech conversion."""
        processor = SpeechProcessor(language="en-US")
        
        result = processor.convert_text_to_speech("Hello, world!")
        
        assert isinstance(result, dict)
        assert "audio_url" in result
        assert "duration_ms" in result

    def test_speech_processor_language_support(self):
        """Test language support."""
        supported_languages = ["en-US", "fr-FR", "de-DE", "es-ES"]
        
        for lang in supported_languages:
            processor = SpeechProcessor(language=lang)
            assert processor.language == lang

    def test_speech_processor_noise_filtering(self):
        """Test noise filtering capability."""
        processor = SpeechProcessor(language="en-US", enable_noise_filter=True)
        
        result = processor.apply_noise_filter(audio_buffer=b"noisy_audio")
        
        assert isinstance(result, dict)
        assert "filtered_audio" in result
        assert "noise_reduction_db" in result


class TestVoiceOrchestrator:
    """Test VoiceOrchestrator functionality."""

    def test_voice_orchestrator_init(self):
        """Test VoiceOrchestrator initialization."""
        orchestrator = VoiceOrchestrator(
            orchestrator_id="orch-001",
            max_concurrent_agents=4
        )
        
        assert orchestrator.orchestrator_id == "orch-001"
        assert orchestrator.max_concurrent_agents == 4
        assert len(orchestrator.agents) == 0

    def test_voice_orchestrator_register_agent(self):
        """Test registering agents with orchestrator."""
        orchestrator = VoiceOrchestrator(orchestrator_id="orch-001")
        
        agent1 = VoiceAgent(agent_id="agent-001", name="Agent 1")
        agent2 = VoiceAgent(agent_id="agent-002", name="Agent 2")
        
        orchestrator.register_agent(agent1)
        orchestrator.register_agent(agent2)
        
        assert len(orchestrator.agents) == 2
        assert orchestrator.get_agent("agent-001") == agent1
        assert orchestrator.get_agent("agent-002") == agent2

    def test_voice_orchestrator_route_request(self):
        """Test routing voice request to appropriate agent."""
        orchestrator = VoiceOrchestrator(orchestrator_id="orch-001")
        
        agent = VoiceAgent(agent_id="agent-001", name="Test Agent")
        orchestrator.register_agent(agent)
        
        result = orchestrator.route_voice_request(
            query="What time is it?",
            priority="normal"
        )
        
        assert isinstance(result, dict)
        assert "agent_id" in result
        assert "response" in result

    def test_voice_orchestrator_concurrent_handling(self):
        """Test handling concurrent voice requests."""
        orchestrator = VoiceOrchestrator(
            orchestrator_id="orch-001",
            max_concurrent_agents=2
        )
        
        for i in range(2):
            agent = VoiceAgent(agent_id=f"agent-{i:03d}", name=f"Agent {i}")
            orchestrator.register_agent(agent)
        
        requests = [
            "What is the weather?",
            "What time is it?"
        ]
        
        results = orchestrator.handle_concurrent_requests(requests)
        
        assert len(results) == 2
        assert all("response" in r for r in results)

    def test_voice_orchestrator_load_balancing(self):
        """Test load balancing across agents."""
        orchestrator = VoiceOrchestrator(orchestrator_id="orch-001")
        
        # Register multiple agents
        for i in range(3):
            agent = VoiceAgent(agent_id=f"agent-{i:03d}", name=f"Agent {i}")
            orchestrator.register_agent(agent)
        
        # Send multiple requests
        for _ in range(10):
            orchestrator.route_voice_request("Test query")
        
        # Verify load is distributed
        loads = [agent.get_current_load() for agent in orchestrator.agents]
        assert max(loads) - min(loads) <= 2  # Load should be balanced

    def test_voice_orchestrator_failover(self):
        """Test failover when agent fails."""
        orchestrator = VoiceOrchestrator(orchestrator_id="orch-001")
        
        agent1 = VoiceAgent(agent_id="agent-001", name="Agent 1")
        agent2 = VoiceAgent(agent_id="agent-002", name="Agent 2")
        
        orchestrator.register_agent(agent1)
        orchestrator.register_agent(agent2)
        
        # Simulate agent1 failure
        agent1.set_state(AgentState.ERROR)
        
        # Request should be routed to agent2
        result = orchestrator.route_voice_request("Test query")
        
        assert result["agent_id"] == "agent-002"

    def test_voice_orchestrator_metrics(self):
        """Test orchestrator metrics collection."""
        orchestrator = VoiceOrchestrator(orchestrator_id="orch-001")
        
        agent = VoiceAgent(agent_id="agent-001", name="Agent 1")
        orchestrator.register_agent(agent)
        
        # Process some requests
        for _ in range(5):
            orchestrator.route_voice_request("Test query")
        
        metrics = orchestrator.get_metrics()
        
        assert isinstance(metrics, dict)
        assert "total_requests" in metrics
        assert "average_response_time_ms" in metrics
        assert "success_rate" in metrics


class TestIntegration:
    """Integration tests for voice components."""

    def test_end_to_end_voice_processing(self):
        """Test end-to-end voice processing workflow."""
        orchestrator = VoiceOrchestrator(orchestrator_id="orch-001")
        
        # Register agents
        for i in range(2):
            agent = VoiceAgent(
                agent_id=f"agent-{i:03d}",
                name=f"Agent {i}",
                model="watsonx-voice-v2"
            )
            orchestrator.register_agent(agent)
        
        # Process voice request
        result = orchestrator.route_voice_request(
            query="Hello, how can you help me?",
            priority="normal"
        )
        
        assert result["agent_id"]
        assert result["response"]
        assert result["status"] == "success"

    def test_multi_language_support(self):
        """Test multi-language voice processing."""
        orchestrator = VoiceOrchestrator(orchestrator_id="orch-001")
        
        languages = ["en-US", "fr-FR", "de-DE"]
        
        for i, lang in enumerate(languages):
            agent = VoiceAgent(
                agent_id=f"agent-{i:03d}",
                name=f"Agent {lang}",
                language=lang
            )
            orchestrator.register_agent(agent)
        
        # Process request in each language
        for lang in languages:
            result = orchestrator.route_voice_request(
                query="Test query",
                language=lang
            )
            assert result["language"] == lang


if __name__ == "__main__":
    pytest.main(["-v", __file__, "--cov=voice_agents", "--cov-report=term-missing"])
