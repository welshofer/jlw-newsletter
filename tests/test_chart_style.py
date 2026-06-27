"""Tests for chart_style.py (REL-2: configurable output dir, default-identical)."""
import importlib
import os

import chart_style


def test_output_path_joins_under_base():
    expected = os.path.join(chart_style.OUTPUT_BASE, "images", "x.png")
    assert chart_style.output_path("images", "x.png") == expected


def test_default_base_is_backward_compatible(monkeypatch):
    """With JLW_OUTPUT_DIR unset, the base must equal the original hardcoded
    path so production output locations are byte-identical."""
    monkeypatch.delenv("JLW_OUTPUT_DIR", raising=False)
    reloaded = importlib.reload(chart_style)
    try:
        assert reloaded.OUTPUT_BASE == "/Users/welshofer/clawd/jlw-newsletter"
        assert (
            reloaded.output_path("images", "chart.png")
            == "/Users/welshofer/clawd/jlw-newsletter/images/chart.png"
        )
    finally:
        importlib.reload(chart_style)  # restore default module state


def test_env_override(monkeypatch):
    monkeypatch.setenv("JLW_OUTPUT_DIR", "/tmp/sandbox")
    reloaded = importlib.reload(chart_style)
    try:
        assert reloaded.output_path("images", "x.png") == "/tmp/sandbox/images/x.png"
    finally:
        monkeypatch.delenv("JLW_OUTPUT_DIR", raising=False)
        importlib.reload(chart_style)
