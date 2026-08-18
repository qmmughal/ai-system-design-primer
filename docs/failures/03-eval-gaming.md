# Eval gaming

Offline scores went up. Production got worse. The team shipped the
prompt that the judge liked.

## Mechanism

You optimized the system against a **proxy** that the system can
satisfy without doing the job.

Classic tells:

- LLM-as-judge shares phrasing with the product prompt ("be concise,
  cite sources, use headings") so the judge awards style
- The gold answers leaked into few-shot examples
- Retrieval eval uses the live index, which now contains the test
  questions (or the answers)
- A router learned to send everything to the model the judge is
- Humans in the loop started labeling like the judge to go home

This is Goodhart's law with a sampler in the loop. It is also how
you get [silent lies](01-rag-silent-lies.md) with a green dashboard.

## What it looks like

- "Groundedness 0.91" while support tickets about wrong refunds rise
- A model that learned to say "according to the docs" without a citation
  id the verifier checks
- Agent evals that count "made a plan" as success
- Leaderboard chasing on a public RAG bench that is now in pretraining

## Detection

- **Human dual-label** on a frozen canary; track κ with the judge
- **Slice metrics:** unanswerable, injection, long-tail entities —
  gaming often boosts the head
- **Outcome metrics:** refunds reversed, tickets reopened, incidents
- Judge prompt hash vs product prompt hash — if they co-evolve weekly,
  you are training on the test

## Fix

- Pin judge, pin gold, pin corpus generation
- Atomic, checkable scores (chunk id present, test suite green, SQL
  exact) before any 1–5 helpfulness
- Hold out a canary the product team cannot train on
- Separate owners: the person who changes the product prompt does not
  own the judge prompt
- Online metrics with teeth

## Eval of the eval

A meta-eval: take N production incidents, blind, and ask whether the
offline suite would have failed them. If not, the suite is a toy.

## Interview cue

When you propose LLM-as-judge, immediately say how it is calibrated
and what it **cannot** score. Interviewers are listening for whether
you have been burned, or whether you believe dashboards.
