*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Project Demo Planning
*Logistics and preparation for the demo session*

---

## Pre-Demo Checklist

- Backend running via uvicorn on port 8000 with a fresh finrelief.db (or seeded via seed_demo_data.py).
- Frontend running via `npm run dev` on port 5173, pointed at the backend through VITE_API_BASE_URL.
- Decide in advance whether to demo with a live GEMINI_API_KEY or the fallback path, and prepare talking points for both.
- Have 2-3 example loans ready to add quickly rather than typing them live from scratch.

## Estimated Demo Duration

10-12 minutes: ~2 minutes problem framing, ~7 minutes live walkthrough of the 7-step demo flow, ~2-3 minutes Q&A.

## Risk Mitigation

If the Gemini API is unreachable during the live demo (network restrictions, quota), the rule-based fallback ensures the negotiation-letter feature still works without any visible failure.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
