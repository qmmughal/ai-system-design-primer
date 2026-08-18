# Book

GitHub cannot preview this PDF on the file page (“Unable to render code block”).
Open it in the browser instead:

**[Open The AI System Design Primer (PDF)](https://raw.githubusercontent.com/qmmughal/ai-system-design-primer/main/book/The-AI-System-Design-Primer.pdf)**

125 pages · 7×10 modern trade layout · Qaiser Mehmood

Rebuild after editing chapters:

```bash
npm install --prefix book @mermaid-js/mermaid-cli
python3 -m pip install weasyprint markdown pymupdf
python3 scripts/build_book.py
```

Requires Chrome or Chromium for Mermaid figures, plus Inter, Noto Serif, and JetBrains Mono when available.
