# nah-mean v0.3.1 Benchmark

- Fixture count: 6
- Baseline: vanilla agent (no skill)
- Current: nah-mean v0.3.1 light-align + context-fit dispatch
- Type: deterministic protocol-risk estimate, not model quality benchmark
- Gate: at least one nah-mean metric must improve by 30% or more
- Result: PASS

| Metric | Vanilla | nah-mean | Change | Winner |
| --- | ---: | ---: | ---: | --- |
| upfront_alignment_tokens | 0.0 | 31.0 | +31.0 tokens | vanilla |
| input_context_token_proxy | 0 | 493 | +493 token proxy | vanilla |
| expected_rework_units | 4.6 | 0.8 | 81.8% lower | nah-mean |
| coordination_workload_units | 4.6 | 2.8 | 38.2% lower | nah-mean |
| estimated_rework_adjusted_seconds | 36.7 | 18.4 | 49.8% lower | nah-mean |

Vanilla wins upfront token overhead because no skill context or alignment response is added. nah-mean wins rework-adjusted workload/time by making intent and executor route explicit before work starts.
