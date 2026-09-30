# CP3 incident evidence

- Challenge ID: `day13-k4-l3b-monitoring-llmops-v1`
- Incident: `rag_slow`
- Affected feature: `monitoring`
- Challenge threshold: `2000 ms`
- Workload: `python scripts/load_test.py --challenge --concurrency 5`

## Metrics

The `/metrics` response after the challenge workload reported:

- traffic: `5`
- latency P50: `2978 ms`
- latency P95: `7125 ms`
- latency P99: `7125 ms`
- TTFT P95: `51 ms`
- quality average: `0.84`

The P95 latency violates the challenge threshold and the CP2 latency SLO threshold of `3000 ms`.

## Logs

Affected request: `correlation_id=req-c5e977df`.

Its `response_sent` record has `latency_ms=7125`, `ttft_ms=50`, `tool_name=retrieval`, and `tool_success=true`. The request used feature `monitoring` and session `k4-l3b-challenge-s02`.

## Root cause and action

`rag_slow` was enabled by the challenge control endpoint. In `app/mock_rag.py`, `retrieve()` calls `time.sleep(2.5)` when that incident is active. Therefore the retrieval span is the slow span; TTFT and retrieval success remain normal, so the evidence points to retrieval latency rather than LLM generation or a retrieval error.

Fix action: disable `rag_slow`, restore the normal retrieval path, and rerun the same challenge workload to confirm P95 recovery.

Preventive measure: keep `HighLatencyP95` alerting on `p95(response_sent.latency_ms) > 3000` for 5 minutes, then follow the runbook to correlate the slow log with its Langfuse trace.

Trace ID: to be copied from the student's private Langfuse project for `req-c5e977df`; no trace ID is fabricated in this evidence.
