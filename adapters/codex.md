# Codex Adapter

## Install

```bash
./install.sh
```

This copies `skills/nah-mean` into:

```text
${CODEX_HOME:-$HOME/.codex}/skills/nah-mean
```

## Manual Install

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/nah-mean "${CODEX_HOME:-$HOME/.codex}/skills/nah-mean"
```

## Triggering

Use naturally:

```text
이 레포 분석해서 어떤 오픈소스인지 설명해줘. 뭔말알?
```

Or explicitly:

```text
Use $nah-mean to align intent before editing this prompt.
```

## Update Existing Install

Run `./install.sh` again. Existing target is backed up when content differs.
