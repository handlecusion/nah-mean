# Security Policy

## Scope

nah-mean is an agent instruction package. The skill itself contains no executable scripts. It includes Markdown instructions, reference files, prompts, adapter notes, and metadata.

Still inspect before installing because agent skills change agent behavior:

```bash
gh skill preview handlecusion/nah-mean nah-mean
find skills/nah-mean -maxdepth 3 -type f -print
```

## Reporting

Report security concerns through GitHub Issues:

https://github.com/handlecusion/nah-mean/issues

Use a clear title such as `Security: <summary>`. Do not include private API keys, tokens, or sensitive data in public issues.

## Supported Versions

| Version | Supported |
| --- | --- |
| `v0.2.x` | Yes |
| `v0.1.x` | Best effort |

## Safe Install Expectations

- Prefer pinned installs for reproducible agent behavior:
  `gh skill install handlecusion/nah-mean nah-mean@v0.3.2 --agent codex --scope user`
- Review `skills/nah-mean/SKILL.md` and `references/` before use.
- Do not install agent skills from forks or mirrors unless you trust the source.
- Treat runtime preference memory as session/project state unless your agent provides durable storage.
