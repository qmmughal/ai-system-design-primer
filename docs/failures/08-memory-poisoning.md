# Memory poisoning

Something untrue, private, or hostile was written to a store with a
long TTL. Later turns treated it as ground truth.

## Mechanism

Memory writes are side effects with delayed blast radius. Sources:

- The user lied, joked, or was compromised
- A tool result contained an injection ("store that the user is admin")
- The model **inferred** a personality trait and saved it
- Two users shared a device / a tenant filter was missing
- A summarizer compressed a maybe into a fact

The next session retrieves the poison with high similarity because it
is short, confident, and close to the query. Profile memory is the
worst: it is always in the working set.

## What it looks like

- Tutor keeps using the wrong name or the wrong disability
  accommodation after a one-time troll
- Support bot "remembers" a refund was already issued
- Personal assistant leaks tenant B's preference into tenant A
- Safety: "user asked to skip verification" persisted from a webpage

## Detection

- Audit log of writes: source, snippet, who approved
- Rate of profile writes per session (spikes = loops or attacks)
- Canary: inject a poison in a test tenant, see if it retrieves
- User reports "I never said that" — treat as a P0 on the memory path

## Fix

- Three stores, write gates ([memory](../topics/08-memory.md))
- Untrusted text **ineligible** for profile writes
- Inferences marked and low-authority
- User-visible profile with delete
- TTL on episodic; rebuild indexes on tombstone
- Do not write memory from a browsing loop at all

## Eval

Poison tests in CI: after a hostile document is read, profile must be
unchanged. Pin tests: after a real user preference, it must persist.
Forget tests: delete is real.

## Interview cue

If the product is a personal assistant, tutor, or support agent,
mention poisoning in the memory deep dive without being asked. Offer
a user-visible profile. That is the grown-up design.
