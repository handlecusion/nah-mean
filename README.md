# nah-mean

Portable intent alignment skill for ambiguous, taste-sensitive, or high-expectation requests.

Use it when a user says things like `뭔말알?`, `이 느낌 알지?`, `알아서 잘`, `you know what I mean?`, `get the vibe?`, or `use your judgment`. Agent first aligns intent, then executes after confirmation unless fast mode is requested.

## What This Repo Contains

```text
.
├── install.sh                  # Install Codex global skill
├── manifest.json               # Portable entrypoint map
├── skills/nah-mean/            # Codex skill package
├── prompts/                    # Copy-paste prompts for generic agents
└── adapters/                   # Framework-specific install notes
```

## Install

Pick the path that matches your agent.

### Recommended Paths

| Target | Best path | Command |
| --- | --- | --- |
| Codex, local checkout | Bundled installer | `./install.sh` |
| Codex, from GitHub | GitHub CLI | `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user` |
| Claude Code, from GitHub | `gh skill` or `skills` CLI | `gh skill install handlecusion/nah-mean nah-mean --agent claude-code --scope user` |
| Agent Skills-compatible clients | `skills` CLI | `npx skills add handlecusion/nah-mean --skill nah-mean -a <agent> -g -y` |
| Any prompt-only agent | Copy prompt | `prompts/nah-mean.ko.md` or `prompts/nah-mean.en.md` |

### Codex

```bash
./install.sh
```

Manual install:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/nah-mean "${CODEX_HOME:-$HOME/.codex}/skills/nah-mean"
```

Install from a published GitHub repo with the `skills` CLI:

```bash
npx skills add handlecusion/nah-mean --list
npx skills add handlecusion/nah-mean --skill nah-mean -a codex -g -y
```

Note: current `skills` CLI may place Codex global installs under `~/.agents/skills`. Use this path only when your Codex build scans that directory. For Codex builds that use `~/.codex/skills`, prefer `./install.sh` or `gh skill install ... --agent codex --scope user`.

Install directly from the skill path:

```bash
npx skills add https://github.com/handlecusion/nah-mean/tree/main/skills/nah-mean -a codex -g -y
```

Install from GitHub with `gh`:

```bash
gh skill preview handlecusion/nah-mean nah-mean
gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user
```

### Claude Code

Use [adapters/claude-code.md](adapters/claude-code.md). Put the provided snippet in user memory or project `CLAUDE.md`.

If your `gh` version supports agent skills:

```bash
gh skill preview handlecusion/nah-mean nah-mean
gh skill install handlecusion/nah-mean nah-mean --agent claude-code --scope user
```

Pin a version when using a tagged release:

```bash
gh skill install handlecusion/nah-mean nah-mean@v0.1.0 --agent claude-code --scope user
```

### Generic Agents

Use one of:

- [prompts/nah-mean.ko.md](prompts/nah-mean.ko.md)
- [prompts/nah-mean.en.md](prompts/nah-mean.en.md)
- [adapters/generic-agent.md](adapters/generic-agent.md)

### Hermes-Like Agents

Use [adapters/hermes-like.md](adapters/hermes-like.md). It assumes no special API and no durable memory unless the runtime provides one.

## Distribution Model

This repo follows current high-signal agent-skill distribution patterns:

- Skill-first layout: `skills/nah-mean/SKILL.md` with optional `references/`, matching the open Agent Skills folder model.
- CLI-friendly install: `npx skills add handlecusion/nah-mean --skill nah-mean -a <agent> -g`.
- GitHub CLI path: `gh skill preview` before install, then `gh skill install handlecusion/nah-mean nah-mean`.
- Local fallback: clone repo, inspect files, run `./install.sh`.
- Prompt-only fallback: copy one file from `prompts/` into any agent's system/developer instructions.

Why this shape:

- Large skill collections expose a `skills/` directory and install selected skills instead of forcing all content into the agent.
- `skills` CLI supports GitHub shorthand, full URLs, direct skill paths, local paths, agent targeting, global/project scope, listing, update, and non-interactive installs.
- GitHub CLI supports preview, install, version pinning, custom directories, local install, and update flows for agent skills.
- Local installers are still useful when users do not have Node.js, `npx`, or a skill-aware CLI.

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

This skill has no executable scripts. It is instruction/reference content only.

## Update

Local checkout:

```bash
git pull
./install.sh
```

`skills` CLI:

```bash
npx skills check
npx skills update nah-mean
```

GitHub CLI:

```bash
gh skill update nah-mean
```

For reproducibility, prefer tagged releases:

```bash
gh skill install handlecusion/nah-mean nah-mean@v0.1.0 --agent claude-code --scope user
```

## Publish Checklist

Before publishing:

1. Tag a release such as `v0.1.0`.
2. Run validation commands in [Validate](#validate).
3. Confirm `skills/nah-mean` matches the installed global Codex copy if you maintain both.
4. Confirm prompt-only adapters still match the core skill behavior.
5. Add the repo to any marketplace or index only after the install commands work from GitHub.

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

- Korean: `바로 해`, `확인 생략`, `질문하지 말고 진행`
- English: `just do it`, `skip confirmation`, `proceed without asking`

Fast mode gives one short alignment, then executes.

## Memory Boundary

Runtime preference memory is not durable storage. Durable memory or wiki writes require explicit user request, repeated preference, or project-level rule. Current user instructions override older memory.

## Validate

Codex skill validation:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/nah-mean
```

If `PyYAML` is missing, install it in a virtualenv or temporary target and set `PYTHONPATH`.

Shell syntax:

```bash
bash -n install.sh
```

Local install smoke tests:

```bash
tmp_home="$(mktemp -d)"
HOME="$tmp_home" gh skill install . nah-mean --from-local --agent codex --scope user --force
test -f "$tmp_home/.codex/skills/nah-mean/SKILL.md"
```

```bash
tmp_home="$(mktemp -d)"
HOME="$tmp_home" npx --yes skills add . --skill nah-mean -a codex -g -y --copy
test -f "$tmp_home/.agents/skills/nah-mean/SKILL.md"
```
