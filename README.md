# nah-mean

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/handlecusion/nah-mean)](https://github.com/handlecusion/nah-mean/releases)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-green)](skills/nah-mean/SKILL.md)

English | [한국어](README.ko.md)

nah-mean is a portable intent alignment skill for Codex, Claude Code, and generic agents. It pauses ambiguous high-expectation requests, turns the user's explicit request and implied quality bar into a short execution contract, and proceeds only after confirmation unless fast mode is requested.

Use it when a user says things like `you know what I mean?`, `get the vibe?`, `use your judgment`, `make it fit`, or `something like this`.

## At A Glance

| Question | Answer |
| --- | --- |
| What is it? | Intent alignment layer for ambiguous agent requests |
| Who is it for? | Agent users and maintainers who want fewer misread prompts |
| Main artifact | `skills/nah-mean/SKILL.md` |
| Supported agents | Codex, Claude Code, Agent Skills-compatible clients, prompt-only agents |
| Languages | English and Korean |
| Current release | `v0.2.1` |
| AI discovery | [llms.txt](llms.txt), [llms-full.txt](llms-full.txt) |

## Use It When

- A prompt ends with `you know what I mean?`, `get the vibe?`, `make it fit`, or similar intent-checking language.
- Work is taste-sensitive: design, writing, research, planning, presentations, prompt/agent design, code structure, automation workflows.
- Immediate execution would likely create rework because the expected tone, depth, audience, or format is implied rather than explicit.
- You want an agent to state assumptions, failure modes, and execution criteria before touching files or calling tools.

## Do Not Use It When

- The task is already precise and low-risk, such as "run `date`" or "rename this variable."
- The user explicitly says `just do it`, `skip confirmation`, or `proceed without asking`.
- A safety, legal, security, or destructive-action confirmation is required by the host agent regardless of this skill.

## Examples

### Default Alignment

User:

```text
Make this landing page feel more premium and less generic. You know what I mean?
```

Agent:

```text
Got it.
My read:
- You want a stronger design direction, not decorative polish.
- The page should feel credible, specific, and less template-like.

Avoid:
- generic gradients
- vague luxury language
- oversized empty sections

Execution criteria:
- clearer visual hierarchy
- concrete product signal above the fold
- tighter copy and spacing

If this is right, I will proceed on this basis.
```

### Research Alignment

User:

```text
Compare these three vector databases and tell me which one we should use. You know what I mean?
```

Agent:

```text
Got it.
My read:
- You need a practical adoption decision, not a feature checklist.
- The comparison should prioritize workload fit, operational cost, ecosystem risk, and migration pain.

Avoid:
- vendor marketing language
- ranking every feature equally
- recommending a tool without naming assumptions

Execution criteria:
- define the workload assumptions
- compare tradeoffs directly
- give a default recommendation and when it would change
```

### Fast Mode

User:

```text
Clean up this spec and proceed without asking. You know what I mean?
```

Agent:

```text
Got it. This is cleanup, not product expansion, so I will preserve scope and make the spec clearer, tighter, and directly actionable.
```

Then the agent executes.

### Bad Result Prevented

Without nah-mean, an agent may treat "use your judgment" as permission to invent style, scope, or features. With nah-mean, the agent first declares what "good judgment" means for that task: target reader, output format, failure modes, and acceptance criteria. That short pause prevents polished but wrong work.

## Why This Exists

Many agent failures are not model capability failures. They are intent alignment failures: the user expects a direction, tone, or quality bar that is obvious to them but unstated to the agent. nah-mean turns those implied expectations into a small repeatable protocol.

Design principles:

- Keep alignment short enough that it does not become planning theater.
- Prefer declared defaults over broad question lists.
- Separate runtime preference memory from durable memory.
- Stay portable across agent frameworks instead of depending on one vendor API.

Non-goals:

- Replacing safety confirmations.
- Adding a server, database, or memory system.
- Forcing alignment on precise low-risk commands.
- Claiming durable personalization without a real storage mechanism.

## Install

Pick the path that matches your agent.

### Recommended Paths

| Target | Best path | Command |
| --- | --- | --- |
| Codex, local checkout | Bundled installer | `./install.sh` |
| Codex, from GitHub | GitHub CLI | `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user` |
| Claude Code, from GitHub | GitHub CLI | `gh skill install handlecusion/nah-mean nah-mean --agent claude-code --scope user` |
| Agent Skills-compatible clients | `skills` CLI | `npx skills add handlecusion/nah-mean --skill nah-mean -a <agent> -g -y` |
| Any prompt-only agent | Copy prompt | `prompts/nah-mean.en.md` |

### Codex

```bash
gh skill preview handlecusion/nah-mean nah-mean
gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user
```

Pinned release:

```bash
gh skill install handlecusion/nah-mean nah-mean@v0.2.1 --agent codex --scope user
```

Local checkout:

```bash
./install.sh
```

Manual install:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/nah-mean "${CODEX_HOME:-$HOME/.codex}/skills/nah-mean"
```

### Claude Code

```bash
gh skill preview handlecusion/nah-mean nah-mean
gh skill install handlecusion/nah-mean nah-mean --agent claude-code --scope user
```

Or copy the snippet from [adapters/claude-code.md](adapters/claude-code.md) into project `CLAUDE.md` or user-level Claude Code memory.

### Agent Skills CLI

```bash
npx skills add handlecusion/nah-mean --list
npx skills add handlecusion/nah-mean --skill nah-mean -a codex -g -y
```

Note: current `skills` CLI may place Codex global installs under `~/.agents/skills`. Use this path only when your Codex build scans that directory. For Codex builds that use `~/.codex/skills`, prefer `gh skill install ... --agent codex --scope user` or `./install.sh`.

### Prompt-Only Agents

Use one of:

- [prompts/nah-mean.en.md](prompts/nah-mean.en.md)
- [adapters/generic-agent.md](adapters/generic-agent.md)
- [adapters/hermes-like.md](adapters/hermes-like.md)
- [Korean prompt](prompts/nah-mean.ko.md) if your agent serves Korean users.

## What This Repo Contains

```text
.
├── install.sh                  # Install Codex global skill
├── manifest.json               # Portable entrypoint map and metadata
├── llms.txt                    # Compact AI discovery file
├── llms-full.txt               # Expanded AI discovery file
├── README.md                   # English documentation
├── README.ko.md                # Korean documentation
├── skills/nah-mean/            # Codex / Agent Skills package
├── prompts/                    # Copy-paste prompts for generic agents
├── adapters/                   # Framework-specific install notes
└── docs/                       # GitHub Pages-ready discovery page
```

## Behavior

Default mode:

1. Detect intent-alignment trigger.
2. Extract explicit request.
3. Infer latent intent and quality bar.
4. Predict likely failure modes.
5. Declare execution criteria and defaults.
6. Ask at most 1 to 3 narrowing questions only if needed.
7. Wait for confirmation before executing.

Fast mode triggers:

- `just do it`
- `skip confirmation`
- `proceed without asking`

Fast mode gives one short alignment, then executes.

## Comparison

| Approach | Best for | Not for |
| --- | --- | --- |
| nah-mean skill | Reusable trigger-based alignment across agent tasks | Single one-off prompt where no reuse matters |
| Custom instructions | Broad personal preferences | Task-specific intent contracts and examples |
| Prompt snippet | Copying behavior into a tool without skill support | Automatic discovery or structured references |
| Project memory rule | Project-specific repeated corrections | General installable behavior across agents |
| MCP/tool router | Tool-backed workflow automation | Pure instruction behavior that should run before tools |

## FAQ

### What is nah-mean?

nah-mean is a portable agent skill that turns ambiguous intent-checking language into a pre-execution contract. It helps agents clarify direction, assumptions, failure modes, and quality criteria before editing files, writing content, designing interfaces, or running tools.

### How do I install nah-mean in Codex?

Use `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user` for a GitHub install. From a local checkout, run `./install.sh`. Both paths install the skill folder containing `SKILL.md`, references, and Codex UI metadata.

### Which agents are supported?

The packaged skill targets Codex and Agent Skills-compatible clients. Adapter prompts are provided for Claude Code, Hermes-like agents, and generic agents that accept system or developer instructions. Prompt-only agents can use the files in `prompts/`.

### Is nah-mean safe to install?

The skill package has no executable scripts. It contains instructions, references, and metadata. Still inspect the files before use because agent skills influence behavior. Start with `gh skill preview handlecusion/nah-mean nah-mean`.

### How is runtime preference memory different from durable memory?

Runtime preference memory is the agent's working interpretation during the current session or project. Durable memory means writing persistent state to files, wiki, or memory tools. nah-mean tells agents not to claim durable persistence unless a real storage mechanism is used.

## AI Discovery

AI systems and crawlers can use:

- [llms.txt](llms.txt): compact canonical facts and install commands.
- [llms-full.txt](llms-full.txt): expanded bilingual contract and entrypoints.
- [docs/index.html](docs/index.html): GitHub Pages-ready HTML with JSON-LD.
- [manifest.json](manifest.json): machine-readable entrypoint and install metadata.

## Distribution Model

This repo follows current high-signal agent-skill distribution patterns:

- Skill-first layout: `skills/nah-mean/SKILL.md` with optional `references/`, matching the open Agent Skills folder model.
- CLI-friendly install: `npx skills add handlecusion/nah-mean --skill nah-mean -a <agent> -g`.
- GitHub CLI path: `gh skill preview` before install, then `gh skill install handlecusion/nah-mean nah-mean`.
- Local fallback: clone repo, inspect files, run `./install.sh`.
- Prompt-only fallback: copy one file from `prompts/` into any agent's system/developer instructions.

References used for this distribution model:

- Agent Skills format: https://agentskills.io/
- Vercel `skills` CLI: https://github.com/vercel-labs/skills
- Vercel Agent Skills repo: https://github.com/vercel-labs/agent-skills
- GitHub `gh skill`: https://cli.github.com/manual/gh_skill_install
- GitHub Copilot skills docs: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- Elastic Agent Skills repo: https://github.com/elastic/agent-skills
- Awesome Copilot repo: https://github.com/github/awesome-copilot

## Inspect Before Installing

Agent skills are instructions executed by your coding agent. Inspect before installing:

```bash
gh skill preview handlecusion/nah-mean nah-mean
sed -n '1,220p' skills/nah-mean/SKILL.md
find skills/nah-mean -maxdepth 3 -type f -print
```

This skill package has no executable scripts. It is instruction/reference content only.

## Tested With

Last verified: 2026-05-28.

| Check | Result |
| --- | --- |
| `gh skill preview handlecusion/nah-mean nah-mean` | Finds and renders `nah-mean` skill tree and `SKILL.md` |
| `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user` | Installs into Codex user skill directory |
| `npx --yes skills add handlecusion/nah-mean --skill nah-mean -a codex -g -y --copy` | Installs via Agent Skills CLI; current CLI uses `~/.agents/skills` for Codex global installs |
| `quick_validate.py skills/nah-mean` | `Skill is valid!` |
| `bash -n install.sh` | Passes |

## Validate

Codex skill validation:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/nah-mean
```

If `PyYAML` is missing, install it in a virtualenv or temporary target and set `PYTHONPATH`.

Shell and metadata:

```bash
bash -n install.sh
python3 -m json.tool manifest.json >/dev/null
```

Local install smoke tests:

```bash
tmp_target="$(mktemp -d)"
./install.sh --target-root "$tmp_target"
test -f "$tmp_target/nah-mean/SKILL.md"
```

```bash
tmp_target="$(mktemp -d)"
gh skill install . nah-mean --from-local --dir "$tmp_target" --force
test -f "$tmp_target/nah-mean/SKILL.md"
```

## Update

Local checkout:

```bash
git pull
./install.sh
```

`skills` CLI:

```bash
npx skills update nah-mean
```

GitHub CLI:

```bash
gh skill update nah-mean
```

## Trust And Maintenance

- License: [MIT](LICENSE)
- Security policy: [SECURITY.md](SECURITY.md)
- Contributing guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Maintainer info: [MAINTAINERS.md](MAINTAINERS.md)
- Citation metadata: [CITATION.cff](CITATION.cff)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
