*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Performance Testing
*Performance and reliability validation notes*

---

## Scope

Performance testing focused on backend responsiveness, database concurrency, authentication overhead, and resilience of the AI negotiation feature when the external Gemini API is slow, unavailable, or misconfigured.

## Test Areas & Results

- SQLite concurrency: check_same_thread=False allows the single-file database to serve concurrent FastAPI requests from multiple worker threads without connection errors during local load testing.
- Password hashing cost: Werkzeug's default hashing method was verified to complete well within typical login-request timeouts on standard development hardware.
- JWT overhead: token creation/verification adds negligible latency (sub-millisecond) per request compared to database I/O.
- AI fallback latency: with no GEMINI_API_KEY configured, negotiation generation returns immediately from the rule-based path, confirming the fallback avoids any network round-trip when AI is disabled.
- AI failure handling: simulated Gemini exceptions (invalid key, network error) were confirmed to be caught and silently redirected to the fallback generator without raising a 500 error to the frontend.

## Recommendations for Production Scale

- Move from SQLite to PostgreSQL for multi-instance deployments.
- Add response caching for repeated settlement predictions on unchanged loan data.
- Introduce a request timeout and retry policy around the Gemini API call.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
