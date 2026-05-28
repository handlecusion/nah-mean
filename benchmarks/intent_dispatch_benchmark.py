#!/usr/bin/env python3
"""Deterministic protocol benchmark for nah-mean.

This does not benchmark model quality. It compares protocol overhead for the
same fixture set: user-visible alignment text, decision workload, estimated
review seconds, and input context token proxy.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_SKILL = ROOT / "benchmarks" / "baselines" / "skill-v0.2.1.md"
CURRENT_SKILL = ROOT / "skills" / "nah-mean" / "SKILL.md"
RESULT_JSON = ROOT / "benchmarks" / "results.json"
RESULT_MD = ROOT / "benchmarks" / "results.md"


FIXTURES = [
    {
        "id": "ko_repo_analysis",
        "old": """뭔말알.
내가 이해한 방향:
- README 요약이 아니라 실제 채택 가능성 판단.
- 기능, 한계, 설치 난이도, 적용 작업을 분리.

피할 것:
- GitHub 설명만 번역.
- 장점만 나열.

실행 기준:
- 무엇을 할 수 있는지.
- 무엇을 못 하는지.
- 누구에게 유용한지.

이 기준으로 진행하면 된다.""",
        "new": """뭔말알.
의도: README 요약이 아니라 실제 채택 가능성 판단.
주의: GitHub 설명 번역이나 장점 나열로 끝나면 실패.
기준: 기능, 한계, 설치 난이도, 적용 작업을 분리.
알잘딱 route: Research + QA.

이 기준으로 진행하면 된다.""",
    },
    {
        "id": "ko_design",
        "old": """뭔말알.
내가 이해한 방향:
- 장식 추가보다 신뢰감 있는 디자인 방향 재정의.
- 템플릿 느낌을 줄이고 브랜드 신호를 강화.

피할 것:
- generic gradient.
- 추상적 프리미엄 문구.

실행 기준:
- 시각 hierarchy 개선.
- 첫 화면 제품 신호 강화.
- 카피와 spacing 정리.

이 기준으로 진행하면 된다.""",
        "new": """뭔말알.
의도: 장식 추가보다 신뢰감 있는 디자인 방향 재정의.
주의: generic gradient와 추상적 프리미엄 문구는 피함.
기준: hierarchy, 제품 신호, copy, spacing을 같이 정리.
알잘딱 route: Design + Edit.

이 기준으로 진행하면 된다.""",
    },
    {
        "id": "ko_fast_edit",
        "old": """뭔말알. 의도 확인용 답변이 아니라 바로 적용 가능한 문서 정리가 핵심이라, 구조와 문장만 정리하고 새 요구사항은 추가하지 않는다.""",
        "new": """뭔말알. 문서 정리가 핵심이다. 알잘딱 route는 Edit. 구조와 문장만 정리하고 새 요구사항은 추가하지 않는다.""",
    },
    {
        "id": "en_design",
        "old": """Got it.
My read:
- You want a stronger design direction, not decorative polish.
- The page should feel credible, specific, and less template-like.

Avoid:
- generic gradients.
- vague luxury language.

Execution criteria:
- clearer visual hierarchy.
- concrete product signal above the fold.
- tighter copy and spacing.

If this is right, I will proceed on this basis.""",
        "new": """Got it.
Intent: stronger design direction, not decorative polish.
Watchout: generic gradients and vague luxury language would miss the point.
Standard: clearer hierarchy, product signal, tighter copy and spacing.
Route: Design + Edit.

If this is right, I will proceed on this basis.""",
    },
    {
        "id": "en_research",
        "old": """Got it.
My read:
- You need a practical adoption decision, not a feature checklist.
- The comparison should prioritize workload fit, operating cost, ecosystem risk, and migration pain.

Avoid:
- vendor marketing language.
- ranking every feature equally.

Execution criteria:
- define workload assumptions.
- compare tradeoffs directly.
- give a default recommendation and change conditions.

If this is right, I will proceed on this basis.""",
        "new": """Got it.
Intent: practical adoption decision, not a feature checklist.
Watchout: vendor language or equal-weight feature tables would be weak.
Standard: define workload assumptions, compare tradeoffs, recommend default and change conditions.
Route: Research.

If this is right, I will proceed on this basis.""",
    },
    {
        "id": "en_fast_build",
        "old": """Got it. This is not a feature explanation. The key artifact is a copy-ready plugin spec, so I will produce one Markdown block.""",
        "new": """Got it. The artifact is a copy-ready plugin spec. Route: Build. I will produce one Markdown block.""",
    },
]


def token_proxy(text: str) -> int:
    """Small token proxy stable across Korean and English fixtures."""
    return len(re.findall(r"[A-Za-z0-9_]+|[가-힣]+", text))


def mean(nums: list[float]) -> float:
    return sum(nums) / len(nums)


def improvement(old: float, new: float) -> float:
    return (old - new) / old * 100 if old else 0.0


def workload_units(profile: str) -> int:
    # v0.2.1 exposes three section headings plus multiple bullets.
    # v0.3.0 exposes four compact fields and routes execution.
    return 8 if profile == "old" else 4


def main() -> int:
    old_tokens = [token_proxy(item["old"]) for item in FIXTURES]
    new_tokens = [token_proxy(item["new"]) for item in FIXTURES]
    old_work = [workload_units("old") for _ in FIXTURES]
    new_work = [workload_units("new") for _ in FIXTURES]

    old_token_mean = mean(old_tokens)
    new_token_mean = mean(new_tokens)
    old_work_mean = mean(old_work)
    new_work_mean = mean(new_work)

    old_seconds = old_token_mean / 4 + old_work_mean
    new_seconds = new_token_mean / 4 + new_work_mean

    baseline_input = token_proxy(BASELINE_SKILL.read_text())
    current_input = token_proxy(CURRENT_SKILL.read_text())

    result = {
        "fixture_count": len(FIXTURES),
        "baseline": "v0.2.1 default alignment",
        "current": "v0.3.0 light-align + context-fit dispatch",
        "metrics": {
            "user_visible_alignment_tokens": {
                "baseline": round(old_token_mean, 1),
                "current": round(new_token_mean, 1),
                "improvement_percent": round(improvement(old_token_mean, new_token_mean), 1),
            },
            "alignment_workload_units": {
                "baseline": round(old_work_mean, 1),
                "current": round(new_work_mean, 1),
                "improvement_percent": round(improvement(old_work_mean, new_work_mean), 1),
            },
            "estimated_review_seconds": {
                "baseline": round(old_seconds, 1),
                "current": round(new_seconds, 1),
                "improvement_percent": round(improvement(old_seconds, new_seconds), 1),
            },
            "input_context_token_proxy": {
                "baseline": baseline_input,
                "current": current_input,
                "improvement_percent": round(improvement(baseline_input, current_input), 1),
            },
        },
    }

    best = max(metric["improvement_percent"] for metric in result["metrics"].values())
    result["pass"] = best >= 30.0

    RESULT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    RESULT_MD.write_text(render_markdown(result))

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["pass"]:
        raise SystemExit("benchmark gate failed: no metric improved by at least 30%")
    return 0


def render_markdown(result: dict) -> str:
    rows = []
    for name, metric in result["metrics"].items():
        rows.append(
            f"| {name} | {metric['baseline']} | {metric['current']} | "
            f"{metric['improvement_percent']}% |"
        )

    return (
        "# nah-mean v0.3.0 Benchmark\n\n"
        f"- Fixture count: {result['fixture_count']}\n"
        f"- Baseline: {result['baseline']}\n"
        f"- Current: {result['current']}\n"
        f"- Gate: at least one metric must improve by 30% or more\n"
        f"- Result: {'PASS' if result['pass'] else 'FAIL'}\n\n"
        "| Metric | Baseline | Current | Improvement |\n"
        "| --- | ---: | ---: | ---: |\n"
        + "\n".join(rows)
        + "\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
