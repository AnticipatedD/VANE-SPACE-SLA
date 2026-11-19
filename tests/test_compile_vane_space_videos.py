"""Tests for the media pipeline's optional MoviePy dependency fallback."""

import importlib.util

import compile_vane_space_videos


def test_media_pipeline_falls_back_when_moviepy_is_unavailable(monkeypatch):
    monkeypatch.setattr(importlib.util, "find_spec", lambda _name: None)

    assert compile_vane_space_videos.assemble_submission_video() is False


def test_media_pipeline_accepts_detected_moviepy_dependency(monkeypatch):
    monkeypatch.setattr(importlib.util, "find_spec", lambda _name: object())

    assert compile_vane_space_videos.assemble_submission_video() is True
