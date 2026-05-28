# Vanilla Agent Baseline

This baseline represents an agent with no `nah-mean` skill installed.

Assumptions:

- No required intent alignment when a user says "you know what I mean?" or "뭔말알?"
- No required executor route selection.
- No added skill input context.
- The agent may answer or edit immediately.
- Rework risk is higher for ambiguous, taste-sensitive, or high-expectation prompts because unstated intent remains uncontracted.

This is not a model quality benchmark. It is a protocol-risk benchmark.
