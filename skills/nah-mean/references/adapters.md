# Adapter Guide

Use this guide to port `nah-mean` behavior across agent frameworks without depending on one runtime.

## Portable Contract

Core behavior can live as:

- system prompt
- developer prompt
- skill file
- plugin instruction
- project memory rule
- agent policy module

Minimum portable fields:

```yaml
name: nah-mean
purpose: Lightly align user intent, then choose the smallest fitting executor route for ambiguous high-expectation requests.
triggers:
  korean:
    - "뭔말알?"
    - "뭔말인지 알지?"
    - "이 느낌 알지?"
    - "이 방향 맞지?"
    - "감 잡았지?"
    - "대충 이런 거"
    - "알아서 잘"
    - "알잘딱"
    - "찰떡같이"
    - "내 의도 알겠지?"
  english:
    - "you know what I mean?"
    - "get the vibe?"
    - "get the direction?"
    - "something like this"
    - "use your judgment"
    - "handle it cleanly"
    - "make it fit"
    - "you know my intent?"
default_mode: align_then_execute
executor_routes: [Direct, Edit, Build, Research, Design, QA, Safety Gate]
fast_mode_triggers:
  korean:
    - "바로 해"
    - "확인 생략"
    - "질문하지 말고 진행"
  english:
    - "just do it"
    - "skip confirmation"
    - "proceed without asking"
post_work_correction_triggers:
  korean:
    - "감다뒤"
memory_boundary: Runtime preference memory is separate from durable project memory.
```

## Generic Agent Prompt

Copy this into any agent framework:

```text
When a user request includes "뭔말알?", "뭔말인지 알지?", "이 느낌 알지?", "이 방향 맞지?", "감 잡았지?", "대충 이런 거", "알아서 잘", "알잘딱", "찰떡같이", "내 의도 알겠지?", or English equivalents like "you know what I mean?", "get the vibe?", "get the direction?", "something like this", "use your judgment", "handle it cleanly", or "make it fit", do not execute immediately.

First create a lightweight intent read:
1. Identify the explicit request and inferred quality bar.
2. Name likely failure modes and key uncertainty.
3. Declare execution criteria and default assumptions.
4. Choose a route: Direct, Edit, Build, Research, Design, QA, or Safety Gate.

Then wait for confirmation before execution.

If the user says "바로 해", "확인 생략", "질문하지 말고 진행", "just do it", "skip confirmation", or "proceed without asking", give a one-sentence alignment, choose the route, and execute immediately.

If the user says "감다뒤" after seeing the result, treat it as a post-work correction trigger. Do not defend the previous result or immediately patch it. First restate the intent you thought you were optimizing for, name where the result missed the user's intended sight, propose a corrected execution standard and route, then wait for confirmation before rework unless the user explicitly says to proceed.

Maintain runtime preference memory from corrections, but do not claim durable persistence unless the framework provides it. Durable memory or wiki writes require explicit user request, repeated preference, or project-level rule.
```

## Codex Skill Adapter

Install as a global skill folder:

```text
${CODEX_HOME:-~/.codex}/skills/nah-mean/
```

Required files:

```text
SKILL.md
agents/openai.yaml
references/core.ko.md
references/core.en.md
references/adapters.md
```

Codex trigger quality depends mainly on `SKILL.md` frontmatter `description`. Keep trigger phrases and task categories in that field.

## Claude Code Adapter

Use one of these patterns:

- Put portable contract in project `CLAUDE.md` for project-scoped behavior.
- Put portable contract in user-level memory or custom instruction for global behavior.
- Keep full contracts as separate markdown files and reference them from `CLAUDE.md` if context cost matters.

Suggested project snippet:

```text
Use nah-mean intent alignment when a user ends a request with "뭔말알?", "you know what I mean?", "get the vibe?", or similar phrases. First give a compact intent read, failure risk, execution standard, and route. Ask at most 1 to 3 narrowing questions. Wait for confirmation unless the user says to proceed without asking.
```

## Hermes-Like or Unknown Agent Adapter

Assume no framework-specific APIs. Use generic prompt form.

Implementation shape:

- one global instruction block for trigger and behavior
- optional runtime preference object if the agent supports session state
- optional durable memory hooks only if explicit memory APIs exist
- no dependency on wiki, MCP, file tools, or browser tools

If the agent has tool routing, add this rule:

```text
Do not call tools for the target task until alignment completes, except for reading durable preference memory when framework policy requires it.
```

## Evaluation Checklist

Given a triggered request, a compliant agent should:

- not execute target work immediately
- give a compact intent read instead of a long plan
- name what to avoid and what standard to use
- choose a fitting executor route
- expose key uncertainty
- ask no more than 1 to 3 questions
- wait for confirmation unless fast mode is triggered
- handle "감다뒤" as a post-work correction trigger, not a pre-execution trigger
- realign original intent, missed sight, corrected standard, and route before rework
- preserve current instruction over old memory
- not claim durable memory without a real storage mechanism

## Minimal Test Prompts

Korean:

```text
이 레포 분석해서 어떤 오픈소스인지 설명해줘. 뭔말알?
```

Expected behavior: align around practical adoption judgment, not README summary.

English:

```text
Make this landing page feel more premium and less generic. You know what I mean?
```

Expected behavior: align around design direction, clichés to avoid, target impression, and execution criteria before editing.

Fast mode:

```text
이 기준으로 문서 정리해. 질문하지 말고 진행. 뭔말알?
```

Expected behavior: one short inline alignment, then execute.

Post-work correction:

```text
감다뒤
```

Expected behavior: restate the previous intended direction, identify where the result missed the user's intended sight, propose a corrected standard and route, then wait before rework unless fast rework is requested.
