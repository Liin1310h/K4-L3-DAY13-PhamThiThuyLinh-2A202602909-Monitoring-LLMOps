# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert mẫu để tham khảo

Ví dụ dưới đây minh họa mức độ cụ thể cần có. Học viên không cần copy nguyên, nhưng ba alert trong bài nộp nên rõ ràng tương tự: điều kiện là gì, kéo dài bao lâu, ảnh hưởng tới user ra sao và người trực cần kiểm tra gì trước.

- Tên: `HighLatencyP95`
- Severity: `warning`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: latency P95 của `response_sent.latency_ms`
- Điều kiện và thời gian duy trì: `p95(latency_ms) > 3000ms` trong 5 phút
- Ảnh hưởng tới người dùng: người dùng phải chờ lâu hơn trước khi nhận câu trả lời
- Ba bước kiểm tra đầu tiên:
  1. Mở dashboard latency để xác nhận P95/P99 và khoảng thời gian tăng.
  2. Lọc `data/logs.jsonl` trong khoảng đó, lấy một `correlation_id` có `latency_ms` cao.
  3. Mở trace cùng `correlation_id` trên Langfuse, so sánh các span chính để xác định bước nào bất thường.
- Mitigation tạm thời: dựa trên evidence thực tế để rollback prompt, khôi phục cấu hình liên quan, tắt practice scenario hoặc giảm tải khi demo.
- Owner: `student-<MSSV>`

## Alert 1

- Tên:
- Severity:
- Duration:
- Kênh thông báo: Slack
- SLI/SLO liên quan:
- Điều kiện và thời gian duy trì:
- Ảnh hưởng tới người dùng:
- Ba bước kiểm tra đầu tiên:
- Mitigation tạm thời:
- Owner:

## CP2 completed runbooks

The active alert contract is defined in `config/alert_rules.yaml`:

### Alert 1: HighLatencyP95

- Severity: warning; duration: 5m; Slack: `#k4-l3b-alerts`.
- Condition: `p95(response_sent.latency_ms) > 3000`.
- Check the latency panel, filter `data/logs.jsonl` by high `latency_ms`, then open the trace with the same `correlation_id`.
- Mitigate by rolling back the prompt if generation is slow, disabling a practice incident, or reducing load.

### Alert 2: HighErrorRate

- Severity: critical; duration: 5m; Slack: `#k4-l3b-alerts`.
- Condition: `error_rate(request_failed) > 2%`.
- Break down `request_failed` by `error_type`, select a `correlation_id`, and inspect its trace.
- Mitigate by disabling the incident, switching to the known-good prompt version, or restoring the failed dependency.

### Alert 3: LowRetrievalSuccess

- Severity: warning; duration: 10m; Slack: `#k4-l3b-alerts`.
- Condition: `retrieval_success_rate < 90%`.
- Check `tool_success` in the errors panel, inspect failed retrieval log lines, and compare retriever spans.
- Mitigate by restoring the retrieval dependency/index and rerunning the workload to confirm recovery.

## Alert 2

- Tên:
- Severity:
- Duration:
- Kênh thông báo: Slack
- SLI/SLO liên quan:
- Điều kiện và thời gian duy trì:
- Ảnh hưởng tới người dùng:
- Ba bước kiểm tra đầu tiên:
- Mitigation tạm thời:
- Owner:

## Alert 3

- Tên:
- Severity:
- Duration:
- Kênh thông báo: Slack
- SLI/SLO liên quan:
- Điều kiện và thời gian duy trì:
- Ảnh hưởng tới người dùng:
- Ba bước kiểm tra đầu tiên:
- Mitigation tạm thời:
- Owner:
