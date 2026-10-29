#!/usr/bin/env python3
"""Generate bilingual upstream status pages from a checked-out Sedrava repository."""
import argparse
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--source", required=True)
p.add_argument("--sha", required=True)
p.add_argument("--output", default="src/content/docs")
a = p.parse_args()
source = Path(a.source)
for needed in ("docs/ROADMAP.md", "docs/LANGUAGE_0_10_TEXT.md", "examples/text_profile.sdr"):
    if not (source / needed).is_file():
        raise SystemExit(f"Missing upstream file: {needed}")
sha = a.sha.strip()
if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
    raise SystemExit("Invalid upstream commit SHA")
base = "https://github.com/VasiliiBabkin/sedrava/blob/" + sha + "/"
pages = [
    ("upstream-status.md", "Upstream development status",
     "Automatically tracked source revision and authoritative Sedrava documents.",
     "This page tracks the latest source revision of the language repository. A new revision does **not** mean a new release. The site publishes this update only after review and merge of its synchronization pull request.",
     "Source revision", "Authoritative documents", [
         ("Roadmap", "docs/ROADMAP.md"),
         ("0.9 language specification", "docs/LANGUAGE_0_9.md"),
         ("0.10 text development specification", "docs/LANGUAGE_0_10_TEXT.md"),
         ("0.10 text engineering report", "docs/TEXT_010_REPORT.md"),
         ("Working text profile example", "examples/text_profile.sdr"),
     ]),
    ("ru/upstream-status.md", "Состояние разработки языка",
     "Автоматически отслеживаемая ревизия исходников и официальные документы Sedrava.",
     "Здесь указана актуальная ревизия исходников языка. **Новый коммит не означает новый выпуск.** Страница обновляется на сайте только после проверки и объединения PR синхронизации.",
     "Ревизия исходников", "Основные документы", [
         ("Дорожная карта", "docs/ROADMAP.md"),
         ("Спецификация 0.9", "docs/LANGUAGE_0_9.md"),
         ("Текстовое ядро 0.10", "docs/LANGUAGE_0_10_TEXT.md"),
         ("Отчёт об испытаниях текста", "docs/TEXT_010_REPORT.md"),
         ("Рабочий пример текстового профиля", "examples/text_profile.sdr"),
     ]),
]
for filename, title, description, intro, revision, heading, links in pages:
    lines = ["---", f"title: {title}", f"description: {description}", "---", "", intro,
             "", f"## {revision}", "", f"[`{sha[:12]}`](https://github.com/VasiliiBabkin/sedrava/commit/{sha})",
             "", f"## {heading}", ""]
    lines += [f"- [{label}]({base}{path})" for label, path in links if (source / path).is_file()]
    out = Path(a.output) / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
