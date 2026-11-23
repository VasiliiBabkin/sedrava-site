#!/usr/bin/env python3
"""Build the Sedrava-authored static showcase, then add audited responsive styles.

The HTML structure is still built from sedrava-dev/site.sdr by the pinned
Sedrava compiler. The current experimental generator has a limited theme DSL,
so we deliberately append a versioned, source-controlled CSS layer. No JS.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "sedrava-dev" / "site.sdr"
THEME = ROOT / "sedrava-dev" / "theme.css"
BRAND = ROOT / "sedrava-dev" / "assets" / "sedrava-logo-primary.png"
FAVICON = ROOT / "sedrava-dev" / "assets" / "favicon.ico"
OUT = ROOT / "build" / "sedrava-dev"

APPROVED_BRAND_SHA256 = "da9c46be34b8a14d5fb262d3ae1bb18c4ff4b50badd8541837d2d8128d1e1fbb"
APPROVED_FAVICON_SHA256 = "a7b2cf84bafaa06cd8c303c2629183ecba0d80b620582f944e8fded656a8c1bf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> None:
    assert sha256(BRAND) == APPROVED_BRAND_SHA256, "Official master logo has changed"
    assert sha256(FAVICON) == APPROVED_FAVICON_SHA256, "Official favicon has changed"

    # The experimental compiler refuses to overwrite a modified output
    # (including appended CSS). Rebuild only the known disposable build tree.
    if OUT.exists():
        assert OUT.is_dir() and not OUT.is_symlink()
        assert OUT.parent.resolve() == (ROOT / "build").resolve()
        assert (OUT / "sedrava-site.json").is_file()
        shutil.rmtree(OUT)

    subprocess.run(
        [sys.executable, "-m", "sedrava_cli", "build", "site",
         str(SOURCE), "--output", str(OUT)],
        cwd=ROOT,
        check=True,
        env=os.environ,
    )

    css_path = OUT / "site.css"
    html_path = OUT / "index.html"
    assert css_path.is_file() and html_path.is_file()
    original_css = css_path.read_text(encoding="utf-8")
    theme_css = THEME.read_text(encoding="utf-8")
    assert ":root" in original_css and "@media (max-width: 720px)" in theme_css
    css_path.write_text(original_css + "\n\n" + theme_css, encoding="utf-8")

    html = html_path.read_text(encoding="utf-8")
    if '<meta name="color-scheme" content="dark">' in html:
        html = html.replace(
            '<meta name="color-scheme" content="dark">',
            '<meta name="color-scheme" content="dark"><meta name="theme-color" content="#141020">',
        )
    else:
        assert '<meta name="color-scheme" content="light">' in html
        html = html.replace(
            '<meta name="color-scheme" content="light">',
            '<meta name="color-scheme" content="dark"><meta name="theme-color" content="#141020">',
        )
    checks = [
        ('<link rel="icon" href="favicon.svg">',
         '<link rel="icon" type="image/x-icon" href="favicon.ico">'),
        ('<link rel="stylesheet" href="site.css">',
         f'<link rel="stylesheet" href="site.css?v={sha256(css_path)[:16]}">'),
    ]
    for old, new in checks:
        assert html.count(old) == 1, f"Unexpected Sedrava HTML shape: {old}"
        html = html.replace(old, new)
    html_path.write_text(html, encoding="utf-8")
    shutil.copyfile(FAVICON, OUT / "favicon.ico")

    assert 'assets/' in html and 'Фирменный знак Sedrava' in html
    assert 'SedravaSQL' in html and 'НАТИВНЫЙ СЕРВЕР' in html
    assert 'site.css?v=' in html and '#141020' in css_path.read_text(encoding="utf-8")
    assert (OUT / "sedrava-site.json").is_file()
    print("PASS: Sedrava-generated HTML + dark responsive theme + exact approved logo/favicon")
    print("PASS: cache-busted CSS, local-only static output, native/SQL content")


if __name__ == "__main__":
    build()
