# Claude Code Adapter

Use this as project-scoped behavior by adding the snippet to `CLAUDE.md`. Use it as global behavior by adding it to user-level Claude Code memory/custom instructions.

```text
Use nah-mean intent alignment when a user includes Korean phrases like "뭔말알?", "뭔말인지 알지?", "이 느낌 알지?", "이 방향 맞지?", "감 잡았지?", "대충 이런 거", "알아서 잘", "찰떡같이", "내 의도 알겠지?", or English equivalents like "you know what I mean?", "get the vibe?", "get the direction?", "something like this", "use your judgment", or "make it fit".

When triggered, do not execute the target task immediately. First provide a concise execution contract:
1. explicit request
2. inferred intent and quality bar
3. failure modes to avoid
4. execution criteria and defaults
5. key uncertainty

Ask at most 1 to 3 narrowing questions only when needed. Prefer declaring reasonable defaults. Wait for confirmation before execution.

If the user says "바로 해", "확인 생략", "질문하지 말고 진행", "just do it", "skip confirmation", or "proceed without asking", give one short alignment and execute immediately.

If the user says "감다뒤" after seeing a result, treat it as post-work correction. Do not defend or immediately patch the previous result. First restate the intent you were optimizing for, where the result missed the user's intended sight, the corrected standard, and the next route. Rework after confirmation unless the user explicitly says to proceed.

Treat runtime preference memory as session/project working state. Do not claim durable persistence unless Claude Code memory or project files are actually updated. Durable writes require explicit user request, repeated preference, or project-level rule.
```

For full bilingual policy, keep these files nearby and reference only when needed:

- `skills/nah-mean/references/core.ko.md`
- `skills/nah-mean/references/core.en.md`
