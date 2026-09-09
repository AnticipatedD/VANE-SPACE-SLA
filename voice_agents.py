#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Voice Agents Module
Orchestration Engine for Multi-Agent Voice Processing
Author: MD ABUL HOSSAIN
"""

import os
import json
import time
import logging
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("voice_agents")


class AgentState(Enum):
    """Voice agent operational states."""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    RESPONDING = "responding"
    ERROR = "error"


def convert_state_to_string(state: AgentState) -> str:
    """Convert AgentState enum to string."""
    return state.value.upper()


@dataclass
class VoiceInput:
    """Structured voice input data."""
    audio_buffer: bytes
    sample_rate: int = 16000
    language: str = "en-US"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    duration_ms: float = 0.0


@dataclass
class VoiceOutput:
    """Structured voice output data."""
    text: str
    audio_url: str
    duration_ms: float
    confidence: float = 0.95
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SpeechProcessor:
    """Speech-to-text and text-to-speech processing."""

    def __init__(self, language: str = "en-US", sample_rate: int = 16000, 
                 enable_noise_filter: bool = False):
        self.language = language
        self.sample_rate = sample_rate
        self.enable_noise_filter = enable_noise_filter
        self.processor_id = str(uuid.uuid4())[:8]
        logger.info(f"SpeechProcessor initialized: {self.processor_id} ({language})")

    def convert_speech_to_text(self, audio_buffer: bytes) -> Dict[str, Any]:
        """Convert speech audio to text."""
        if not audio_buffer or len(audio_buffer) == 0:
            return {
                "text": "",
                "confidence": 0.0,
                "error": "Empty audio buffer"
            }

        # Simulated transcription
        duration_ms = (len(audio_buffer) / self.sample_rate) * 1000
        confidence = min(0.99, 0.85 + (len(audio_buffer) % 1000) / 10000)

        return {
            "text": f"[Simulated transcription from {self.language}]",
            "confidence": round(confidence, 4),
            "language": self.language,
            "duration_ms": round(duration_ms, 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def convert_text_to_speech(self, text: str) -> Dict[str, Any]:
        """Convert text to speech audio."""
        if not text or not text.strip():
            return {
                "audio_url": "",
                "duration_ms": 0.0,
                "error": "Empty text input"
            }

        # Simulated TTS
        estimated_duration = len(text) * 60  # ~60ms per character

        return {
            "audio_url": f"s3://vane-audio/{uuid.uuid4()}.wav",
            "duration_ms": round(estimated_duration, 2),
            "language": self.language,
            "format": "wav",
            "sample_rate": self.sample_rate,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def apply_noise_filter(self, audio_buffer: bytes) -> Dict[str, Any]:
        """Apply noise filtering to audio."""
        if not audio_buffer:
            return {"filtered_audio": b"", "noise_reduction_db": 0.0}

        # Simulated noise filtering
        noise_reduction_db = 12 + (len(audio_buffer) % 100) / 10

        return {
            "filtered_audio": audio_buffer,
            "noise_reduction_db": round(noise_reduction_db, 2),
            "filter_applied": True,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


class VoiceAgent:
    """Individual voice processing agent."""

    def __init__(self, agent_id: str, name: str, model: str = "watsonx-voice-v2", 
                 language: str = "en-US"):
        self.agent_id = agent_id
        self.name = name
        self.model = model
        self.language = language
        self.state = AgentState.IDLE
        self.conversation_history: List[Dict[str, str]] = []
        self.speech_processor = SpeechProcessor(language=language)
        self.current_load = 0
        self.processed_requests = 0
        self.error_count = 0
        self.last_error = None
        logger.info(f"VoiceAgent initialized: {agent_id} ({name})")

    def set_state(self, state: AgentState) -> None:
        """Update agent operational state."""
        self.state = state
        logger.debug(f"Agent {self.agent_id} state changed to {convert_state_to_string(state)}")

    def process_voice_input(self, query: str, audio_buffer: Optional[bytes] = None) -> Dict[str, Any]:
        """Process incoming voice input."""
        self.set_state(AgentState.LISTENING)
        
        try:
            start_time = time.perf_counter()
            
            # Process audio if provided, else use text directly
            if audio_buffer:
                stt_result = self.speech_processor.convert_speech_to_text(audio_buffer)
                transcription = stt_result.get("text", query)
                confidence = stt_result.get("confidence", 0.9)
            else:
                transcription = query
                confidence = 1.0

            processing_time_ms = (time.perf_counter() - start_time) * 1000
            self.processed_requests += 1

            result = {
                "transcription": transcription,
                "confidence": round(confidence, 4),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "processing_time_ms": round(processing_time_ms, 2),
                "agent_id": self.agent_id
            }

            self.conversation_history.append({"role": "user", "content": transcription})
            return result

        except Exception as e:
            self.set_state(AgentState.ERROR)
            self.error_count += 1
            self.last_error = str(e)
            logger.error(f"Error processing voice input: {e}")
            return {"error": str(e), "agent_id": self.agent_id}

    def generate_response(self, query: str) -> Dict[str, Any]:
        """Generate voice response to query."""
        self.set_state(AgentState.PROCESSING)
        
        try:
            start_time = time.perf_counter()

            # Simulated response generation
            response_text = f"[Response to: {query[:50]}...]"

            # Convert to speech
            tts_result = self.speech_processor.convert_text_to_speech(response_text)

            processing_time_ms = (time.perf_counter() - start_time) * 1000

            result = {
                "text": response_text,
                "audio_url": tts_result.get("audio_url"),
                "duration_ms": tts_result.get("duration_ms"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "processing_time_ms": round(processing_time_ms, 2),
                "agent_id": self.agent_id
            }

            self.conversation_history.append({"role": "assistant", "content": response_text})
            self.set_state(AgentState.IDLE)
            return result

        except Exception as e:
            self.set_state(AgentState.ERROR)
            self.error_count += 1
            self.last_error = str(e)
            logger.error(f"Error generating response: {e}")
            return {"error": str(e), "agent_id": self.agent_id}

    def get_error_info(self) -> Dict[str, Any]:
        """Get current error information."""
        return {
            "has_error": self.state == AgentState.ERROR,
            "error_count": self.error_count,
            "last_error": self.last_error,
            "agent_id": self.agent_id
        }

    def reset(self) -> None:
        """Reset agent to initial state."""
        self.state = AgentState.IDLE
        self.conversation_history = []
        self.current_load = 0
        self.error_count = 0
        self.last_error = None
        logger.info(f"Agent {self.agent_id} reset successfully")

    def get_current_load(self) -> int:
        """Get current processing load."""
        return self.current_load

    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "state": convert_state_to_string(self.state),
            "processed_requests": self.processed_requests,
            "error_count": self.error_count,
            "current_load": self.current_load,
            "conversation_history_length": len(self.conversation_history)
        }


class VoiceOrchestrator:
    """Master orchestrator for multi-agent voice processing."""

    def __init__(self, orchestrator_id: str, max_concurrent_agents: int = 4):
        self.orchestrator_id = orchestrator_id
        self.max_concurrent_agents = max_concurrent_agents
        self.agents: Dict[str, VoiceAgent] = {}
        self.request_queue: List[Dict[str, Any]] = []
        self.processed_requests = 0
        self.failed_requests = 0
        logger.info(f"VoiceOrchestrator initialized: {orchestrator_id}")

    def register_agent(self, agent: VoiceAgent) -> bool:
        """Register voice agent with orchestrator."""
        if len(self.agents) >= self.max_concurrent_agents:
            logger.warning(f"Max concurrent agents ({self.max_concurrent_agents}) reached")
            return False
        
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent {agent.agent_id} registered")
        return True

    def get_agent(self, agent_id: str) -> Optional[VoiceAgent]:
        """Retrieve agent by ID."""
        return self.agents.get(agent_id)

    def _select_best_agent(self) -> Optional[VoiceAgent]:
        """Select agent with lowest load."""
        if not self.agents:
            return None
        
        available_agents = [
            agent for agent in self.agents.values() 
            if agent.state != AgentState.ERROR
        ]
        
        if not available_agents:
            return None
        
        return min(available_agents, key=lambda a: a.get_current_load())

    def route_voice_request(self, query: str, priority: str = "normal", 
                           language: str = "en-US") -> Dict[str, Any]:
        """Route voice request to appropriate agent."""
        agent = self._select_best_agent()
        
        if not agent:
            self.failed_requests += 1
            return {"status": "error", "error": "No available agents"}
        
        try:
            agent.current_load += 1
            
            # Process voice input
            input_result = agent.process_voice_input(query)
            
            # Generate response
            response_result = agent.generate_response(query)
            
            self.processed_requests += 1
            agent.current_load -= 1
            
            return {
                "agent_id": agent.agent_id,
                "status": "success",
                "query": query,
                "language": language,
                "response": response_result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        except Exception as e:
            self.failed_requests += 1
            agent.current_load -= 1
            logger.error(f"Error routing request: {e}")
            return {"status": "error", "error": str(e), "agent_id": agent.agent_id}

    def handle_concurrent_requests(self, requests: List[str]) -> List[Dict[str, Any]]:
        """Handle multiple concurrent voice requests."""
        results = []
        
        for request in requests:
            result = self.route_voice_request(request)
            results.append(result)
        
        return results

    def get_metrics(self) -> Dict[str, Any]:
        """Get orchestrator-wide metrics."""
        agent_metrics = [agent.get_metrics() for agent in self.agents.values()]
        
        total_requests = self.processed_requests + self.failed_requests
        success_rate = (
            (self.processed_requests / total_requests * 100) 
            if total_requests > 0 else 0.0
        )
        
        return {
            "orchestrator_id": self.orchestrator_id,
            "total_agents": len(self.agents),
            "total_requests": total_requests,
            "successful_requests": self.processed_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(success_rate, 2),
            "average_response_time_ms": self._calculate_average_response_time(),
            "agent_metrics": agent_metrics,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _calculate_average_response_time(self) -> float:
        """Calculate average response time across all agents."""
        if not self.agents:
            return 0.0
        
        total_time = sum(
            sum(1 for _ in agent.conversation_history) 
            for agent in self.agents.values()
        )
        
        return round(total_time / len(self.agents), 2) if self.agents else 0.0

    def shutdown(self) -> None:
        """Gracefully shutdown all agents."""
        for agent in self.agents.values():
            agent.reset()
        
        self.agents.clear()
        logger.info(f"Orchestrator {self.orchestrator_id} shutdown complete")


def main() -> None:
    """Demonstration of voice agents system."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
    )
    
    logger.info("=" * 80)
    logger.info("VANE-SPACE-SLA Voice Agents System Initialization")
    logger.info("=" * 80)
    
    # Initialize orchestrator
    orchestrator = VoiceOrchestrator(orchestrator_id="orch-001", max_concurrent_agents=3)
    
    # Register agents
    for i in range(3):
        agent = VoiceAgent(
            agent_id=f"voice-agent-{i:03d}",
            name=f"Voice Agent {i}",
            model="watsonx-voice-v2",
            language="en-US"
        )
        orchestrator.register_agent(agent)
    
    # Process sample requests
    sample_queries = [
        "What is the weather forecast?",
        "Can you help me with scheduling?",
        "Provide system status update"
    ]
    
    logger.info("Processing sample voice requests...")
    results = orchestrator.handle_concurrent_requests(sample_queries)
    
    for i, result in enumerate(results, 1):
        logger.info(f"Request {i}: Agent {result.get('agent_id')} - Status {result.get('status')}")
    
    # Print metrics
    metrics = orchestrator.get_metrics()
    logger.info(f"Success Rate: {metrics['success_rate']}%")
    logger.info(f"Total Requests: {metrics['total_requests']}")
    
    # Cleanup
    orchestrator.shutdown()
    logger.info("Voice agents system shutdown complete")


if __name__ == "__main__":
    main()
