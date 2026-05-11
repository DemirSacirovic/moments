# `moments` — Sophie-inspired Signal Pipeline

Tactical practice project to internalize patterns Sergio cares about.
Built between Lina interview (2026-05-08) and Sergio interview (~2026-05-15).

---

## STATUS — gdje smo (2026-05-11 popodne)

### ✅ Day 1 (Sun 2026-05-10)
- FastAPI app + decorators
- Pydantic schemas + validation (422 testirano)
- SQLite persistence + connection helper
- `POST /event` endpoint
- **Idempotency** (PRIMARY KEY na event_id)
- **Parameterized queries** (SQL injection prevention)
- HTTP statuses (200, 422, 404)

### ✅ Day 2 (Mon 2026-05-11)
- GitHub repo setup → push (`github.com/DemirSacirovic/moments`, public)
- macOS Keychain za PAT
- **Mock LLM** (`app/llm.py`) — random delay + 15% deliberate failure
- **Queue helpers** u `db.py` — `get_next_queued_event`, `update_event_status`
- **Background worker** (`app/worker.py`) — polling loop, status state machine
- **Full e2e test** — POST /event → worker pickup → done
- 🟡 **Retry + exponential backoff + jitter** — kod napisan, NIJE testiran još

### 📊 Linije koda
~300 linija, sve napisano ručno, sve razumije na nivou *"prepoznajem"* (nivo 1-2).

---

## ARHITEKTURA — trenutno

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Klijent      │ ──> │  API         │ ──> │ moments.db   │
│ (Swagger UI) │     │  main.py     │     │ events tbl   │
└──────────────┘     │  (sync)      │     │ status field │
                     └──────────────┘     └──────┬───────┘
                                                 │ polling
                                                 ▼
                                          ┌──────────────┐
                                          │ Worker       │
                                          │ - mock LLM   │
                                          │ - retry      │
                                          │ - status     │
                                          │   transitions│
                                          └──────────────┘
```

API i worker su **odvojeni procesi**. Komunikacija kroz DB.

---

## KONCEPTI — gdje sam svjesno (post Day 2)

### 🟢 Razumijem (mogu objasniti svojim riječima)
- FastAPI request lifecycle, decorators, type hints
- Pydantic BaseModel, Field, Enum, validation, response_model
- Klasa vs instanca
- HTTP statusi (200, 422, 404, 500)
- **Idempotency** — isti event_id → isti job_id (PRIMARY KEY)
- **Parameterized queries** — separation of code and data
- Mutable default gotcha (`default_factory`)
- Case sensitivity, dunder atributi
- Decorators (concept + FastAPI use)
- Mock vs real LLM — when and why
- Status state machine (queued → processing → done/failed)

### 🟡 Razumijem djelimično
- **Sync/Async/Background decision** — 4/5 scenarija tačno, fluentnost treba
- **`if __name__ == '__main__'`** — koncept hvataš, mehanizam mut
- **Retry + backoff + jitter** — kod napisan, nije live testiran
- **Race conditions u workeru** — pomenuto, nije rješavano

### 🔴 Tek upoznajem
- Circuit breaker
- Dead Letter Queue (DLQ)
- Caching strategija
- Multi-tenant isolation
- **Sophie arhitektura** (event-driven, NE Q&A!) — najveći gap
- RAG-specific: hybrid search, reranking, eval framework
- Observability (structured logging, metrics, traces)

---

## NIVO PROJEKTA vs ŠTO ONI TRAŽE

### Patterns demonstrated → **mid-level**
Sami patterns koje sam pokrio (FastAPI, idempotency, queue, worker, retry) su mid-level. Iznad junior-a, ispod senior-a.

### Šta nedostaje da bude "senior portfolio piece"
- Async/await kroz stack (sync currently)
- Pravi message broker (Redis/RabbitMQ)
- Concurrency safety (race conditions postoje)
- Strukturirani logging + metrike (samo `print()`)
- Test suite (0 testova)
- Type checker (mypy) — nije provjereno
- Config kroz env vars + pydantic-settings
- Distributed tracing
- Real LLM + rate limiter
- Observability dashboard
- CI/CD pipeline
- Multi-tenant row-level isolation
- Eval framework za LLM

### Šta Sergio TRAŽI (procjena na osnovu Lina + JD + LinkedIn)
- **Mid-Senior backend AI** ($5-7.5k/mo — salary range)
- Generalist (5-osoblje)
- Praktično operativno (reliability, onboarding 1100 advisora)
- "Depth, taste, judgment" — NIJE leetcode
- Komunikacija + biznis razumijevanje
- Shipper, ne istraživač (već imaju paying customers)

### Gdje sam ja u poređenju
- Backend patterns: junior-mid (gap)
- AI/RAG depth: senior (PravoAI) ✅
- Pisanje iz glave: junior (gap)
- Sophie domain razumijevanje: junior (gap koji moram da popravim)
- Engineering taste: mid (raste)
- Honest komunikacija: senior ✅
- Brzina učenja: senior ✅

**Net realno:** $5-6k range, ne $7k osim ako mock interview pokaže izvanrednost.

---

## PRIORITETI ZA 4 DANA — by importance

### #1 — SOPHIE ARHITEKTURA (najveći gap, SRI)
Moj mental model je trenutno **PravoAI (Q&A search)**, ne Sophie (event-driven trigger).

Ako Sergio pita "walk me through Sophie" i ja opišem PravoAI — minus.

**Akcija (SRI 2-3h):** drill na event-driven mental model.
- Signal extraction layer
- Multi-agent orchestration (extract → score → notify)
- Personalization per-advisor
- Compliance/audit
- Crtanje arhitekture + verbalizacija na engleskom

### #2 — RELIABILITY u kodu (UTO)
Završi retry/DLQ/circuit breaker u `moments`. Talking point:
*"I implemented retry+backoff+jitter when my mock LLM fails — same pattern I'd use for real LLM API."*

**Akcija (UTO ~3h):**
- Retry test (provjeri da radi)
- DLQ tabela + flow za 3 retry-a fail-a
- Circuit breaker (5 fail-ova → open)
- Caching (opciono)

### #3 — MULTI-TENANT + 1100 ADVISORA ONBOARDING (SRI)
Lina **eksplicitno** spomenula. Sergio će sigurno pitati.

**Akcija (SRI 1.5h):**
- Tenant_id u svakom event-u (već postoji u schemi)
- Onboarding flow: kako migrirati 1100 advisora
- Data isolation strategija
- Bulk ingestion sa retry/error handling
- Plan po fazama (pilot 50 → 500 → 1100)

### #4 — RAG DEPTH (PravoAI v2 story, ČET)
Tvoja strongest play. Treba je odbraniti čisto na engleskom — brojevi, failure modes, decisions.

**Akcija (ČET 1.5h):**
- Polish 60-sek priče
- Pripremi follow-up answers (eval, hybrid search detalji, reranking, citation grounding)
- Konkretni brojevi (koliko docs, koja arhitektura, koji rezultati)

### #5 — MOCK INTERVIEW (ČET)
Full simulacija na engleskom. Claude = Sergio, ja = ja. Feedback gdje pucam.

**Akcija (ČET 2h):**
- 30 min PravoAI deep dive
- 30 min Sophie arhitektura
- 30 min reliability/scaling pitanja
- 30 min behavioral (zašto Prospera, why now, gaps)

---

## ŠTA **NE** RADITI (waste of time)

- ❌ Multi-agent sistem from scratch
- ❌ Dubok async (gubim dan, ne pita specifične primitive)
- ❌ Real LLM integracija (skupo, ne dodaje signal)
- ❌ Real message broker (overkill)
- ❌ Novi frameworki (SQLAlchemy, Celery — ostani sa znanim)
- ❌ Leetcode (Sergio ne traži)
- ❌ "I'll learn anything" mantra (show don't tell)
- ❌ Pretvarati se da je projekat senior-level

---

## TALKING POINTS — sa moments koda

### 1. Idempotency
> *"Every POST /event includes a client-supplied event_id stored as PRIMARY KEY. Retry returns existing job_id, no duplicate processing. Idempotency at the storage layer."*

### 2. Parameterized queries
> *"Every query uses ? placeholders. SQL injection impossible by construction, not by sanitization."*

### 3. Sync/Async/Background decision
> *"Three questions: how long, what does it wait for, does the user need an immediate answer."*

### 4. Validation at boundary
> *"Pydantic at every API boundary. Wrong input gets 422 with structured errors. By db layer, types guaranteed."*

### 5. API/Worker decoupling
> *"API and worker are separate processes. API publishes via DB, worker polls. Each scales independently. Failures retry from queue, poison messages to DLQ."*

### 6. Deliberate failure for testing reliability
> *"My mock LLM fails 15% of the time on purpose. Real LLM almost never fails on a test bench — but I needed deterministic failures to validate retry/backoff. In production I'd swap mock with the real client behind the same interface."*

### 7. (Posle SRI) Sophie architecture
> *"Sophie is event-driven, not query-driven. Signal sources → ingestion → extraction → scoring → notification. The hard part isn't the LLM — it's the signal layer and personalization per advisor."*

---

## SOPHIE PARALELA — `moments` ↔ Sophie

| moments (demo) | Sophie (Prospera) |
|---|---|
| `event_id` | `signal_id` |
| `tenant_id` | `advisor_id` |
| `client_id` | `client_id` (klijent advisora) |
| `event_type` (email/calendar/transaction) | isto |
| Mock LLM "is this a moment?" | Real multi-agent scoring |
| 1 worker (extract) | 3+ workers (extract → score → notify) |
| sqlite | Postgres + vector DB |
| Polling (2s) | Real broker (push) |
| `print()` | OpenTelemetry, structured logs |
| Single tenant DB | Row-level multi-tenant isolation |

**KLJUČ:** event-driven, pull-based ingestion → queue → workers → action.
NIJE Q&A (kao PravoAI). NIJE RAG search. To je **trigger system** koji odlučuje *"WHEN to act"*.

---

## STRATEGIJA U INTERVJUU

1. **Honest gap framing** — Sergio detektuje BS u 30 sekundi
2. **PravoAI depth prvo** — strongest play
3. **Sophie arhitektura razumijevanje** — pokazi event-driven, ne search
4. **Multi-tenant konkretan plan** — ako pita za 1100 advisora
5. **Ne snižuj $7k anchor** — *"That's where I'm at. Understand if scope lands lower."*
6. **Pitanja za njega** — radoznalost, ne pretenzija
7. **Brzina učenja** — *"This in 5 days, here's what I built and what I learned"*

---

## KAKO POKRENUTI — quick reference

```bash
# Setup
cd ~/Desktop/PROJECTS/moments
source venv/bin/activate

# Terminal 1: API
uvicorn app.main:app --reload

# Terminal 2: Worker
python -m app.worker

# Terminal 3: Slobodan za komande
sqlite3 moments.db "SELECT * FROM events"
sqlite3 moments.db ".schema"

# Open browser
http://127.0.0.1:8000/docs
```

---

## STRUKTURA FAJLOVA

```
moments/
├── PLAN.md                    ← ovaj fajl (master plan)
├── README.md                  ← TODO za petak
├── moments.db                 ← SQLite (gitignored)
├── .env                       ← gitignored
├── .gitignore
├── venv/                      ← gitignored
├── app/
│   ├── __init__.py
│   ├── main.py                ← FastAPI endpoint-i
│   ├── schemas.py             ← Pydantic
│   ├── db.py                  ← SQLite layer + queue helpers
│   ├── worker.py              ← Background worker
│   └── llm.py                 ← Mock LLM
└── tests/
    └── __init__.py            (prazno)
```

---

## OTVORENA PITANJA (still mut)

- [ ] Sync/async u praksi — više drill-a
- [ ] `if __name__ == "__main__"` — mehanizam (parked, neće biti u intervjuu duboko)
- [ ] Concurrency safety u worker-u (mogući race condition)
- [ ] Pravi LLM integration (mock works for now)
- [ ] Sophie architecture mental model (urgent fix Wed)

---

## SLEDEĆI KORAK — kad se vratim sa pauze (Mon eve 2026-05-11)

1. **10 min:** retry test (pošalji 5 event-a, vidi retry print-ove)
2. **45 min:** DLQ pattern (failed posle 3 retry-a → posebna tabela ili column)
3. **30 min:** Circuit breaker (5 consecutive fails → open state, skip processing)
4. **Pauza ili kraj dana**

Sutra (UTO):
- Caching (opciono)
- SRI plan finalization
- Početak Sophie arhitektura drill-a

---

## PRINCIPI

1. Education mode — Demir piše kod, Claude objašnjava
2. Concept > syntax
3. Active recall — periodic provjera bez koda
4. Working > complete
5. Talking points — svaki feature mapiran u rečenicu
6. **NIVO objašnjenja:** Demir 3.5 god Python + 70 kurseva. Zna koncepte, gap je fluentnost. NE tretirati kao početnika — mehanizmi, tradeoff-i, dublja logika. Precizno, ne basic.
