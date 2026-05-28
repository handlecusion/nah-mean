# nah-mean v0.3.0 Benchmark

- Fixture count: 6
- Baseline: v0.2.1 default alignment
- Current: v0.3.0 light-align + context-fit dispatch
- Gate: at least one metric must improve by 30% or more
- Result: PASS

| Metric | Baseline | Current | Improvement |
| --- | ---: | ---: | ---: |
| user_visible_alignment_tokens | 39.5 | 31.0 | 21.5% |
| alignment_workload_units | 8.0 | 4.0 | 50.0% |
| estimated_review_seconds | 17.9 | 11.8 | 34.3% |
| input_context_token_proxy | 388 | 493 | -27.1% |
