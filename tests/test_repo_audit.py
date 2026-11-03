import pytest
from pathlib import Path
from unittest.mock import MagicMock
from src.repo_audit import collect_python_files, build_audit_prompt, audit_repository

def test_collect_python_files_ignores_dirs(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "valid.py").write_text("print('ok')", encoding="utf-8")
    
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "ignored.py").write_text("print('ignore')", encoding="utf-8")

    files = collect_python_files(src)
    assert len(files) == 1
    assert any("valid.py" in str(p) for p in files.keys())
    assert not any("ignored.py" in str(p) for p in files.keys())

def test_collect_python_files_max_size(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    huge_file = src / "huge.py"
    # Write a file exceeding MAX_FILE_BYTES (500 KB)
    huge_file.write_text("x = 1\n" * 100_000, encoding="utf-8")

    files = collect_python_files(src)
    assert len(files) == 1
    assert "skipped" in files[huge_file]

def test_build_audit_prompt():
    dummy_files = {Path("src/main.py"): "print('test')"}
    prompt = build_audit_prompt(dummy_files)
    assert "src/main.py" in prompt
    assert "print('test')" in prompt

def test_audit_repository_mocked(mocker, tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "sample.py").write_text("print('hello')", encoding="utf-8")

    mock_client = MagicMock()
    mock_chunk = MagicMock()
    mock_chunk.text = "Audit Report Success"
    mock_client.models.generate_content_stream.return_value = [mock_chunk]

    mocker.patch("src.repo_audit.genai.Client", return_value=mock_client)
    mocker.patch("os.environ", {"GEMINI_API_KEY": "test-key"})

    # Should execute successfully without throwing exceptions
    audit_repository(src, model="gemini-2.5-flash")
    mock_client.models.generate_content_stream.assert_called_once()
