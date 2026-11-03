import pytest
from unittest.mock import MagicMock
from src.agent_orchestrator import run_agent_orchestrator

def test_agent_orchestrator_mocked(mocker):
    mock_client = MagicMock()
    mock_chunk = MagicMock()
    mock_chunk.text = "Architect & Security Review Passed"
    mock_client.models.generate_content_stream.return_value = [mock_chunk]
    
    mocker.patch("src.agent_orchestrator.genai.Client", return_value=mock_client)
    mocker.patch("os.environ", {"GEMINI_API_KEY": "test-key"})

    try:
        run_agent_orchestrator("Validate zero-trust telemetry pipeline", model="gemini-2.5-flash")
    except SystemExit:
        pytest.fail("Orchestrator exited unexpectedly")

    assert mock_client.models.generate_content_stream.call_count == 2
