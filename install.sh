#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./install.sh [--target-root PATH]

Installs the nah-mean Codex skill into:
  ${CODEX_HOME:-$HOME/.codex}/skills/nah-mean

Options:
  --target-root PATH  Directory containing Codex skills
  -h, --help          Show help
EOF
}

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$repo_dir/skills/nah-mean"
target_root="${CODEX_HOME:-$HOME/.codex}/skills"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target-root)
      if [ "$#" -lt 2 ]; then
        echo "error: --target-root requires PATH" >&2
        exit 2
      fi
      target_root="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ ! -f "$source_dir/SKILL.md" ]; then
  echo "error: missing skill source: $source_dir" >&2
  exit 1
fi

mkdir -p "$target_root"
target_dir="$target_root/nah-mean"

if [ -d "$target_dir" ] && diff -qr "$source_dir" "$target_dir" >/dev/null; then
  echo "nah-mean already installed: $target_dir"
  exit 0
fi

if [ -e "$target_dir" ]; then
  backup_dir="$target_dir.backup.$(date +%Y%m%d%H%M%S)"
  mv "$target_dir" "$backup_dir"
  echo "existing skill backed up: $backup_dir"
fi

cp -R "$source_dir" "$target_dir"
echo "installed nah-mean: $target_dir"
