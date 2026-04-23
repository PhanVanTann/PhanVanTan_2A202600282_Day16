# Lab 16 Benchmark Report

## Metadata
- Dataset: test
- Mode: llm
- Records: 1
- Agents: react

## Summary

### Overall
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Count | 1 | 0 | N/A |
| EM | 1.0 | 0 | 0 |
| Avg attempts | 1 | 0 | 0 |
| Avg token estimate | 10 | 0 | 0 |
| Avg latency (ms) | 10 | 0 | 0 |

### Easy
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Count | 1 | 0 | N/A |
| EM | 1.0 | 0 | 0 |
| Avg attempts | 1 | 0 | 0 |
| Avg token estimate | 10 | 0 | 0 |
| Avg latency (ms) | 10 | 0 | 0 |

### Medium
No data available.

### Hard
No data available.


## Failure modes
```json
{
  "react": {
    "none": 1
  }
}
```

## Extensions implemented
- structured_evaluator
- reflection_memory
- benchmark_report_json
- mock_mode_for_autograding

## Discussion
Reflexion helps when the first attempt stops after the first hop or drifts to a wrong second-hop entity. The tradeoff is higher attempts, token cost, and latency. In a real report, students should explain when the reflection memory was useful, which failure modes remained, and whether evaluator quality limited gains.
