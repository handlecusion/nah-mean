# GEO Improvement Goal Prompt

Use this prompt to drive the next implementation pass.

```text
<goal_context>
Continue working toward the active thread goal.

<objective>
Improve the public GEO/SEO readiness of https://github.com/handlecusion/nah-mean so AI search systems and agent-skill installers can discover, understand, cite, trust, and recommend the project.

Current audit baseline:
- Overall GEO score: ~55/100 (Fair/Poor boundary)
- AI Visibility: 59/100
- Brand Authority: ~20/100
- Content E-E-A-T: 67/100
- Technical GEO: 82/100
- Schema / Structured Data: 56/100
- Platform Readiness: 51/100

Primary diagnosis:
- The repo is technically accessible and installable, but weak as a public entity.
- README has useful install commands, but lacks compact AI-answer blocks, FAQ, visible examples, and trust artifacts.
- GitHub metadata is good but incomplete: no license, no homepage, no maintainer/citation/security files, no llms.txt, no release asset/checksum.
- Because GitHub controls page schema/robots, repo-owned AI discovery should happen through README structure, root llms.txt, manifest metadata, release assets, and optionally GitHub Pages.
</objective>

Requirements:
1. Add open-source trust files:
   - LICENSE, preferably MIT unless user specifies otherwise.
   - SECURITY.md with safe-install guidance for agent skills and vulnerability/reporting policy.
   - CONTRIBUTING.md with lightweight contribution rules.
   - CITATION.cff with project title, author/maintainer handle, version 0.1.0 or next version, release date, repo URL, and keywords.
   - CHANGELOG.md with v0.1.0 initial release and the current improvement release section.

2. Improve README for AI citability:
   - Add a top "What is nah-mean?" answer block in 40-70 words.
   - Add "Use it when" and "Do not use it when" bullets near the top.
   - Add 3-4 visible examples:
     - Korean default alignment mode.
     - English default alignment mode.
     - Fast mode.
     - Before/after showing a bad ambiguous request response prevented by nah-mean.
   - Add FAQ with short direct answers:
     - What is nah-mean?
     - How do I install nah-mean in Codex?
     - Which agents are supported?
     - Is nah-mean safe to install?
     - How is runtime preference memory different from durable memory?
   - Add comparison table:
     - nah-mean skill vs custom instructions vs prompt snippet vs project memory rule vs MCP/tool router.
     - Include best-for and not-for rows.
   - Add "Tested with" section with command outputs summarized:
     - `gh skill preview handlecusion/nah-mean nah-mean`
     - `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user`
     - `npx --yes skills add handlecusion/nah-mean --skill nah-mean -a codex -g -y --copy`
     - `quick_validate.py skills/nah-mean`
   - Keep README concise enough that install commands remain easy to copy.

3. Add AI discovery files:
   - Add root `llms.txt` with canonical project facts, repo URL, release URL, skill path, install commands, supported agents, safety note, and important docs links.
   - Add root `llms-full.txt` with expanded bilingual trigger/behavior contract and all important repository entrypoints.
   - Link `llms.txt` from README near the install/discovery section.

4. Enrich machine-readable metadata:
   - Expand `manifest.json` with:
     - `repository`
     - `canonical_url`
     - `release_url`
     - `license`
     - `keywords`
     - `maintainers`
     - `homepage`
     - `skill_path`
     - `same_as`
     - `verified_install_commands`
   - Keep existing entrypoints.
   - Validate JSON.

5. Optional but high-value if time allows:
   - Add `docs/index.html` for GitHub Pages with server-rendered content and JSON-LD using `SoftwareSourceCode` and `CreativeWork`.
   - Add `docs/llms.txt` mirroring root `llms.txt`.
   - Add `docs/sitemap.xml`.
   - Set GitHub repo homepage to the Pages URL after publishing.
   - Create a release zip asset `nah-mean-skill-vNEXT.zip` and SHA256 checksum.

Verification:
- Run `git diff --check`.
- Run `bash -n install.sh`.
- Run `python3 -m json.tool manifest.json >/dev/null`.
- Run Codex skill validation:
  `python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/nah-mean`
  If PyYAML is missing, install it into a temporary target and set PYTHONPATH, not global Python.
- Run local install smoke test:
  `tmp_target="$(mktemp -d)" && ./install.sh --target-root "$tmp_target" && test -f "$tmp_target/nah-mean/SKILL.md"`
- Run GitHub CLI local skill install smoke test:
  `tmp_target="$(mktemp -d)" && gh skill install . nah-mean --from-local --dir "$tmp_target" --force && test -f "$tmp_target/nah-mean/SKILL.md"`
- If remote changes are pushed, run:
  `gh skill preview handlecusion/nah-mean nah-mean`
  `gh skill install handlecusion/nah-mean nah-mean --dir "$(mktemp -d)" --force`
  `npx --yes skills add handlecusion/nah-mean --skill nah-mean -a codex -g -y --copy`

Constraints:
- Do not add API keys, local absolute paths, or private machine data.
- Keep install commands copy-pasteable.
- Avoid claiming durable memory unless the target agent/runtime provides it.
- Do not over-market. Prefer concrete behavior, examples, commands, and validation evidence.
- Treat this as a repo/package GEO improvement pass, not a traditional website SEO project.

Completion criteria:
- Trust files exist and are linked where appropriate.
- README includes AI-citable answer blocks, examples, FAQ, comparison table, and tested install evidence.
- `llms.txt` and `llms-full.txt` exist at repo root.
- `manifest.json` contains enriched metadata and validates.
- Skill package still validates.
- Install smoke tests pass.
- Public repo metadata and README make the project easy for AI systems to summarize as:
  "nah-mean is a portable intent alignment skill for Codex, Claude Code, and generic agents that pauses ambiguous high-expectation requests, aligns intent, and then executes after confirmation."
</goal_context>
```

## Audit Summary

| Category | Score | Main Gap |
|---|---:|---|
| AI Visibility | 59 | Missing `llms.txt`, weak external entity signals, no compact answer block |
| Brand Authority | 20 | New repo, no stars/forks/external mentions, no homepage |
| Content E-E-A-T | 67 | Good mechanics, weak maintainer story/trust artifacts/examples |
| Technical GEO | 82 | Strong GitHub access/install surface, but GitHub-controlled crawl limits |
| Schema / Structured Data | 56 | GitHub microdata only; no repo-owned JSON-LD/docs site |
| Platform Readiness | 51 | Good Bing/GitHub fit, weak Google/Gemini/entity footprint |

## Highest-Impact First Edits

1. Add `LICENSE`, `SECURITY.md`, `CITATION.cff`, `CONTRIBUTING.md`, `CHANGELOG.md`.
2. Add top README answer block, FAQ, examples, and comparison table.
3. Add root `llms.txt` and `llms-full.txt`.
4. Enrich `manifest.json`.
5. Add docs/GitHub Pages with JSON-LD if public discovery remains priority after basic repo trust work.
