---
name: nah-mean
description: Intent alignment layer for ambiguous or high-expectation requests before execution. Use when a user says Korean triggers like "뭔말알?", "뭔말인지 알지?", "이 느낌 알지?", "이 방향 맞지?", "감 잡았지?", "대충 이런 거", "알아서 잘", "찰떡같이", "내 의도 알겠지?", or English equivalents like "you know what I mean?", "get the vibe?", "you get the direction?", "make it fit", "use your judgment", "you know the intent?", especially for design, writing, research, planning, prompt/agent design, code structure, automation workflows, presentations, business plans, and other work where executing immediately risks rework.
---

# Nah Mean

Use this skill to create an execution contract before doing ambiguous, taste-sensitive, or high-quality work.

## Core Behavior

When triggered, do not immediately execute unless the user explicitly asks for fast execution with phrases like "바로 해", "확인 생략", "질문하지 말고 진행", "just do it", "skip confirmation", or "proceed without asking".

Default mode:

1. State what you believe the user wants.
2. Separate explicit request from inferred intent.
3. Name likely failure modes.
4. Declare execution criteria and defaults.
5. Ask at most 1 to 3 narrowing questions only when needed.
6. Wait for confirmation before execution.

Fast mode:

1. Give one short inline alignment.
2. Execute immediately.

## Response Shape

Use Korean when the user writes Korean. Use English when the user writes English. For mixed input, match the user's dominant language.

Short Korean shape:

```text
뭔말알.
내가 이해한 방향:
- ...
- ...

피할 것:
- ...
- ...

실행 기준:
- ...
- ...

이 기준으로 진행하면 된다.
```

Short English shape:

```text
Got it.
My read:
- ...
- ...

Avoid:
- ...
- ...

Execution criteria:
- ...
- ...

If this is right, I will proceed on this basis.
```

## Memory Boundary

Maintain preference memory inside the current conversation when possible. Treat it as runtime personalization, not guaranteed durable storage.

Use durable memory or wiki tools only when available and appropriate:

- Query long-term project or user context when project instructions call for it.
- Do not write durable memory for one-off taste, uncertain inference, or rejected assumptions.
- Write durable memory only when the user explicitly asks, a preference repeats, or project-level rules require persistence.
- Current user instructions override older memory.

## Reference Files

Read only what is needed:

- `references/core.ko.md`: full Korean contract and examples.
- `references/core.en.md`: full English contract and examples.
- `references/adapters.md`: portable guidance for Codex, Claude Code, Hermes-like, and generic agent frameworks.
