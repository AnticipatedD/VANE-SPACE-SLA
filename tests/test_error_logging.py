"""Tests for structured error reporting in CLI entrypoints."""

from types import SimpleNamespace
from unittest.mock import patch

from src import agent_orchestrator, repo_audit


def test_agent_orchestrator_records_unexpected_failure(monkeypatch):
    monkeypatch.setattr(
        agent_orchestrator.argparse.ArgumentParser,
        "parse_args",
        lambda self: SimpleNamespace(task="test task", model="test-model"),
    )

    def fail(*args, **kwargs):
        raise RuntimeError("simulated orchestration failure")

    monkeypatch.setattr(agent_orchestrator, "run_agent_orchestrator", fail)
    with patch.object(agent_orchestrator.logger, "exception") as log_exception:
        assert agent_orchestrator.main() == 1
        log_exception.assert_called_once()


def test_repository_audit_records_unexpected_failure(monkeypatch):
    monkeypatch.setattr(
        repo_audit.argparse.ArgumentParser,
        "parse_args",
        lambda self: SimpleNamespace(target=repo_audit.Path("src"), model="test-model"),
    )

    def fail(*args, **kwargs):
        raise RuntimeError("simulated audit failure")

    monkeypatch.setattr(repo_audit, "audit_repository", fail)
    with patch.object(repo_audit.logger, "exception") as log_exception:
        assert repo_audit.main() == 1
        log_exception.assert_called_once()
