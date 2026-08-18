# Tool hallucination

The model invented a tool, invented arguments, skipped a tool it
needed, or announced it had called a tool it had not.

## Mechanism

Tool use is just more tokens, usually in a JSON channel. Samplers:

- **Invent names** (`crm.search_v2`) when the schema is long or similar
- **Invent ids** (`order_id: 12345`) that look right
- **Skip the call** and answer from pretraining ("your flight is on
  time")
- **Confabulate success** ("I sent the email") because that is a common
  continuation

Retries and sloppy parsers make it worse: `json.loads` fails, you
regex out something that looks like an id, you execute it.

## What it looks like

- CRM 404 storms on sequential ids
- "I refunded you" with no refund row
- SQL tools with `DROP` in a comment the model thought was clever
- Tests pass in the agent's narrative; CI never ran

## Detection

- Gateway: unknown tool name rate
- Schema validation fail rate
- **Effect vs claim:** if the model says it sent mail, there must be a
  span. A verifier compares the narrative to the trace (this is an
  eval you can run offline on fixtures)
- Downstream 4xx on tools

## Fix

- Strict JSON schema, constrained decode if available
- Allowlist; unknown name is a runtime error, not a best-effort
- **Do not execute** until validate
- For facts that live in tools, **cite-or-refuse** applies: no tool
  span, no claim
- Idempotency keys so invented retries do not double-apply
- Reduce the tool catalog so names are not a soup

## Eval

Golden traces: given a user question, the **sequence of tool names and
argument shapes** is the label. Score exact match on names, and
validators on args. Include "must not call" cases (small talk, jailbreak).

## Interview cue

Say "the model does not call tools; the runtime does, after validation."
Then show what happens on invalid JSON. That sentence carries a lot of
level.
