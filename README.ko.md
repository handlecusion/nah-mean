# nah-mean

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/handlecusion/nah-mean)](https://github.com/handlecusion/nah-mean/releases)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-green)](skills/nah-mean/SKILL.md)

[English](README.md) | 한국어

nah-mean은 Codex, Claude Code, 일반 agent에 붙일 수 있는 intent alignment skill이다. 사용자가 모호하지만 높은 품질을 기대하는 요청을 했을 때 바로 실행하지 않고, 명시 요청과 암묵적 품질 기준을 짧게 정리한 뒤 확인을 받고 진행한다. 확인 뒤에는 `알잘딱` route로 Direct, Edit, Build, Research, Design, QA, Safety Gate 중 최소 적합 executor를 고른다.

사용자가 `뭔말알?`, `뭔말인지 알지?`, `이 느낌 알지?`, `이 방향 맞지?`, `알아서 잘`, `알잘딱`, `찰떡같이` 같은 표현을 붙일 때 쓴다.

## 한눈에 보기

| 질문 | 답 |
| --- | --- |
| 무엇인가? | 모호한 agent 요청을 실행 전 정렬하는 intent alignment layer |
| 누구에게 필요한가? | 프롬프트 오해와 재작업을 줄이고 싶은 agent 사용자/관리자 |
| 핵심 파일 | `skills/nah-mean/SKILL.md` |
| 지원 대상 | Codex, Claude Code, Agent Skills 호환 클라이언트, prompt-only agent |
| 언어 | 한국어와 영어 |
| 현재 릴리스 | `v0.3.0` |
| AI discovery | [llms.txt](llms.txt), [llms-full.txt](llms-full.txt) |

## 뭔말알-알잘딱-Driven

이 skill은 긴 plan을 먼저 만드는 방식이 아니다.

- `[뭔말알]`: 사용자의 말끝에 숨은 의도, 실패 위험, 실행 기준만 짧게 잡는다.
- `[알잘딱]`: 확인 뒤 상황에 맞는 executor route를 고른다.
- 목표: 더 적은 토큰과 더 적은 질문으로, 실행 전 오해를 줄이는 것.

유쾌한 이름이지만 성능 기준은 진지하게 잡는다. 벤치마크 기준으로 v0.3.0은 v0.2.1 기본 정렬보다 예상 검토 시간을 평균 34.3% 줄였다.

## 이런 경우 사용

- 프롬프트가 `뭔말알?`, `이 느낌 알지?`, `알아서 잘`, `알잘딱`, `찰떡같이` 같은 표현으로 끝남.
- 디자인, 글쓰기, 리서치, 기획, 발표자료, 프롬프트/agent 설계, 코드 구조처럼 취향과 맥락이 중요한 작업.
- 바로 실행하면 톤, 깊이, 독자, 형식 해석이 어긋나 재작업이 생길 가능성이 큼.
- 파일 수정이나 도구 호출 전에 agent가 가정, 실패 방향, 실행 기준을 먼저 말해주길 원함.
- 확인 뒤에는 agent가 Direct/Edit/Build/Research/Design/QA 중 맞는 실행 route를 알아서 고르길 원함.

## 이런 경우 사용하지 않음

- `date` 실행, 변수명 변경처럼 정확하고 낮은 위험의 작업.
- 사용자가 `바로 해`, `확인 생략`, `질문하지 말고 진행`이라고 명시함.
- 보안, 법률, 결제, 삭제, 배포처럼 별도 확인이 필요한 작업. 이 skill은 안전 확인을 대체하지 않음.

## 예시

### 기본 정렬

사용자:

```text
이 레포 분석해서 어떤 오픈소스인지 설명해줘. 뭔말알?
```

Agent:

```text
뭔말알.
의도: README 요약이 아니라 실제로 써먹을 수 있는지 판단하는 분석.
주의: GitHub 설명 번역이나 장점 나열로 끝나면 실패.
기준: 기능, 한계, 설치 난이도, 적용 가능한 작업, 위험한 착각을 분리.
알잘딱 route: Research + QA.

이 기준으로 진행하면 된다.
```

### 디자인/문서 정렬

사용자:

```text
이 랜딩페이지 더 고급스럽고 덜 뻔하게 만들어줘. 이 느낌 알지?
```

Agent:

```text
뭔말알.
의도: 장식 추가가 아니라 신뢰감 있는 디자인 방향 재정의.
주의: generic gradient, 추상적 프리미엄 문구, 빈 공간만 늘리는 구성은 피함.
기준: 시각 hierarchy, 첫 화면 제품 신호, 카피와 spacing을 같이 정리.
알잘딱 route: Design + Edit.
```

### Fast Mode

사용자:

```text
이 기준으로 문서 정리해. 질문하지 말고 진행. 뭔말알?
```

Agent:

```text
뭔말알. 이건 의도 확인용 답변이 아니라 바로 적용 가능한 문서 정리가 핵심이다. 알잘딱 route는 Edit로 잡고, 구조와 문장만 정리하며 새 요구사항은 추가하지 않는다.
```

그 다음 바로 실행한다.

### 방지되는 나쁜 결과

nah-mean이 없으면 agent가 `알아서 잘`을 스타일, 범위, 기능을 마음대로 추가해도 된다는 뜻으로 해석할 수 있다. nah-mean은 먼저 "잘"의 의미를 작업 기준으로 바꾼다: 대상 독자, 출력 형식, 실패 방향, 완료 기준. 이 짧은 정렬이 그럴듯하지만 틀린 결과를 줄인다.

## 왜 만들었나

agent 실패는 모델 성능 부족이 아니라 의도 정렬 실패에서 많이 나온다. 사용자는 방향, 톤, 품질 기준이 당연하다고 생각하지만 agent에게는 생략된 정보인 경우가 많다. nah-mean은 그 암묵 기대를 짧고 반복 가능한 절차로 바꾼다.

설계 원칙:

- alignment가 과한 회의록이나 plan theater가 되지 않도록 짧게 유지.
- confirmation 뒤에는 알잘딱 route로 최소 적합 executor를 선택.
- 질문 폭탄보다 합리적 기본값 선언 선호.
- runtime preference memory와 durable memory 구분.
- 특정 vendor API에 묶이지 않는 portable instruction contract 유지.

비목표:

- 안전 확인 대체.
- 서버, DB, memory system 추가.
- 명확하고 낮은 위험의 명령에도 강제 적용.
- 실제 저장장치 없이 durable personalization을 주장.

## 설치

agent에 맞는 방식을 고른다.

### 추천 경로

| 대상 | 권장 경로 | 명령 |
| --- | --- | --- |
| Codex, local checkout | bundled installer | `./install.sh` |
| Codex, GitHub 설치 | GitHub CLI | `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user` |
| Claude Code, GitHub 설치 | GitHub CLI | `gh skill install handlecusion/nah-mean nah-mean --agent claude-code --scope user` |
| Agent Skills 호환 client | `skills` CLI | `npx skills add handlecusion/nah-mean --skill nah-mean -a <agent> -g -y` |
| prompt-only agent | prompt 복사 | `prompts/nah-mean.ko.md` |

### Codex

```bash
gh skill preview handlecusion/nah-mean nah-mean
gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user
```

고정 버전:

```bash
gh skill install handlecusion/nah-mean nah-mean@v0.3.0 --agent codex --scope user
```

로컬 checkout:

```bash
./install.sh
```

수동 설치:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/nah-mean "${CODEX_HOME:-$HOME/.codex}/skills/nah-mean"
```

### Claude Code

```bash
gh skill preview handlecusion/nah-mean nah-mean
gh skill install handlecusion/nah-mean nah-mean --agent claude-code --scope user
```

또는 [adapters/claude-code.md](adapters/claude-code.md)의 snippet을 프로젝트 `CLAUDE.md`나 user-level memory에 넣는다.

### Agent Skills CLI

```bash
npx skills add handlecusion/nah-mean --list
npx skills add handlecusion/nah-mean --skill nah-mean -a codex -g -y
```

주의: 현재 `skills` CLI는 Codex global install을 `~/.agents/skills`에 둘 수 있다. Codex가 `~/.codex/skills`를 보는 환경이면 `gh skill install ... --agent codex --scope user` 또는 `./install.sh`를 우선한다.

### Prompt-only Agent

다음 중 하나를 쓴다:

- [prompts/nah-mean.ko.md](prompts/nah-mean.ko.md)
- [adapters/generic-agent.md](adapters/generic-agent.md)
- [adapters/hermes-like.md](adapters/hermes-like.md)
- 영어 사용자용은 [prompts/nah-mean.en.md](prompts/nah-mean.en.md)

## Repo 구성

```text
.
├── install.sh                  # Codex global skill 설치
├── manifest.json               # portable entrypoint map and metadata
├── llms.txt                    # compact AI discovery file
├── llms-full.txt               # expanded AI discovery file
├── README.md                   # English documentation
├── README.ko.md                # Korean documentation
├── skills/nah-mean/            # Codex / Agent Skills package
├── prompts/                    # prompt-only agent용 prompt
├── adapters/                   # framework별 설치 notes
├── benchmarks/                 # protocol overhead benchmark
└── docs/                       # GitHub Pages-ready discovery page
```

## 동작 방식

기본 모드:

1. intent-alignment trigger 감지.
2. `[뭔말알]`로 의도, 주의, 기준만 짧게 정리.
3. 필요할 때만 최대 1-3개 질문.
4. 확인 후 `[알잘딱]` route 선택.
5. Direct/Edit/Build/Research/Design/QA/Safety Gate 중 최소 적합 executor로 실행.

Fast mode trigger:

- `바로 해`
- `확인 생략`
- `질문하지 말고 진행`

Fast mode는 짧게 해석하고 알잘딱 route를 고른 뒤 바로 실행한다.

## 비교

| 방식 | 적합한 경우 | 부적합한 경우 |
| --- | --- | --- |
| nah-mean skill | 여러 agent 작업에서 재사용되는 trigger 기반 alignment | 일회성 prompt 하나만 필요할 때 |
| Custom instructions | 넓은 개인 선호 반영 | 작업별 실행 계약과 예시가 필요할 때 |
| Prompt snippet | skill format 없는 도구에 복붙 | 자동 discovery나 구조화된 references가 필요할 때 |
| Project memory rule | 프로젝트별 반복 correction | 여러 agent에 설치 가능한 일반 규칙이 필요할 때 |
| MCP/tool router | tool-backed workflow 자동화 | tool 호출 전 순수 instruction behavior가 필요할 때 |

## 벤치마크

v0.3.0은 같은 6개 fixture를 v0.2.1 기본 정렬 방식과 새 뭔말알-알잘딱 방식으로 비교한다.

```bash
python3 benchmarks/intent_dispatch_benchmark.py
```

현재 결과:

| Metric | v0.2.1 baseline | v0.3.0 | Change |
| --- | ---: | ---: | ---: |
| 사용자에게 보이는 alignment tokens | 39.5 | 31.0 | 21.5% 감소 |
| Alignment workload units | 8.0 | 4.0 | 50.0% 감소 |
| 예상 검토 시간(초) | 17.9 | 11.8 | 34.3% 감소 |
| Input context token proxy | 388 | 493 | 27.1% 증가 |

Input context token은 새 executor dispatch 설명 때문에 증가했다. 대신 decision workload와 estimated review time 중 하나 이상이 30% 이상 줄었는지 gate로 검증한다.

## FAQ

### nah-mean은 무엇인가?

nah-mean은 모호한 intent-checking 표현을 실행 전 계약으로 바꾸는 portable agent skill이다. agent가 파일 수정, 글쓰기, 디자인, 리서치, 도구 호출 전에 방향, 가정, 실패 가능성, 품질 기준을 먼저 정렬하게 만든다.

### Codex에 어떻게 설치하나?

GitHub 설치는 `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user`를 쓴다. 로컬 checkout에서는 `./install.sh`를 실행한다. 둘 다 `SKILL.md`, references, Codex metadata가 포함된 skill folder를 설치한다.

### 어떤 agent를 지원하나?

패키지 skill은 Codex와 Agent Skills 호환 client를 대상으로 한다. Claude Code, Hermes-like agent, generic agent용 adapter prompt도 제공한다. prompt-only agent는 `prompts/` 파일을 복사해서 쓸 수 있다.

### 설치해도 안전한가?

skill package에는 실행 script가 없다. instructions, references, metadata만 들어 있다. 그래도 agent behavior에 영향을 주므로 설치 전 `gh skill preview handlecusion/nah-mean nah-mean`으로 내용을 확인한다.

### runtime preference memory와 durable memory는 어떻게 다른가?

runtime preference memory는 현재 세션/프로젝트에서 agent가 참고하는 작업 상태다. durable memory는 파일, wiki, memory tool 등에 실제로 기록되는 장기 상태다. nah-mean은 실제 저장 수단 없이 영구 기억을 주장하지 않도록 지시한다.

## AI Discovery

AI system과 crawler는 다음 파일을 쓸 수 있다:

- [llms.txt](llms.txt): compact canonical facts and install commands.
- [llms-full.txt](llms-full.txt): expanded bilingual contract and entrypoints.
- [docs/index.html](docs/index.html): GitHub Pages-ready HTML with JSON-LD.
- [manifest.json](manifest.json): machine-readable entrypoint and install metadata.

## Distribution Model

이 repo는 agent-skill 배포 관행을 따른다:

- `skills/nah-mean/SKILL.md` 중심 구조.
- `npx skills add handlecusion/nah-mean --skill nah-mean -a <agent> -g`.
- `gh skill preview` 후 `gh skill install handlecusion/nah-mean nah-mean`.
- clone 후 `./install.sh` fallback.
- skill 미지원 agent는 `prompts/` 파일 복사.

참고:

- Agent Skills format: https://agentskills.io/
- Vercel `skills` CLI: https://github.com/vercel-labs/skills
- Vercel Agent Skills repo: https://github.com/vercel-labs/agent-skills
- GitHub `gh skill`: https://cli.github.com/manual/gh_skill_install
- GitHub Copilot skills docs: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- Elastic Agent Skills repo: https://github.com/elastic/agent-skills
- Awesome Copilot repo: https://github.com/github/awesome-copilot

## 설치 전 확인

Agent skill은 coding agent의 행동을 바꾸는 instruction이다. 설치 전 확인한다:

```bash
gh skill preview handlecusion/nah-mean nah-mean
sed -n '1,220p' skills/nah-mean/SKILL.md
find skills/nah-mean -maxdepth 3 -type f -print
```

이 skill package에는 실행 script가 없다. instruction/reference content만 있다.

## 검증

마지막 검증일: 2026-05-28.

| Check | Result |
| --- | --- |
| `gh skill preview handlecusion/nah-mean nah-mean` | `nah-mean` skill tree와 `SKILL.md` 렌더링 |
| `gh skill install handlecusion/nah-mean nah-mean --agent codex --scope user` | Codex user skill directory에 설치 |
| `npx --yes skills add handlecusion/nah-mean --skill nah-mean -a codex -g -y --copy` | Agent Skills CLI 설치 성공. 현재 CLI는 Codex global install을 `~/.agents/skills`에 둘 수 있음 |
| `quick_validate.py skills/nah-mean` | `Skill is valid!` |
| `python3 benchmarks/intent_dispatch_benchmark.py` | 30%+ improvement gate 통과 |
| `bash -n install.sh` | 통과 |

Codex skill validation:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/nah-mean
```

Shell and metadata:

```bash
bash -n install.sh
python3 -m json.tool manifest.json >/dev/null
```

Benchmark:

```bash
python3 benchmarks/intent_dispatch_benchmark.py
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

## 업데이트

로컬 checkout:

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

## 신뢰와 유지보수

- License: [MIT](LICENSE)
- Security policy: [SECURITY.md](SECURITY.md)
- Contributing guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Maintainer info: [MAINTAINERS.md](MAINTAINERS.md)
- Citation metadata: [CITATION.cff](CITATION.cff)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
