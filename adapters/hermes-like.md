# Hermes-Like Adapter

Use this for agent frameworks with unknown plugin shape. Assume generic prompt injection, optional session state, and no durable memory by default.

## Runtime Shape

```yaml
module: nah-mean
type: intent-alignment
default_mode: align_then_execute
fast_mode: inline_alignment_execute
state:
  runtime_preferences: optional
  durable_memory: optional_if_framework_supports_it
tools:
  target_task_tools: blocked_until_alignment_confirmed
```

## Instruction Block

```text
Install nah-mean as an intent alignment layer. When trigger phrases appear, pause target-task execution and produce an execution contract. Trigger phrases include Korean "뭔말알?", "뭔말인지 알지?", "이 느낌 알지?", "이 방향 맞지?", "알아서 잘", and English "you know what I mean?", "get the vibe?", "get the direction?", "use your judgment", "make it fit".

Execution contract must include explicit request, inferred intent, failure modes, execution criteria, defaults, and key uncertainty. Ask at most 1 to 3 narrowing questions. Wait for confirmation unless fast mode is requested.

Fast mode triggers include "바로 해", "확인 생략", "질문하지 말고 진행", "just do it", "skip confirmation", and "proceed without asking". In fast mode, state one short alignment and execute.

Post-work correction trigger includes Korean "감다뒤". When it appears after a result, restate the intent being optimized, name where the result missed the user's intended sight, propose the corrected standard and route, then wait before rework unless the user explicitly says to proceed.

Positive alignment feedback trigger includes Korean "감다살". When it appears after alignment or a result, restate the intent or standard that matched, reinforce that preference in runtime state, and do not claim durable memory unless durable storage is updated.

Do not call target-task tools before alignment completes. Reading durable preferences is allowed only if the framework provides such storage and policy allows it.
```

## Porting Notes

- If framework has plugin manifests, map `manifest.json` entrypoints to plugin resources.
- If framework has only prompt memory, use `prompts/nah-mean.ko.md` or `prompts/nah-mean.en.md`.
- If framework has durable memory, store only explicit or repeated preferences.
- If framework has no durable memory, keep corrections in session state only.
