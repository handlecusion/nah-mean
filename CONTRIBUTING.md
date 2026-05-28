# Contributing

Contributions should keep nah-mean portable across agent frameworks.

## Good Contributions

- Clearer trigger phrases in Korean or English.
- Better examples showing alignment before execution.
- Adapter improvements for Codex, Claude Code, Hermes-like agents, and generic agents.
- Documentation that improves safety, install clarity, or AI discoverability.
- Tests or validation notes for `gh skill`, `npx skills`, and Codex skill validation.

## Avoid

- Adding runtime dependencies without a clear need.
- Adding executable scripts to the skill package unless the security model is documented.
- Claiming durable memory behavior without an actual storage mechanism.
- Making the skill platform-specific when a portable instruction contract works.

## Validation

Before opening a pull request, run:

```bash
git diff --check
bash -n install.sh
python3 -m json.tool manifest.json >/dev/null
```

If Codex skill validation is available:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/nah-mean
```
