# Failure atlas

Production AI fails **fluently**. The system still returns 200. The
sentence still parses. The user still thanks it. These pages are the
failures that show up in postmortems regardless of vendor.

Each failure is:

1. **Mechanism** — what is actually happening
2. **What it looks like** — the ticket
3. **Detection** — the metric or trace
4. **Fix** — in the system, not in the prompt
5. **Eval** — the case that would have caught it
6. **Interview cue** — when to bring it up unprompted

If you have a new one from production, add a file and a row here.
Anonymous is fine. See [CONTRIBUTING.md](../contributing.md).

| # | Failure | Mechanism in one line |
| --- | --- | --- |
| 1 | [RAG silent lies](01-rag-silent-lies.md) | Weak evidence, strong prose |
| 2 | [Agent loops](02-agent-loops.md) | No halt, or halt that never fires |
| 3 | [Eval gaming](03-eval-gaming.md) | The test and the system share a tell |
| 4 | [Prompt injection](04-prompt-injection.md) | Untrusted text became instructions |
| 5 | [Context rot](05-context-rot.md) | Working set admitted junk |
| 6 | [Cost blowups](06-cost-blowups.md) | Decode × tools × retries |
| 7 | [Tool hallucination](07-tool-hallucination.md) | RPC invented or skipped |
| 8 | [Memory poisoning](08-memory-poisoning.md) | A lie got a long TTL |

When you design, pick the two failures your product is *for*. A browsing
agent that does not mention (4) has not started. A RAG handbook that
does not mention (1) has not started.
