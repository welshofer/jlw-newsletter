"""SEC-1 regression: the archive index must HTML-escape newsletter-derived
text so a title/subtitle containing markup cannot inject into index.html."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GEN = ROOT / "scripts" / "generate_index.py"

FIXTURE = """<!doctype html>
<html><head>
<title>Pwn &amp; &lt;script&gt;alert(1)&lt;/script&gt;</title>
</head><body>
<p class="hero-subtitle">Danger &amp; &lt;img src=x onerror=alert(2)&gt;</p>
</body></html>
"""


def test_index_escapes_injected_markup(tmp_path):
    (tmp_path / "jlw-2026-01-01-pwn.html").write_text(FIXTURE)

    result = subprocess.run(
        [sys.executable, str(GEN), str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    out = (tmp_path / "index.html").read_text()

    # The injected payloads must NOT appear as live markup...
    assert "<script>alert(1)</script>" not in out
    assert "<img src=x onerror=alert(2)>" not in out
    # ...they must appear escaped.
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in out
    assert "Pwn &amp; " in out
