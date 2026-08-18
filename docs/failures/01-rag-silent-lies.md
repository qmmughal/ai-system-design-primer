# RAG silent lies

The model answered. The chunk was wrong, missing, or unread. The prose
was excellent.

## Mechanism

Generation is trained to continue. Retrieval is a search problem. When
you concatenate "here are some maybe-related paragraphs" with "be a
helpful assistant", the decoder will **fill gaps**. Users hear a fact.
You logged a 200.

Common sub-mechanisms:

- **Miss:** the right chunk never made top-k (chunking, ACLs, query
  mismatch)
- **Misfire:** a nearby-looking chunk ranked higher (same product name,
  old policy version)
- **Unread:** the chunk was in the prompt middle and lost-in-the-middle
  ate it
- **Over-generate:** the chunk had half the answer; the model supplied
  the rest from pretraining

## What it looks like

- Support bot cites "§4 refunds" for a plan that has no refunds
- Internal Q&A invents an on-call rotation
- Legal assistant quotes a case that does not exist, or exists and says
  the opposite
- Thumbs-up stay high. The incident is a downstream human who trusted it

## Detection

You will not see this in HTTP error rates.

- **Citation coverage:** percent of claims with a chunk id
- **Groundedness verifier:** claim embedding / NLI against cited chunks
- **Retrieval debug:** for labeled questions, is `gold_chunk_id` in
  top-k?
- **Trace:** `chunk_ids`, scores, `index_id`. Silent lies with score
  0.11 are a product decision, not a mystery

## Fix

In order:

1. **Cite-or-refuse** in code, not in the prompt
2. Hybrid search + rerank so the right chunk is actually present
3. Put evidence next to the question; drop extra chunks rather than
   stuffing 40
4. Verifier fails → one retrieve-again or a refusal
5. Show citations in the UI so users can catch what evals miss

Do not "add chain-of-thought". That writes a longer lie.

## Eval

A set of questions whose gold answers are **chunk ids**, not just
strings. Score recall@k separately from answer correctness. Include
**unanswerable** questions; the only correct behavior is refuse.

## Interview cue

When the prompt is RAG, mention silent lies in the first architecture
pass: a refuse path and a verifier box. Wait until asked, and the
interviewer will ask "what if retrieval is wrong?" — you wanted to be
there already.
