#!/usr/bin/env python3
"""Headless mobile regression for the generated Sedrava static showcase.

Run after scripts/build_dev_site.py in GitHub Actions. Screenshots are saved
as CI artifacts; no screenshot publishing, tracking or public API access.
"""
from __future__ import annotations
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "build" / "sedrava-dev"
REPORT = ROOT / "build" / "dev-mobile-check"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        pass


@contextmanager
def local_site():
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(SITE))
    )
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        worker.join(timeout=5)
        server.server_close()


def verify():
    assert (SITE / "index.html").is_file()
    REPORT.mkdir(parents=True, exist_ok=True)
    sizes = (320, 360, 390, 768, 1280)
    with local_site() as url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in sizes:
                ctx = browser.new_context(
                    viewport={"width": width, "height": 900},
                    device_scale_factor=1,
                    is_mobile=width <= 390,
                    has_touch=width <= 390,
                )
                page = ctx.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                result = page.goto(url + "/", wait_until="networkidle", timeout=25000)
                assert result and result.status == 200, (width, result)
                metrics = page.evaluate("""() => {
                  const body = document.body;
                  const root = document.documentElement;
                  const title = document.querySelector('h1');
                  const cta = document.querySelector('a.s-button');
                  const logos = [...document.querySelectorAll('img')];
                  const link = document.querySelector('link[rel="stylesheet"]');
                  const ctaRect = cta.getBoundingClientRect();
                  return {
                    width: innerWidth,
                    bodyScrollWidth: body.scrollWidth,
                    htmlScrollWidth: root.scrollWidth,
                    titleFont: parseFloat(getComputedStyle(title).fontSize),
                    textColor: getComputedStyle(body).color,
                    colorScheme: getComputedStyle(root).colorScheme,
                    theme: getComputedStyle(root).getPropertyValue('--background').trim(),
                    cssVersioned: link?.getAttribute('href')?.includes('?v='),
                    logosLoaded: logos.every(x => x.complete && x.naturalWidth > 0),
                    logos: logos.length,
                    ctaLeft: ctaRect.left,
                    ctaRight: ctaRect.right,
                    ctaHeight: ctaRect.height,
                    navLinks: document.querySelectorAll('a.s-link.v-quiet').length,
                  };
                }""")
                assert not errors, (width, errors)
                assert metrics["bodyScrollWidth"] <= width + 2, (width, metrics)
                assert metrics["htmlScrollWidth"] <= width + 2, (width, metrics)
                assert metrics["colorScheme"] == "dark", (width, metrics)
                assert metrics["theme"].lower() == "#141020", (width, metrics)
                assert metrics["cssVersioned"], (width, metrics)
                assert metrics["logosLoaded"] and metrics["logos"] >= 2, (width, metrics)
                assert metrics["ctaLeft"] >= -2 and metrics["ctaRight"] <= width + 2, (width, metrics)
                assert metrics["ctaHeight"] >= 45, (width, metrics)
                assert metrics["navLinks"] >= 4, (width, metrics)
                if width in (360, 390, 1280):
                    page.screenshot(
                        path=str(REPORT / f"sedrava-demo-{width}.png"),
                        full_page=True,
                    )
                print(f"PASS viewport={width}: no horizontal overflow, assets loaded, dark theme, CTA visible")
                ctx.close()
        finally:
            browser.close()


if __name__ == "__main__":
    verify()
