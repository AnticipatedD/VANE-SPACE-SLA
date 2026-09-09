#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Voice Orchestrator Node
Central orchestration hub for voice processing, routing, and analytics
Author: MD ABUL HOSSAIN
"""

import os
import json
import time
import logging
import uuid
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
)
logger = logging.getLogger("voice_orchestrator")


class ProcessingPriority(Enum):
    """Voice request processing priority levels."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


class NodeStatus(Enum):
    """Orchestrator node operational status."""
    ONLINE = "online"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


@dataclass
class VoiceRequest:
    """Structured voice orchestration request."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    query: str = ""
    priority: ProcessingPriority = ProcessingPriority.NORMAL
    language: str = "en-US"
    source_client: str = ""
    audio_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class VoiceResponse:
    """Structured voice orchestration response."""
    request_id: str
    status: str
    transcription: str = ""
    response_text: str = ""
    audio_url: str = ""
    processing_time_ms: float = 0.0
    confidence_score: float = 0.0
    agent_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class VoiceOrchestratorNode:
    """Central voice orchestration hub."""

    def __init__(self, node_id: str = None, region: str = "us-east-1", max_queue_size: int = 1000):
        self.node_id = node_id or f"voice-orch-{str(uuid.uuid4())[:8]}"
        self.region = region
        self.status = NodeStatus.ONLINE
        self.max_queue_size = max_queue_size
        
        # Request management
        self.request_queue: List[VoiceRequest] = []
        self.processing_history: Dict[str, VoiceResponse] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Metrics and monitoring
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_processing_time = 0.0
        
        # Connected agents
        self.connected_agents: Dict[str, Dict[str, Any]] = {}
        self.agent_health: Dict[str, bool] = {}
        
        logger.info(f"VoiceOrchestratorNode initialized: {self.node_id} (region: {region})")

    def register_agent(self, agent_id: str, agent_name: str, capabilities: List[str]) -> bool:
        """Register voice processing agent."""
        if agent_id in self.connected_agents:
            logger.warning(f"Agent {agent_id} already registered")
            return False
        
        self.connected_agents[agent_id] = {
            "name": agent_name,
            "capabilities": capabilities,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "load": 0,
            "status": "healthy"
        }
        self.agent_health[agent_id] = True
        
        logger.info(f"Agent registered: {agent_id} ({agent_name})")
        return True

    def deregister_agent(self, agent_id: str) -> bool:
        """Deregister voice processing agent."""
        if agent_id not in self.connected_agents:
            return False
        
        del self.connected_agents[agent_id]
        del self.agent_health[agent_id]
        
        logger.info(f"Agent deregistered: {agent_id}")
        return True

    def submit_voice_request(self, query: str, priority: ProcessingPriority = ProcessingPriority.NORMAL,
                            language: str = "en-US", source_client: str = "") -> VoiceRequest:
        """Submit voice request for processing."""
        if len(self.request_queue) >= self.max_queue_size:
            logger.error("Request queue full - rejecting new requests")
            return None
        
        request = VoiceRequest(
            query=query,
            priority=priority,
            language=language,
            source_client=source_client
        )
        
        # Add to queue (sorted by priority)
        self.request_queue.append(request)
        self.request_queue.sort(key=lambda r: r.priority.value)
        
        self.total_requests += 1
        logger.info(f"Voice request submitted: {request.request_id} (priority: {priority.name})")
        
        return request

    def process_voice_request(self) -> Optional[VoiceResponse]:
        """Process next voice request from queue."""
        if not self.request_queue:
            return None
        
        # Get highest priority request
        request = self.request_queue.pop(0)
        
        # Find best available agent
        best_agent = self._select_best_agent(request)
        if not best_agent:
            self.failed_requests += 1
            logger.error(f"No available agents for request {request.request_id}")
            return None
        
        # Process request
        start_time = time.perf_counter()
        
        try:
            # Simulate processing
            response = VoiceResponse(
                request_id=request.request_id,
                status="success",
                transcription=f"[Transcribed: {request.query[:50]}]",
                response_text=f"[Response to: {request.query[:50]}]",
                audio_url=f"s3://vane-audio/{request.request_id}.wav",
                confidence_score=0.92 + (hash(request.request_id) % 10) / 100,
                agent_id=best_agent[0]
            )
            
            processing_time = (time.perf_counter() - start_time) * 1000
            response.processing_time_ms = processing_time
            
            self.processing_history[request.request_id] = response
            self.successful_requests += 1
            self.total_processing_time += processing_time
            self.connected_agents[best_agent[0]]["load"] -= 1
            
            logger.info(f"Request processed: {request.request_id} by agent {best_agent[0]} in {processing_time:.2f}ms")
            return response
        
        except Exception as e:
            self.failed_requests += 1
            logger.error(f"Error processing request {request.request_id}: {e}")
            return None

    def _select_best_agent(self, request: VoiceRequest) -> Optional[tuple]:
        """Select best agent for request based on load and capabilities."""
        available_agents = []
        
        for agent_id, agent_info in self.connected_agents.items():
            if self.agent_health.get(agent_id, False) and agent_info["status"] == "healthy":
                available_agents.append((agent_id, agent_info))
        
        if not available_agents:
            return None
        
        # Select agent with lowest load
        best_agent = min(available_agents, key=lambda a: a[1]["load"])
        best_agent[1]["load"] += 1
        
        return best_agent

    def get_agent_health(self) -> Dict[str, Any]:
        """Get health status of all agents."""
        health_status = {}
        
        for agent_id, agent_info in self.connected_agents.items():
            health_status[agent_id] = {
                "name": agent_info["name"],
                "status": agent_info["status"],
                "load": agent_info["load"],
                "healthy": self.agent_health.get(agent_id, False)
            }
        
        return health_status

    def set_node_status(self, status: NodeStatus) -> None:
        """Update orchestrator node status."""
        self.status = status
        logger.info(f"Node status updated: {status.value}")

    def process_batch_requests(self, requests: List[Dict[str, Any]]) -> List[VoiceResponse]:
        """Process multiple voice requests in batch."""
        responses = []
        
        for req_data in requests:
            request = self.submit_voice_request(
                query=req_data.get("query", ""),
                priority=ProcessingPriority(req_data.get("priority", 3)),
                language=req_data.get("language", "en-US"),
                source_client=req_data.get("source_client", "")
            )
            
            if request:
                response = self.process_voice_request()
                if response:
                    responses.append(response)
        
        return responses

    def get_metrics(self) -> Dict[str, Any]:
        """Get orchestrator metrics and statistics."""
        avg_processing_time = (
            self.total_processing_time / self.successful_requests
            if self.successful_requests > 0 else 0.0
        )
        
        success_rate = (
            self.successful_requests / self.total_requests * 100
            if self.total_requests > 0 else 0.0
        )
        
        return {
            "node_id": self.node_id,
            "region": self.region,
            "status": self.status.value,
            "connected_agents": len(self.connected_agents),
            "healthy_agents": sum(1 for h in self.agent_health.values() if h),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(success_rate, 2),
            "average_processing_time_ms": round(avg_processing_time, 2),
            "current_queue_size": len(self.request_queue),
            "processing_history_size": len(self.processing_history),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_request_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get request processing history."""
        history = []
        
        for req_id, response in list(self.processing_history.items())[-limit:]:
            history.append(asdict(response))
        
        return history

    def shutdown(self) -> None:
        """Gracefully shutdown orchestrator node."""
        logger.info(f"Shutting down VoiceOrchestratorNode: {self.node_id}")
        self.set_node_status(NodeStatus.OFFLINE)
        self.connected_agents.clear()
        self.request_queue.clear()
        logger.info("Orchestrator node shutdown complete")


def main() -> None:
    """Demonstration of Voice Orchestrator Node."""
    logger.info("=" * 100)
    logger.info("VANE-SPACE-SLA Voice Orchestrator Node")
    logger.info("=" * 100)
    
    # Initialize orchestrator node
    orchestrator = VoiceOrchestratorNode(
        node_id="voice-orch-primary-001",
        region="us-east-1",
        max_queue_size=500
    )
    
    # Register agents
    logger.info("\nRegistering voice agents...")
    for i in range(3):
        orchestrator.register_agent(
            agent_id=f"voice-agent-{i:03d}",
            agent_name=f"Voice Agent {i}",
            capabilities=["speech_to_text", "text_to_speech", "nlp_processing"]
        )
    
    # Submit batch requests
    logger.info("\nSubmitting voice requests...")
    requests = [
        {"query": "What is the weather forecast?", "priority": 2, "language": "en-US"},
        {"query": "Schedule a meeting tomorrow", "priority": 1, "language": "en-US"},
        {"query": "Provide system status", "priority": 3, "language": "en-US"},
        {"query": "How can I help?", "priority": 3, "language": "en-US"},
    ]
    
    responses = orchestrator.process_batch_requests(requests)
    
    logger.info(f"\nProcessed {len(responses)} requests")
    for response in responses:
        logger.info(
            f"Request {response.request_id}: {response.status} "
            f"({response.processing_time_ms:.2f}ms, confidence: {response.confidence_score:.2%})"
        )
    
    # Print metrics
    logger.info("\n" + "=" * 100)
    logger.info("ORCHESTRATOR METRICS")
    logger.info("=" * 100)
    metrics = orchestrator.get_metrics()
    logger.info(json.dumps(metrics, indent=2))
    
    # Print agent health
    logger.info("\n" + "=" * 100)
    logger.info("AGENT HEALTH STATUS")
    logger.info("=" * 100)
    health = orchestrator.get_agent_health()
    logger.info(json.dumps(health, indent=2))
    
    # Cleanup
    orchestrator.shutdown()


if __name__ == "__main__":
    main()
