# Context rot

The working set filled with old turns, fat tool dumps, duplicate
chunks, and a summary of a summary. The instruction and the user
question were still *in* the window. The model behaved as if they
were not.

## Mechanism

Attention is finite and uneven. Long-context marketing hid this; it
did not repeal it.

Rot sources:

- Unbounded chat history
- Tool results appended forever
- RAG top-40 "just in case"
- Memory retrieval that dumps the whole profile
- Recursively summarized sessions that lost the number the user cares
  about, then treated the summary as truth

Prefill cost and TTFT also explode. Rot is a quality *and* a latency
incident.

## What it looks like

- Model follows an obsolete instruction from turn 4
- Ignores "answer in JSON" at the end because a tool dump in the middle
  contained a JSON-looking blob
- Coding agent edits the wrong file because the tree listing drowned
  the user's path
- "It got dumber after we added memory"

## Detection

- `tokens_in` p50/p95
- Fraction of prompt that is tool dumps vs instructions
- TTFT vs prompt size (should be a known curve)
- Ablation in replay: drop the middle 60%, does the answer improve?

## Fix

- Admission policy ([context](../topics/03-context.md))
- Hard caps per section (memory ≤ 800, tools ≤ 1500, rag ≤ 2k, …)
- Artifacts by reference
- Reset working memory on topic change (detected, or user "new chat")
- Do not store tool dumps in episodic memory

## Eval

Take a good short-context case. Sprinkle 20k tokens of plausible junk
in the middle. Score the drop. If the drop is large, your packer is
the bug, not the model.

## Interview cue

If you propose "just use the 1M window", you should immediately talk
about rot and prefill cost. That sentence is the difference between
junior and staff on this topic.
