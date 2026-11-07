"""Serve the real static build and verify branding in Chromium (requires Playwright)."""
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
master = ROOT / 'public/brand/sedrava-logo-primary.png'
assert hashlib.sha256(master.read_bytes()).hexdigest() == 'da9c46be34b8a14d5fb262d3ae1bb18c4ff4b50badd8541837d2d8128d1e1fbb'
for line in (master.parent / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ')
    assert hashlib.sha256((master.parent / name).read_bytes()).hexdigest() == digest, name
output = ROOT / 'build/branding-check'
output.mkdir(parents=True, exist_ok=True)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / 'dist'))
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
results = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(**({'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}))
        for language, route in [('en','/'), ('ru','/ru/')]:
            for theme in ['light', 'dark']:
                for width in [360, 768, 1440]:
                    page = browser.new_page(viewport={'width':width,'height':1000}, color_scheme=theme)
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    response = page.goto(f'http://127.0.0.1:{server.server_port}{route}')
                    assert response.status == 200
                    page.evaluate('(theme) => { localStorage.setItem("starlight-theme",theme); document.documentElement.dataset.theme=theme; }', theme)
                    page.locator('.site-title img').wait_for()
                    page.wait_for_function('Array.from(document.images).every(i => i.complete)')
                    assert page.locator('img').evaluate_all('(images) => images.every(i => i.naturalWidth > 0)'), 'broken image'
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route,width,'overflow')
                    assert page.locator('.site-title img').evaluate('(i) => getComputedStyle(i).objectFit === "contain"')
                    assert page.locator('meta[property="og:image"]').get_attribute('content').endswith('/brand/sedrava-og.png')
                    page.keyboard.press('Tab')
                    assert page.evaluate('document.activeElement.tagName === "A"'), 'keyboard navigation'
                    assert not errors, errors
                    name = f'{language}-{theme}-{width}'
                    page.screenshot(path=str(output / f'{name}.png'), full_page=True)
                    results.append({'case':name,'status':'PASS'})
                    page.close()
        browser.close()
finally:
    server.shutdown()
(output / 'results.json').write_text(json.dumps(results, indent=2)+'\n')
print(f'PASS: {len(results)} browser cases; master and derivative checksums verified')
