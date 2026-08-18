# Cost blowups

The product worked in the demo. The bill is a multiple of the model
card you showed finance. Nobody changed the price. The loop did.

## Mechanism

Cost is `Σ (in + out + tools) × retries × users`. People estimate
`in + out` for a single happy path.

Multipliers that hide in the design:

- **Output tokens:** hidden reasoning, chatty agents, "write a report"
- **Retries:** validator fail → repair; judge fail → escalate; 429 →
  retry the *large* model
- **Tools:** each result re-enters as future `tokens_in`
- **Prefill without cache:** unique giant prompts
- **Fan-out:** multi-agent, or map-reduce over 200 chunks
- **Training-eval leakage into prod:** temperature > 0 "for quality"
  on an extractor that should be 0 and cached

## What it looks like

- Unit economics: $0.12 / chat on a product that charges $0.00
- One "research" button that launches 30 L-model calls
- A weekend spike from a crawler hitting `/complete`
- Prefix cache hit rate 5% after a "minor" prompt tweak that put a
  UUID at the top

## Detection

- `$ / request` and `$ / successful_task` (the second is the real one)
- tokens_out, tool_calls, retries, cache_hit — **split**
- Per-tenant budgets with pages
- Alert on p99 $ as well as p50 (loops live in the tail)

## Fix

- Budget object, hard stop
- Router: S first, L once
- max_tokens appropriate to the product
- Prefix-cache hygiene ([gateways](../topics/13-gateways.md))
- Cache extractors
- Don't multi-agent a FAQ
- Auth and quotas on the gateway so the public cannot light money on fire

## Eval

A **cost eval**: the same gold set scored with a dollar ceiling.
A change that +4% quality and +80% $ is a fail unless the product
asked for that.

## Interview cue

Put `$ / day` on the board in the first ten minutes. If the design has
an agent, multiply by steps. Interviewers are hiring you to not be
surprised by the bill.
