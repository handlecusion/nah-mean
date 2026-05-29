---
name: nah-mean
description: Lightweight intent alignment and context-fit execution dispatch for ambiguous or high-expectation requests. Use when a user says Korean triggers like "뭔말알?", "뭔말인지 알지?", "이 느낌 알지?", "이 방향 맞지?", "감 잡았지?", "대충 이런 거", "알아서 잘", "알잘딱", "찰떡같이", "내 의도 알겠지?", or English equivalents like "you know what I mean?", "get the vibe?", "you get the direction?", "make it fit", "use your judgment", "handle it cleanly", "you know the intent?", especially for design, writing, research, planning, prompt/agent design, code structure, automation workflows, presentations, business plans, and other work where executing immediately risks rework. Also use when a Korean user says "감다뒤" after work to restate the original intent and realign the shared sight before rework.
---

# Nah Mean

Use this skill in three gears:

- **Nah-Mean**: lightweight intent read before execution. This is not a full plan.
- **Aljalttak**: choose the smallest fitting executor route after confirmation or fast-mode trigger.
- **Gamdadwi**: post-work correction recovery when the user disliked the result and wants the agent to realign intent before rework.

## Core Behavior

When triggered, do not execute target work immediately unless the user asks for fast execution with phrases like "바로 해", "확인 생략", "질문하지 말고 진행", "just do it", "skip confirmation", or "proceed without asking".

Default mode:

1. Give a compact Nah-Mean read: intent, risk, execution standard.
2. Ask at most 1 to 3 narrowing questions only when the default would be risky.
3. Wait for confirmation.
4. Use Aljalttak dispatch to choose the executor route and then execute.

Fast mode:

1. Give one short Nah-Mean read.
2. Pick an Aljalttak executor route.
3. Execute immediately.

Post-work correction mode:

When the user says "감다뒤" after seeing a result, treat it as a correction trigger, not as a new pre-execution alignment trigger.

1. Do not defend the previous result or patch immediately.
2. Restate the intent you thought you were optimizing for.
3. Name where the result likely missed the user's intended sight.
4. Propose the corrected execution standard and Aljalttak route.
5. Rework only after the user confirms, unless they explicitly tell you to proceed.

## Aljalttak Dispatch

After alignment, pick one route. Keep it implicit unless naming it helps the user.

| Route | Use when |
| --- | --- |
| Direct | answer or rewrite can be done without tools |
| Edit | files need small scoped changes |
| Build | multi-file implementation or structured artifact creation |
| Research | current facts, sources, or external comparison matter |
| Design | UI/visual/product taste is central |
| QA | user asks whether it works, or proof is needed |
| Safety Gate | destructive, security, legal, financial, or deployment risk needs explicit confirmation |

## Response Shape

Use Korean when the user writes Korean. Use English when the user writes English. For mixed input, match the user's dominant language.

Short Korean shape:

```text
뭔말알.
의도: ...
주의: ...
기준: ...
알잘딱 route: ...

이 기준으로 진행하면 된다.
```

Short Korean correction shape:

```text
감다뒤 인식.
내가 잡았던 의도: ...
어긋난 지점: ...
다시 맞출 sight: ...
재작업 기준: ...
알잘딱 route: ...

이 기준으로 다시 잡으면 된다.
```

Short English shape:

```text
Got it.
Intent: ...
Watchout: ...
Standard: ...
Route: ...

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
