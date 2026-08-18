# How to use this primer

Read this once. Then stop reading like a blog and start running designs.

## The unit of work is a design, not a chapter

A chapter is vocabulary. Skill is what happens when you take a vague prompt
("design a support bot") and, in 40 minutes, produce:

1. A requirements list with explicit non-goals
2. A back-of-envelope for QPS, tokens, cost, and latency
3. A one-page architecture
4. Two or three deep dives
5. The failures you expect on day 30
6. The eval that would have caught them on day 0

If you cannot do that out loud, you do not know the topic yet. Re-read the
chapter, then retry the matching interview with a timer.

## How an AI system design interview actually runs

It is the old system-design loop with four extra questions. Interviewers
almost always ask some cut of:

| Minute | They are testing | You should |
| --- | --- | --- |
| 0–5 | Product sense | Clarify users, trust, latency, cost, offline vs online |
| 5–10 | Numeracy | Estimate tokens in/out, cache hit rate, $/day |
| 10–20 | Architecture | Draw the request path, stores, and control plane |
| 20–35 | Depth | Zoom into retrieval, tools, evals, or safety |
| 35–45 | Judgment | Name failures, what you would cut, what you would measure first |

They are not testing whether you have used LangGraph. They are testing
whether you treat a probabilistic component as a system.

### Questions you ask in the first five minutes

- Who is the user, and what happens if the answer is wrong?
- What is the latency budget (TTFT vs complete)? Streaming or not?
- What is the cost budget per request and per day?
- What data is trusted? What data is attacker-controlled?
- What actions can the system take (read vs write vs pay vs email)?
- What is the empty-corpus / cold-start story?
- Online, batch, or both?
- Single tenant or many, with data isolation?

Write the answers on the board. Designs die when those stay implicit.

## Back-of-envelope that is specific to LLMs

Always estimate four numbers. Invent a scale if the interviewer will not
give you one, and say you are inventing it.

```text
requests / day
× tokens_in  (prompt + retrieved + memory + tool dumps)
× tokens_out (including hidden reasoning if you pay for it)
× $ / million tokens, split input vs output vs cached
= $ / day

p50 / p95 TTFT
p50 / p95 total latency  (or tokens-per-second × tokens_out)
tool calls / request × tool latency
retry rate × the above
```

A worked example lives in
[Design ChatGPT](../interviews/01-design-chatgpt.md). Copy the shape,
not the dollar figures.

## How to read a topic chapter

Every topic in this primer is built the same way on purpose:

1. **Recommendation** — what to do by default
2. **Picture** — one diagram
3. **Mechanism** — why it works, with numbers
4. **Choices** — the actual forks you will be asked about
5. **Failures** — link into the atlas
6. **What interviewers listen for** — the phrases that score

Skip around. The README study paths are suggestions, not a course.

## How to keep this living

When a model generation lands, three things in this repo go stale first:

- Context-window folklore ("just stuff the PDF in")
- Price examples
- Which job is "too hard for a small model"

Update the chapter and date the change. Do not add a "2026 updates"
graveyard section. Fold the new truth into the recommendation.
