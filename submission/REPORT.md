# Báo cáo cá nhân — K4-L3B Day 13 Monitoring & LLMOps

## 1. Thông tin học viên

- Họ và tên: **Phạm Thị Thùy Linh**
- MSSV: **2A202602909**
- Lớp: `K4-L3B`
- Repository URL: **[BỔ SUNG URL REPOSITORY]**
- Commit SHA cuối: **[BỔ SUNG SAU KHI COMMIT]**
- Project Langfuse: `day13-k4-l3b-<MSSV>`
- Challenge ID: `day13-k4-l3b-monitoring-llmops-v1`

## 2. Evidence index

| Evidence            | File                                                              |
| ------------------- | ----------------------------------------------------------------- |
| Log validator       | [02-log-validator.png](evidence/02-log-validator.png)             |
| Dashboard validator | [03-dashboard-validator.png](evidence/03-dashboard-validator.png) |
| Structured log      | [04-structured-log.png](evidence/04-structured-log.png)           |
| CP3 incident note   | [15-cp3-incident-note.md](evidence/15-cp3-incident-note.md)       |

Ảnh runtime Langfuse, dashboard và incident còn cần bổ sung sau khi chụp: `01`, `05`, `06`–`14`.

## 3. Kết quả kỹ thuật

| Hạng mục                | Kết quả     |
| ----------------------- | ----------- |
| Log validator           | `100/100`   |
| Missing required fields | `0`         |
| Missing enrichment      | `0`         |
| Unique correlation IDs  | `17`        |
| PII leaks               | `0`         |
| Dashboard validator     | `6/6 panel` |
| Tracing/prompt tests    | `7 passed`  |
| CP3 latency P95/P99     | `7125 ms`   |
| CP3 TTFT P95            | `51 ms`     |
| CP3 quality average     | `0.84`      |

## 4. Checkpoint 1 — Logging và PII

Middleware xoá context cũ trước mỗi request, nhận `x-request-id` hợp lệ hoặc sinh ID dạng `req-<8-hex>`, bind ID vào structlog và trả lại qua header `x-request-id`. Header `x-response-time-ms` cũng được trả về.

Trước event `request_received`, ứng dụng bind `user_id_hash`, `session_id`, `feature`, `model` và `env`. User ID được hash SHA-256 rút gọn, không ghi giá trị nguyên bản.

PII scrubber chạy trước JSON rendering và file writer. Các pattern gồm email, số điện thoại Việt Nam, CCCD và thẻ thanh toán. Structured log đạt `100/100`, không còn record thiếu field, thiếu enrichment hoặc PII nguyên văn.

Evidence: [log validator](evidence/02-log-validator.png), [structured log](evidence/04-structured-log.png). Ảnh PII redaction cần bổ sung tại `evidence/05-pii-redaction.png`.

## 5. Checkpoint 2 — Tracing, prompt, dashboard và alert

Mỗi request có root observation `day13-agent-request`/`lab-agent-run`, cùng hai child observations: `retrieval` dạng `retriever` và `llm-generation` dạng `generation`. Generation ghi model, prompt reference, input/output tokens và cost; preview được scrub trước khi gửi.

Prompt dùng name `day13-chat`, label `production` và version lấy từ Langfuse. Prompt v1 là baseline; prompt v2 cải thiện grounding và fallback. Trace ID cần bổ sung sau khi chụp:

- Trace dùng prompt v1: **[BỔ SUNG TRACE ID V1]**
- Trace dùng prompt v2: **[BỔ SUNG TRACE ID V2]**

Dashboard dùng `data/logs.jsonl` và gồm 6 panel: latency, traffic, errors, cost, tokens và quality. Panel latency theo dõi P50/P95/P99 và TTFT; panel errors theo dõi error rate và retrieval success. Contract đạt `6/6 panel`.

SLO là `99.5%` request thành công và latency không quá `3000 ms` trong cửa sổ `28d`. Error budget là `0.5%`; với 10.000 request, tối đa 50 request được phép không đạt SLO.

Ba alert là `HighLatencyP95` (P95 > 3000 ms trong 5 phút), `HighErrorRate` (error rate > 2% trong 5 phút) và `LowRetrievalSuccess` (retrieval success < 90% trong 10 phút). Runbook nằm tại [docs/alerts.md](../docs/alerts.md).

Evidence dashboard validator: [03-dashboard-validator.png](evidence/03-dashboard-validator.png). Ảnh trace, prompt và dashboard runtime cần bổ sung tại `evidence/06`–`evidence/11`.

## 6. Checkpoint 3 — Điều tra challenge

Challenge `day13-k4-l3b-monitoring-llmops-v1` bật incident `rag_slow`, affected feature là `monitoring`, threshold `2000 ms`.

Metrics ghi nhận traffic `5`, latency P50 `2978 ms`, P95 `7125 ms`, P99 `7125 ms`, TTFT P95 `51 ms` và quality average `0.84`. Request đại diện là `req-c5e977df`, session `k4-l3b-challenge-s02`, có `response_sent.latency_ms=7125`, `tool_name=retrieval` và `tool_success=true`.

Root cause là `rag_slow`: `app/mock_rag.py::retrieve()` thực hiện `time.sleep(2.5)`. TTFT vẫn khoảng `50 ms` và retrieval không fail, nên retrieval là span gây chậm, không phải LLM generation. Fix action là tắt `rag_slow`, khôi phục retrieval path và chạy lại workload. Preventive measure là duy trì alert `HighLatencyP95`, lọc log theo correlation ID và mở trace để xác định span.

Evidence chi tiết: [15-cp3-incident-note.md](evidence/15-cp3-incident-note.md). Ảnh metric, log và trace cần bổ sung tại `evidence/12`, `evidence/13`, `evidence/14`.

## 7. Quyết định kỹ thuật và blocker

Quyết định quan trọng là scrub PII trước khi serialize thay vì sau khi file đã được ghi, bảo đảm dữ liệu nhạy cảm không xuất hiện trong structured log hoặc trace preview.

Một số test dùng `tmp_path` bị Windows từ chối quyền truy cập thư mục tạm pytest. Các test logic tracing/prompt đã đạt `7 passed`; dashboard validator độc lập đạt `6/6 panel`.

## 8. Checklist trước khi nộp

- [ ] Bổ sung họ tên, MSSV, URL repository và commit SHA.
- [ ] Bổ sung `01-pytest.png` và `05-pii-redaction.png`.
- [ ] Bổ sung evidence Langfuse `06`–`10` và trace ID v1/v2.
- [ ] Bổ sung ảnh dashboard runtime `11`.
- [ ] Bổ sung incident images `12`, `13`, `14`.
- [ ] Chạy lại tests và validators trên commit cuối.
- [ ] Không commit `.env`, secret, PII thô, log JSONL hoặc `config/challenge.json`.
