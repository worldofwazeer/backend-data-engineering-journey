```markdown
# Engineering Notes: Resilient API Ingestion

## 1. Context Managers over Manual Session Closure
Manually calling `.close()` exposes a pipeline to resource leaks if an unhandled exception crashes the execution mid-flight. By wrapping `requests.Session()` within `__enter__` and `__exit__`, Python guarantees connection teardown regardless of runtime errors.

## 2. The Danger of "HTTP 200 Implies JSON"
Production proxies, API gateways (like AWS API Gateway, Cloudflare), or server maintenance modes regularly return standard `200 OK` status codes while serving text payloads or raw HTML templates. Parsing these directly with `.json()` throws ambiguous errors (`JSONDecodeError`). Verifying the presence of the MIME type beforehand (`"application/json" in header`) isolates data structure anomalies instantly.

## 3. Retaining Exception State in Loops
When handling retries inside loops, breaking or exiting an `except` block clears the active exception framework. Utilizing a dedicated tracking variable (`last_exception`) ensures that if all retries are exhausted, the client bubbles up the *original* network/HTTP root cause down the stack trace rather than crashing due to an empty context.

## 4. Global vs Local Variable Scoping
Assigning global configurations to local method boundaries (e.g., `max_retries = MAX_RETRIES`) allows methods to