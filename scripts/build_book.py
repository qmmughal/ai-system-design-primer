#!/usr/bin/env python3
"""Build a print book PDF from the primer markdown."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown
from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BOOK = ROOT / "book"
BUILD = BOOK / "build"
DIAGRAMS = BUILD / "diagrams"
ASSETS = BOOK / "assets"
PDF_OUT = BOOK / "The-AI-System-Design-Primer.pdf"

PUPPETEER_CFG = BUILD / "puppeteer.json"
CHROME = os.environ.get("CHROME", "/usr/local/bin/google-chrome")

PARTS: list[tuple[str, str, str, list[tuple[str, Path]]]] = [
    (
        "I",
        "How to think",
        "The mental models, the request path, and the scarce resource of context.",
        [
            ("How to use this primer", DOCS / "topics" / "00-how-to-use.md"),
            ("The systems model of an LLM", DOCS / "topics" / "01-llm-systems-model.md"),
            ("The request path", DOCS / "topics" / "02-request-path.md"),
            ("Context is a scarce resource", DOCS / "topics" / "03-context.md"),
        ],
    ),
    (
        "II",
        "The stack",
        "Retrieval, agents, tools, memory, evals, cost, safety, and the gateway.",
        [
            ("RAG", DOCS / "topics" / "04-rag.md"),
            ("Chunking, embeddings, retrieval", DOCS / "topics" / "05-retrieval.md"),
            ("Agents are loops", DOCS / "topics" / "06-agents.md"),
            ("Tools and MCP", DOCS / "topics" / "07-tools-mcp.md"),
            ("Memory", DOCS / "topics" / "08-memory.md"),
            ("Evals", DOCS / "topics" / "09-evals.md"),
            ("Observability", DOCS / "topics" / "10-observability.md"),
            ("Cost, latency, routing", DOCS / "topics" / "11-cost-latency-routing.md"),
            ("Safety", DOCS / "topics" / "12-safety.md"),
            ("Gateways, caching, structured output", DOCS / "topics" / "13-gateways.md"),
        ],
    ),
    (
        "III",
        "Failure atlas",
        "Production AI fails fluently. These are the eight postmortems that repeat.",
        [
            ("How to read a failure", DOCS / "failures" / "README.md"),
            ("RAG silent lies", DOCS / "failures" / "01-rag-silent-lies.md"),
            ("Agent loops", DOCS / "failures" / "02-agent-loops.md"),
            ("Eval gaming", DOCS / "failures" / "03-eval-gaming.md"),
            ("Prompt injection", DOCS / "failures" / "04-prompt-injection.md"),
            ("Context rot", DOCS / "failures" / "05-context-rot.md"),
            ("Cost blowups", DOCS / "failures" / "06-cost-blowups.md"),
            ("Tool hallucination", DOCS / "failures" / "07-tool-hallucination.md"),
            ("Memory poisoning", DOCS / "failures" / "08-memory-poisoning.md"),
        ],
    ),
    (
        "IV",
        "Interviews",
        "Forty-five minutes, a whiteboard, and judgment. Full staff-level solutions.",
        [
            ("How to run the interview", DOCS / "interviews" / "README.md"),
            ("Design ChatGPT", DOCS / "interviews" / "01-design-chatgpt.md"),
            ("Design a customer support agent", DOCS / "interviews" / "02-customer-support-agent.md"),
            ("Design enterprise RAG", DOCS / "interviews" / "03-enterprise-rag.md"),
            ("Design a coding assistant", DOCS / "interviews" / "04-coding-assistant.md"),
            ("Design AI search", DOCS / "interviews" / "05-ai-search.md"),
            ("Design an LLM gateway", DOCS / "interviews" / "06-llm-gateway.md"),
            ("Design memory for a personal assistant", DOCS / "interviews" / "07-personal-memory.md"),
            ("Design an eval platform", DOCS / "interviews" / "08-eval-platform.md"),
            ("Design a code review agent", DOCS / "interviews" / "09-code-review-agent.md"),
            ("Design a realtime voice agent", DOCS / "interviews" / "10-voice-agent.md"),
            ("Design multimodal product search", DOCS / "interviews" / "11-multimodal-search.md"),
            ("Design workplace search", DOCS / "interviews" / "12-workplace-ai.md"),
            ("Design LLM content moderation", DOCS / "interviews" / "13-moderation.md"),
            ("Design cost-optimized inference", DOCS / "interviews" / "14-cost-optimized-inference.md"),
            ("Design a browsing agent", DOCS / "interviews" / "15-browsing-agent.md"),
            ("Design an AI tutor", DOCS / "interviews" / "16-ai-tutor.md"),
            ("Design meeting summarization", DOCS / "interviews" / "17-meeting-summarization.md"),
            ("Design a multi-agent research system", DOCS / "interviews" / "18-multi-agent-research.md"),
        ],
    ),
]


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "section"


def find_mmdc() -> str:
    for candidate in (
        shutil.which("mmdc"),
        "/tmp/node_modules/.bin/mmdc",
        str(BOOK / "node_modules" / ".bin" / "mmdc"),
    ):
        if candidate and Path(candidate).exists():
            return candidate
    raise SystemExit("mmdc not found. npm install @mermaid-js/mermaid-cli")


def ensure_dirs() -> None:
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    PUPPETEER_CFG.write_text(
        '{"executablePath":"%s","args":["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"]}\n'
        % CHROME
    )


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "smarty", "attr_list"],
    )


def rewrite_links(md: str) -> str:
    def repl(match: re.Match[str]) -> str:
        label, href = match.group(1), match.group(2)
        if href.startswith("http") or href.startswith("mailto:") or href.startswith("#"):
            return match.group(0)
        name = Path(href.split("#")[0]).stem
        if name in {"README", "index"}:
            parent = Path(href.split("#")[0]).parent.name
            if parent == "failures":
                return f"[{label}](#how-to-read-a-failure)"
            if parent == "interviews":
                return f"[{label}](#how-to-run-the-interview)"
        pretty = name
        pretty = re.sub(r"^\d+-", "", pretty)
        return f"[{label}](#{slug(pretty.replace('-', ' '))})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md)


def render_mermaid(source: str, mmdc: str, index: int) -> str:
    digest = hashlib.sha1(source.encode()).hexdigest()[:12]
    png = DIAGRAMS / f"fig-{index:03d}-{digest}.png"
    if not png.exists():
        mmd = png.with_suffix(".mmd")
        mmd.write_text(source.strip() + "\n")
        cmd = [
            mmdc,
            "-p",
            str(PUPPETEER_CFG),
            "-i",
            str(mmd),
            "-o",
            str(png),
            "-b",
            "transparent",
            "-s",
            "2",
            "-q",
        ]
        subprocess.run(cmd, check=True, cwd=BUILD)
    rel = os.path.relpath(png, BUILD)
    return (
        f'\n\n<figure><img src="{rel}" alt="Diagram {index}"/>'
        f"<figcaption>Figure {index}</figcaption></figure>\n\n"
    )


def drop_first_heading(md: str) -> str:
    return re.sub(r"^# [^\n]+\n+", "", md, count=1)


def extract_sections(md: str, titles: list[str]) -> str:
    chunks = []
    for title in titles:
        pat = rf"(^## {re.escape(title)}\n.*?)(?=^## |\Z)"
        m = re.search(pat, md, flags=re.M | re.S)
        if m:
            chunks.append(m.group(1).strip())
    return "\n\n".join(chunks)


def expand_mermaid(md: str, mmdc: str, start: int) -> tuple[str, int]:
    pattern = re.compile(r"```mermaid\n(.*?)```", re.S)
    n = start

    def repl(match: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return render_mermaid(match.group(1), mmdc, n)

    return pattern.sub(repl, md), n


def chapter_html(title: str, kicker: str, body_md: str, mmdc: str, fig: int) -> tuple[str, int, str]:
    cid = slug(title)
    body_md = drop_first_heading(body_md)
    body_md = rewrite_links(body_md)
    body_md, fig = expand_mermaid(body_md, mmdc, fig)
    inner = md_to_html(body_md)
    html = (
        f'<section class="chapter" id="{cid}">'
        f'<p class="chapter-kicker">{kicker}</p>'
        f'<h1 class="chapter-title">{title}</h1>'
        f"{inner}</section>"
    )
    return html, fig, cid


def build() -> None:
    ensure_dirs()
    mmdc = find_mmdc()
    fig = 0
    toc: list[tuple[str, str, str]] = []
    body: list[str] = []

    index_md = (DOCS / "index.md").read_text()
    preface_md = extract_sections(
        index_md,
        ["Why this exists", "Ten laws", "The picture you should be able to draw", "Numbers in this repo"],
    )
    preface_md, fig = expand_mermaid(preface_md, mmdc, fig)
    preface_md = rewrite_links(preface_md)
    body.append(
        '<section class="preface chapter" id="preface">'
        '<p class="chapter-kicker">Front matter</p>'
        '<h1 class="chapter-title">Preface</h1>'
        + md_to_html(preface_md)
        + "</section>"
    )
    toc.append(("chapter", "Preface", "preface"))

    for roman, part_title, deck, chapters in PARTS:
        pid = slug(f"part {part_title}")
        body.append(
            f'<section class="part-page" id="{pid}">'
            f'<p class="part-label">Part {roman}</p>'
            f"<h1>{part_title}</h1>"
            f'<p class="part-deck">{deck}</p>'
            "</section>"
        )
        toc.append(("part", f"Part {roman} · {part_title}", pid))
        for i, (title, path) in enumerate(chapters, start=1):
            kicker = f"Part {roman} · Chapter {i}"
            if roman == "IV":
                kicker = f"Part {roman} · Interview {i}" if i > 1 else f"Part {roman} · Chapter {i}"
            if roman == "III" and i > 1:
                kicker = f"Part {roman} · Failure {i - 1}"
            html, fig, cid = chapter_html(title, kicker, path.read_text(), mmdc, fig)
            body.append(html)
            toc.append(("chapter", title, cid))

    toc_html = ['<nav class="toc front"><h1>Contents</h1><ol>']
    for kind, label, cid in toc:
        toc_html.append(f'<li><a class="{kind}" href="#{cid}">{label}</a></li>')
    toc_html.append("</ol></nav>")

    cover = ASSETS / "cover.png"
    cover_html = (
        f'<article class="cover-page"><img src="{cover.resolve()}" alt="Cover"/></article>'
        if cover.exists()
        else ""
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>The AI System Design Primer</title>
  <meta name="author" content="Qaiser Mehmood"/>
  <meta name="description" content="Learn how to design production AI systems. Prep for the AI system design interview."/>
</head>
<body>
{cover_html}
<section class="half-title front">
  <p>The AI System Design Primer</p>
</section>
<section class="title-page front">
  <h1>The AI System Design Primer</h1>
  <div class="title-rule"></div>
  <p class="subtitle">Learn how to design production AI systems.<br/>Prep for the AI system design interview.</p>
  <p class="author">Qaiser Mehmood</p>
  <p class="imprint">A living technical handbook · 2026</p>
</section>
<section class="copyright front">
  <p><strong>The AI System Design Primer</strong></p>
  <p>Copyright © 2026 Qaiser Mehmood and contributors.</p>
  <p>Prose is licensed under Creative Commons Attribution–ShareAlike 4.0 International.
  Code samples are MIT.</p>
  <p>This PDF is generated from the living GitHub handbook and will go stale
  when the field moves. Prefer the repository for corrections.</p>
  <p>github.com/qmmughal/ai-system-design-primer</p>
  <p>First edition, 2026. Typeset in Noto Serif, Inter, and JetBrains Mono.</p>
</section>
{''.join(toc_html)}
{''.join(body)}
<section class="colophon chapter" id="colophon">
  <h1>Colophon</h1>
  <p>This book was generated from the Markdown source of the primer. Figures
  are rendered from the Mermaid diagrams in the repository. Running heads,
  parts, and page geometry follow a 7.5 × 9.5 inch trade-book layout.</p>
  <p>Rebuild with <code>python3 scripts/build_book.py</code>.</p>
</section>
</body>
</html>
"""
    BUILD.joinpath("book.html").write_text(html)
    print(f"Rendering PDF ({fig} figures)…", flush=True)
    HTML(string=html, base_url=str(BUILD)).write_pdf(
        PDF_OUT,
        stylesheets=[CSS(filename=str(BOOK / "book.css"))],
        metadata={
            "title": "The AI System Design Primer",
            "authors": ["Qaiser Mehmood"],
            "description": "Learn how to design production AI systems. Prep for the AI system design interview.",
            "keywords": ["AI", "system design", "LLM", "RAG", "agents"],
            "generator": "The AI System Design Primer book builder",
        },
    )
    print(f"Wrote {PDF_OUT} ({PDF_OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    try:
        build()
    except subprocess.CalledProcessError as exc:
        sys.exit(f"diagram render failed: {exc}")
