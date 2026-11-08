import pytest
from pathlib import Path
from unittest.mock import MagicMock
from src.repo_audit import audit_repository, collect_python_files, build_audit_prompt


def test_collect_python_files(tmp_path):
    test_file = tmp_path / "test_module.py"
    test_file.write_text("print('hello')", encoding="utf-8")

    files = collect_python_files(tmp_path)
    assert test_file in files
    assert files[test_file] == "print('hello')"


def test_build_audit_prompt():
    path = Path("src/dummy.py")
    prompt = build_audit_prompt({path: "x = 1"})
    assert "src/dummy.py" in prompt
    assert "x = 1" in prompt


def test_audit_repository_offline(tmp_path):
    test_file = tmp_path / "sample.py"
    test_file.write_text("x = 42", encoding="utf-8")

    mock_client = MagicMock()
    mock_chunk = MagicMock()
    mock_chunk.text = "Audit Report OK"
    mock_client.models.generate_content_stream.return_value = [mock_chunk]

    audit_repository(tmp_path, model="gemini-2.5-flash", client=mock_client)
    mock_client.models.generate_content_stream.assert_called_once()
