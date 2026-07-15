*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Project Planning
*Epics, stories, and estimated effort*

---

## Planning Approach

Work was broken into 6 epics, each containing 3-5 stories, sized in story-points/time estimates, and sequenced so that infrastructure (Epic 1) precedes feature logic (Epics 2-4), which precedes hardening and release (Epics 5-6).

## Epic Breakdown & Duration

- Epic 1 — Application Development & System Setup (4h): Python/React environment, dependency installation, project structure.
- Epic 2 — AI Integration & Financial Processing Setup (4h): FastAPI endpoints, Financial Engine, Settlement Prediction, AI Negotiation Engine, Fallback Logic.
- Epic 3 — Database Management & Financial Data Storage Setup (2h 30m): API development functionality, loan/settlement processing, data handling.
- Epic 4 — Frontend Integration & UI Development (3h): UI build, FastAPI communication, financial data visualization, UI enhancements.
- Epic 5 — Testing, Debugging & Performance Optimization (2h): system testing, error handling/fallback management, performance and session security.
- Epic 6 — Version Control, Finalization & Deployment Readiness (2h): GitHub setup, cleanup, deployment configuration.

## Total Estimated Effort

Approximately 17.5 hours across all six epics, tracked story-by-story in the project workspace Kanban board.

## Sequencing Rationale

Backend environment and database models were built first since every later feature (financial engine, settlement engine, AI engine) depends on the ORM models and API scaffolding being in place.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
