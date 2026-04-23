# Lab 16 Benchmark Report
# Họ Và Tên: Phan Văn Tấn
# MSHV : 2A202600282
## Metadata
- Dataset: hotpotqa.json
- Mode: llm
- Records: 200
- Agents: react, reflexion

## Summary

### Overall
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Count | 100 | 100 | N/A |
| EM | 0.83 | 1.0 | 0.17 |
| Avg attempts | 1 | 1.17 | 0.17 |
| Avg token estimate | 48.94 | 64.92 | 15.98 |
| Avg latency (ms) | 10647.88 | 14335.69 | 3687.81 |

### Easy
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Count | 33 | 33 | N/A |
| EM | 1.0 | 1.0 | 0.0 |
| Avg attempts | 1 | 1 | 0 |
| Avg token estimate | 44.3 | 44.3 | 0.0 |
| Avg latency (ms) | 11215.42 | 10637.09 | -578.33 |

### Medium
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Count | 33 | 33 | N/A |
| EM | 1.0 | 1.0 | 0.0 |
| Avg attempts | 1 | 1 | 0 |
| Avg token estimate | 36 | 36 | 0 |
| Avg latency (ms) | 8500.06 | 8279 | -221.06 |

### Hard
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Count | 34 | 34 | N/A |
| EM | 0.5 | 1.0 | 0.5 |
| Avg attempts | 1 | 1.5 | 0.5 |
| Avg token estimate | 66 | 113 | 47 |
| Avg latency (ms) | 12181.68 | 23804.06 | 11622.38 |


## Failure modes
```json
{
  "react": {
    "none": 83,
    "looping": 3,
    "wrong_final_answer": 5,
    "incomplete_multi_hop": 5,
    "entity_drift": 4
  },
  "reflexion": {
    "none": 100
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
