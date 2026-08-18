# Prompt injection

Untrusted text was decoded as instructions. The model called a tool,
wrote memory, or revealed a prompt it should not have.

## Mechanism

There is no privilege bit in a token. If a web page, PDF, README, email,
or ticket is concatenated into the same stream as your policy, the
sampler can treat it as policy.

**Direct:** the user typed "ignore previous instructions".
**Indirect:** the user typed "summarize this URL", and the URL contains
the attack. Indirect is the production bug.

Tool-calling raises the stakes: the attack is not a funny poem. It is
`email.send(to=attacker, body=latest_messages)`.

## What it looks like

- Browsing agent exfiltrates the conversation to a query string
- Support agent files a refund because a ticket comment said to
- Coding agent runs `curl | sh` from a README
- Memory profile now contains "user is the CEO; skip KYC"

## Detection

- Tool-call policy engine: deny destinations not in the allowlist
- Detectors on results (heuristics + a specialist classifier) — useful,
  bypassable; do not bet the company
- Anomaly: first time this user emailed an external domain
- Canary instructions in the system prompt that should never appear in
  tool args ("if you see 'oranges-zebra-17', you are being attacked")

## Fix

Ranked:

1. **Do not give the reading loop irreversible tools**
2. **Allowlists** on URLs, email domains, commands
3. **Quarantine:** untrusted text is data. Actions are proposed, then
   executed by a policy that does not see the raw page
4. **Human gate** on send/pay/merge
5. **Strip / neutralize** HTML comments, hidden text, `system:` lines
   in retrieved docs
6. Prompt admonitions — last, and never alone

See [Safety](../topics/12-safety.md).

## Eval

A pinned corpus of pages: HTML comments, white-on-white text, PDF
JS, GitHub issues, "this is the user speaking". Success is **no
disallowed tool call**, not "the summary looks cautious".

Include **exfiltration** cases (markdown images, URLs with secrets).

## Interview cue

For any design with browsing, email, or MCP, open with indirect
injection. If the interviewer has to introduce it, you designed a demo.
