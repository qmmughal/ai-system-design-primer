# Book PDF

The trade-book PDF of this primer:

**[The-AI-System-Design-Primer.pdf](The-AI-System-Design-Primer.pdf)**

Rebuild after editing chapters:

```bash
npm install --prefix book @mermaid-js/mermaid-cli
python3 -m pip install weasyprint markdown
python3 scripts/build_book.py
```

Requires Google Chrome or Chromium (for Mermaid figures) and the fonts
Inter, Noto Serif, and JetBrains Mono when available.
