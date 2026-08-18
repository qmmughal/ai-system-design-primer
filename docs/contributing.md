# Contributing

This is a living document. The field moves; the primer should move with it.
A contribution is useful when it makes a future reader *more precise*, not
when it adds another heading.

## What we want

- **Corrections** with a source (paper, incident, vendor doc, your production
  numbers). Replace stale prices, model names, and latency claims.
- **New failure modes** from real systems. Anonymous is fine. Include: what
  you observed, the mechanism, the detection, the fix, and the eval that
  would have caught it.
- **Interview solutions** that an interviewer could actually run. Clarify
  requirements, do back-of-envelope math, pick an architecture, deep-dive
  3–5 components, name failure modes, and close with tradeoffs.
- **Diagrams** in Mermaid. Prefer one idea per diagram.

## What we do not want

- Vendor pitch decks, "awesome lists" of links, or "coming soon" sections.
- Framework tutorials (`how to use library X`). Teach the system, then name
  tools as examples.
- Benchmark screenshots without the eval design.
- Agent hype. If a DAG, a classifier, or a SQL query would do, say so.

## How to add a topic

1. Write a complete chapter in `topics/`. The file must teach: a definition,
   a diagram, numbers, failure modes, and a "what interviewers listen for"
   section. No stubs.
2. Link it from [index.md](index.md) and from `mkdocs.yml` at the repo root.
3. If the topic changes interview advice, update the relevant interview.

## How to add a failure

Use the template in [`failures/README.md`](failures/README.md). One file per
failure. Title the file after the *mechanism* (`rag-silent-lies.md`), not the
symptom (`wrong-answers.md`).

## How to add an interview

Use the template in [`interviews/README.md`](interviews/README.md). Solutions
should be 80% architecture and 20% product. Invent a scale and stick to it.

## Voice

Write like a staff engineer reviewing a design doc:

- Prefer "do X because Y" over "you should consider X".
- Put the recommendation before the taxonomy.
- Use approximate numbers and label them as such. Prices change; ratios last
  longer (`output tokens cost ~4–8× input` is better than a screenshot).
- Name the tradeoff in the same paragraph as the choice.

## Local site

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

## License

Prose is [CC BY-SA 4.0](license.md). Code samples are MIT. By contributing you
agree your text ships under CC BY-SA 4.0 and your code samples under MIT.
