# Agent loops

The while-loop kept calling tools, or kept "thinking", until the budget
you forgot to set met a vendor timeout. Or it looped a tight cycle:
search → open → search the same query — for forty minutes.

## Mechanism

Agents halt when **your runtime** says so. Models predict a stop token
sometimes. Sometimes they predict another tool call. Without:

- a max step count
- a max $ / tokens / ms
- a repeat detector on `(tool, args)`
- a verifier that can declare success

…the loop is unbounded. Retries layered on timeouts make it worse:
every 504 spawns a new loop with no memory of the last one.

## What it looks like

- A "research" job that files 400 search queries
- A coding agent that reruns tests, edits, reruns tests, on a flaky test
- Finance Slack: one tenant did $2k of tool calls overnight
- UX: spinner forever, then a truncated apology

## Detection

- `tool_calls_per_request` p95
- `duplicate_tool_call_rate`
- `$ / request` outliers
- span waterfalls that look like a sawtooth
- halt_reason enum: `success | user | budget | loop | policy` — if that
  enum does not exist, you cannot detect this

## Fix

- Budget object on every request ([request path](../topics/02-request-path.md))
- Loop detector: same tool+args twice → fail that path
- State hash: if working state did not change, stop
- Flaky tools: circuit breaker, do not retry in the model loop
- Checkpoints: persist artifacts so a *new* loop does not start from zero
- For irreversible tools: you should not be looping at all

## Eval

Tasks with **no solution** (impossible tickets). The agent must halt
and escalate, not search forever. Score `halt_reason=escalate` as
success. Score `steps > N` as fail even if it eventually lucks out.

## Interview cue

Draw the loop. Label halt. If you say "the agent just figures it out",
you have described the incident.
