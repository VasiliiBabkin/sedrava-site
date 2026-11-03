"""Real Chromium smoke checks for Sedrava-native website and generated live examples.

The site and demos are compiled independently from .sdr; this script does not
patch generated HTML, CSS or JavaScript. It only serves build output and tests it.
"""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import shutil
import threading
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
EVIDENCE = BUILD / "native-browser-evidence"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class NativeSiteBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (BUILD / "native-site/index.html").is_file():
            raise AssertionError("Build the native site before browser smoke checks")
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(BUILD)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(
            executable_path=os.environ.get("SEDRAVA_CHROMIUM") or shutil.which("chromium"),
            args=["--no-sandbox"])
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        EVIDENCE.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], "Page emitted JavaScript exceptions")

    def goto(self, path):
        response = self.page.goto(self.base + path, wait_until="domcontentloaded")
        self.assertEqual(response.status, 200)
        return self.page

    def test_en_ru_pages_and_exact_counter_code(self):
        source = (ROOT / "sedrava-next/demos/counter.sdr").read_text(encoding="utf-8").strip()
        p = self.goto("/native-site/")
        self.assertTrue(p.get_by_text("BUILT WITH SEDRAVA", exact=True).is_visible())
        self.assertTrue(p.get_by_role("heading", name="The language that builds its own website.").is_visible())
        p.get_by_role("link", name="Examples", exact=True).click()
        self.assertIn("/native-site/examples/", p.url)
        self.assertEqual(p.locator("pre code").inner_text().strip(), source)
        self.assertTrue(p.get_by_text("not yet embedded", exact=False).is_visible())
        self.goto("/native-site/ru/")
        self.assertTrue(p.get_by_text("САЙТ НАПИСАН НА SEDRAVA", exact=True).is_visible())
        p.get_by_role("link", name="Примеры", exact=True).click()
        self.assertEqual(p.locator("pre code").inner_text().strip(), source)

    def test_counter_actually_updates_and_persists(self):
        p = self.goto("/live-examples/counter/")
        self.assertTrue(p.get_by_role("heading", name="A live Sedrava counter").is_visible())
        self.assertEqual(p.locator("output[data-state=count]").inner_text(), "0")
        p.get_by_role("button", name="Add one").click()
        p.get_by_role("button", name="Add one").click()
        self.assertEqual(p.locator("output[data-state=count]").inner_text(), "2")
        p.reload()
        self.assertEqual(p.locator("output[data-state=count]").inner_text(), "2")
        self.assertEqual(p.locator("script:not([src])").count(), 0)

    def test_tasks_and_crm_render_after_real_compilation(self):
        p = self.goto("/live-examples/tasks/")
        self.assertTrue(p.get_by_role("heading", name="Tasks on Sedrava").is_visible())
        p.get_by_label("New task").fill("From site smoke test")
        p.get_by_role("button", name="Add task").click()
        self.assertEqual(p.locator('[data-list], [data-each]').count() > 0, True)
        p.reload()
        self.assertTrue(p.get_by_text("From site smoke test").first.is_visible())
        self.goto("/live-examples/crm/")
        self.assertTrue(p.get_by_role("heading", name="Your client desk").is_visible())

    def test_mobile_and_desktop_without_horizontal_overflow(self):
        for width in (320, 360, 390, 768, 1024, 1440):
            self.page.set_viewport_size({"width": width, "height": 900})
            self.goto("/native-site/ru/examples/")
            self.assertLessEqual(
                self.page.evaluate("document.documentElement.scrollWidth"), width + 1,
                f"Overflow at {width}px")
            self.page.screenshot(path=str(EVIDENCE / f"ru-examples-{width}.png"), full_page=True)
            self.goto("/live-examples/counter/")
            self.assertLessEqual(
                self.page.evaluate("document.documentElement.scrollWidth"), width + 1,
                f"Counter overflow at {width}px")
            self.page.screenshot(path=str(EVIDENCE / f"counter-{width}.png"), full_page=True)


if __name__ == "__main__":
    unittest.main()
