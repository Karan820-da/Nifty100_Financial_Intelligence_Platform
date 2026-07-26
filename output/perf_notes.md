# Sprint 6 - Day 43 Performance Notes

## Load Test

- Concurrent Requests: 10
- Total Execution Time: 3.06 seconds
- Average Response Time: 2.94 seconds
- Fastest Response: 2.80 seconds
- Slowest Response: 3.05 seconds

Result:
- Passed sprint requirement (10 concurrent requests completed within 10 seconds).

## Dashboard Performance

| Company | Load Time |
|---------|-----------|
| TCS | 2 sec |
| INFY | 2 sec |
| HDFCBANK |2 sec |
| RELIANCE | 2 sec |
| ICICIBANK | 2 sec |

Target:
- Under 3 seconds per company profile.

## End-to-End Integration

- FastAPI running on port 8000: ✅
- Streamlit running on port 8501: ✅
- No port conflicts: ✅
- Dashboard successfully retrieved API data: ✅


## Performance Bottlenecks

No significant bottlenecks identified during concurrent API testing