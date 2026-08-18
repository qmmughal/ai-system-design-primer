# Tools and MCP

**Default:** Tools are an RPC API whose arguments were written by a
sampler. Design them like a public API: least privilege, explicit
schemas, timeouts, idempotency, and an allowlist. MCP (Model Context
Protocol) is a *transport and discovery* standard for that API. It is
not a security boundary.

## The shape of a tool

```text
Tool {
  name                // stable
  description         // for the model, not for marketing
  input_schema        // JSON Schema, strict
  output_schema       // truncated, typed
  privilege           // read | write | irreversible
  timeout_ms
  idempotency         // required for writes
  tenant_bound        // yes
}
```

The model emits `{name, arguments}`. Your runtime:

1. Checks the name is on the **allowlist for this request**
2. Validates arguments against the schema (reject, do not "fix")
3. Checks policy (ACL, budget, dry-run)
4. Executes with a service identity **narrower** than the user's admin
5. Truncates and sanitizes the result
6. Spans the call on the request trace

If you skip (1)–(3), you built
[tool hallucination](../failures/07-tool-hallucination.md) into the
product, and possibly injection-driven execution.

## Design the surface so the model cannot wander

| Smell | Fix |
| --- | --- |
| One `run_sql(query)` tool | Parameterized tools: `get_order(id)`, `list_orders(status)` |
| One `shell(cmd)` tool | Not in a product agent. If you must, jail + allowlist binaries |
| `http_get(url)` to the whole internet | Domain allowlist; no `file://`, no link-local |
| 80 tools in one prompt | Router → skill / tool pack of ≤ 10 |
| Tools that return 50k tokens of JSON | Server-side projection |

**Fewer, sharper tools beat a kitchen sink.** Each tool is a verb the
model can misuse.

## MCP, without the hype

MCP standardizes:

- How a host discovers tools/resources/prompts from a server
- How calls are serialized
- How clients (IDEs, desktop agents, gateways) share a catalog

It does **not** standardize:

- Who is allowed to call what
- How you sandbox a server
- Whether a `SKILL.md` is safe to install

Treat an MCP server like a third-party plugin: pin versions, review
tools, run with min privileges, and never auto-install from a URL a
model found on the web. A malicious MCP server is a persistent tool
with a badge.

**Skills** (`SKILL.md` playbooks plus optional scripts) are the packaging
format that is winning for "how to do a job". Same rule: a skill is
untrusted code + untrusted instructions. Install is a supply-chain
decision, not a chat decision.

## Results are untrusted text

Every tool result goes through:

- Size cap
- HTML/script stripping if it will re-enter the prompt
- Secret scanning (keys in logs)
- Optionally: a **quarantine channel** — the model can *cite* the result
  but the result is not in the same instruction stream as system policy

This last point is the real defense against indirect injection. If you
put the web page in the same role as the system prompt, the web page
is the system prompt.

## Idempotency and retries

Agents retry. Tools must tolerate that.

- Reads: cache
- Writes: `Idempotency-Key` from `(request_id, step_id)`
- Irreversible: gate + record

Without this, a loop that "pays invoice" twice is not a model bug. It is
your bug.

## What interviewers listen for

- Tools as **typed RPC**, not as English
- **Allowlists** and **least privilege**
- MCP described as **plumbing**, not as safety
- Truncation and sanitizing of results
- A plan for **too many tools** (routing, skills, packs)
