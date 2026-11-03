"""Stage-0 check: the exact displayed code matches the compiled Sedrava demo."""
from pathlib import Path
import json
import re

root = Path(__file__).parent
site = (root / "site.sdr").read_text(encoding="utf-8")
demo = (root / "demos/counter.sdr").read_text(encoding="utf-8").rstrip("\n")
code_blocks = re.findall(r'^\s+code ("(?:\\.|[^"\\])*")\s*$', site, re.MULTILINE)
matches = [json.loads(token) for token in code_blocks if json.loads(token).startswith('webapp "Counter"\n')]
assert len(matches) == 2, f"Expected two counter code samples, found {len(matches)}"
assert all(item == demo for item in matches), "Displayed counter source differs from compiled WebApp"
assert "САЙТ НАПИСАН НА SEDRAVA" in site
assert "BUILT WITH SEDRAVA" in site
assert "0.10.0" in site and "0.11" in site
print("PASS: EN/RU code panels match a real Sedrava demo; status/provenance present")
