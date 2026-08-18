# AI system design interviews

These solutions are *one* coherent staff-level answer, not the only
answer. If you memorize them you will sound like a blog. If you can
rebuild them from the [ten laws](../index.md#ten-laws) on a whiteboard,
you are ready.

## Format

45 minutes unless the host says otherwise.

| Clock | Move |
| --- | --- |
| 0–5 | Requirements, non-goals, trust model |
| 5–12 | Scale + token/$/latency envelope |
| 12–22 | One diagram, request path, stores |
| 22–38 | Two deep dives the prompt actually cares about |
| 38–45 | Failures, evals, what you would cut |

They will interrupt. Let them. The interview is a conversation about
judgment, not a speech.

## Template every solution in this folder uses

1. **Clarify** — users, wrong-answer cost, write vs read, latency, cost
2. **Scale** — invented if needed, labeled as invented
3. **Envelope** — QPS, tokens, $/day, TTFT
4. **Picture** — mermaid
5. **Deep dives** — 2–4
6. **Failures** — linked to the atlas
7. **Evals**
8. **Listen for** — the phrases that score
9. **Cut list** — what you drop under time or money pressure

## How to practice

- 40 minutes, out loud, laptop closed except a blank diagram
- Then read the solution and note the *one* deep dive you skipped
- Do the same prompt again a week later; the diagram should get simpler

## Index

1. [Design ChatGPT](01-design-chatgpt.md) — platform chat
2. [Customer support agent](02-customer-support-agent.md) — tools + policy
3. [Enterprise RAG](03-enterprise-rag.md) — retrieval + ACLs
4. [Coding assistant](04-coding-assistant.md) — repo working set
5. [AI search](05-ai-search.md) — live web + citations
6. [LLM gateway](06-llm-gateway.md) — platform
7. [Personal assistant memory](07-personal-memory.md) — memory stores
8. [Eval platform](08-eval-platform.md) — meta-system
9. [Code review agent](09-code-review-agent.md) — gated writes
10. [Voice agent](10-voice-agent.md) — latency
11. [Multimodal product search](11-multimodal-search.md) — embeddings
12. [Workplace search](12-workplace-ai.md) — tenancy
13. [Moderation](13-moderation.md) — precision
14. [Cost-optimized inference](14-cost-optimized-inference.md) — $
15. [Browsing agent](15-browsing-agent.md) — injection
16. [AI tutor](16-ai-tutor.md) — memory + pedagogy
17. [Meeting summarization](17-meeting-summarization.md) — batch + PII
18. [Multi-agent research](18-multi-agent-research.md) — loops + isolation
