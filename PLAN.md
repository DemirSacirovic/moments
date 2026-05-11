# `moments` — Sophie-inspired Signal Pipeline

Tactical practice project to internalize patterns Sergio cares about.
Built between Lina interview (2026-05-08) and Sergio interview (2026-05-15).

---

## STATUS — gdje smo (2026-05-10)

### ✅ Završeno (Day 1 — Sunday)

| # | Šta | Fajl |
|---|---|---|
| 1 | FastAPI app sa decorator-ima | `app/main.py` |
| 2 | Pydantic schemas + validacija | `app/schemas.py` |
| 3 | SQLite persistence + connection helper | `app/db.py` |
| 4 | `POST /event` endpoint | `app/main.py` |
| 5 | Idempotency (PRIMARY KEY na event_id) | `app/db.py` + `app/main.py` |
| 6 | Parameterized queries (SQL injection prevention) | `app/db.py` |
| 7 | HTTP status codes (200, 422) — testiran 422 | tested |

### 📊 Linije koda
~200 linija, sve napisano ručno (bez copy-paste), sve razumijem na nivou *"prepoznajem kad mi pokažeš"*.

---

## ARHITEKTURA — trenutno

```
┌──────────────┐     ┌──────────────┐
│ Klijent      │ POST│  FastAPI     │
│ (curl /      │ ──> │  main.py     │
│  Swagger UI) │ <── │              │
└──────────────┘ 200 └──────┬───────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ db.py        │
                    │ - find_event │  ← idempotency check
                    │ - insert     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ moments.db   │
                    │ (SQLite)     │
                    └──────────────┘
```

---

## ARHITEKTURA — gdje idemo

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Klijent      │ ──> │  API         │ ──> │ DB / Queue   │
└──────────────┘     │  (main.py)   │     │ (events tbl) │
                     └──────────────┘     └──────┬───────┘
                                                 │ pop
                                                 ▼
                                          ┌──────────────┐
                                          │ Worker       │
                                          │ (worker.py)  │
                                          │ - mock LLM   │
                                          │ - retry      │
                                          │ - DLQ        │
                                          └──────────────┘
```

---

## KONCEPTI — gdje sam svjesno

### 🟢 Razumijem (mogu objasniti svojim riječima)

- **FastAPI request lifecycle** — decorator → potpis → tijelo
- **Pydantic schemas** — `BaseModel`, `Field`, `Enum`, validacija
- **Klasa vs instanca** — klasa = nacrt, instanca = stvarna stvar
- **HTTP statusi** — 200, 422, 404
- **Idempotency** — isti event_id → isti job_id (PRIMARY KEY)
- **Mutable default gotcha** — `default_factory=dict` umjesto `default={}`
- **Case sensitivity u Pythonu**

### 🟡 Razumijem djelimično (treba još jedan-dva prolaska)

- **Parameterized queries** — znam pravilo (`?` placeholder), mehanizam tek hvatam
- **Sync vs async vs background** — koncept jasan, decision tree treba praksu
- **Mutable default factory** — pravilo OK, *zašto* još nije skroz
- **`response_model` vs `-> Type`** — funkcionalnost OK, kad koristiti šta još mut

### 🔴 Tek upoznajem (sutra)

- **Background worker pattern** — koncept skiciran, nije u kodu
- **Queue pattern** — koncept skiciran, nije u kodu
- **Retry + exponential backoff + jitter** — nije rađeno
- **Circuit breaker** — nije rađeno
- **Dead Letter Queue (DLQ)** — nije rađeno
- **Caching** — nije rađeno
- **Multi-tenant config** — koncept jasan, kod nije
- **RAG-specific:** hybrid search, reranking, eval — nije rađeno

---

## SLEDEĆI KORACI — 4 dana do intervjua

### PON 2026-05-11 (Day 2) — ~5h
- 15 min recap + active recall (engleski)
- 30 min sync/async drill (decision matrix u praksi)
- 1.5h **Background worker skeleton** — `app/worker.py`
- 1.5h **Mock LLM** — fake LLM koji random kasni i pukne
- 1h Refactor — povezati API → queue → worker
- TEST: pošalji event → vidi da worker pokupi → vidi da update-uje status

### UTO 2026-05-12 (Day 3) — ~4h
- 15 min recap
- 1.5h **Retry + exponential backoff + jitter**
- 1h **Circuit breaker** (5 fail-ova → "open")
- 1h **DLQ** (failed events u posebnu tabelu)
- 1h **Caching** (cache LLM responses sa TTL)

### SRI 2026-05-13 (Day 4) — ~5h
- 15 min recap
- 2h **Sophie arhitektura** — drill na event-driven mental model
- 1.5h **Multi-tenant config** — tenant_id u svakom event-u
- 1h **Observability** — strukturirani logs, brojači
- 1h **Eval harness** — small golden set, precision/recall

### ČET 2026-05-14 (Day 5) — ~4h
- 1h Polish kod, README
- 1h Polish PravoAI story v2 (technical version)
- 2h **Mock interview sa Claude-om** (full simulation)

### PET 2026-05-15
- 1-2h light review ujutru
- Interview sa Sergio

---

## ŠTA TREBA REĆI U INTERVJUU — talking points sa moments

### 1. Idempotency
> *"Every POST /event includes a client-supplied event_id. I store it as PRIMARY KEY. If the same event_id arrives twice — network retry — I return the existing job_id, no duplicate processing. Idempotency at the storage layer, not just at the application layer."*

### 2. Parameterized queries
> *"Every query uses ? placeholders with a tuple of values. SQL injection is impossible by construction, not by sanitization."*

### 3. Sync vs Async vs Background (decision)
> *"Three questions: How long? What does it wait for? Does the user need an immediate answer? Background workers for >5s tasks, async for I/O-bound, sync as default for fast deterministic work."*

### 4. Validation at boundary
> *"Pydantic schemas at every API boundary. Wrong input gets 422 with a structured error response. By the time data reaches my db layer, types are guaranteed."*

### 5. Architecture (kad bude worker)
> *"API and worker are separate processes. API publishes to a queue, worker consumes. Each can scale independently. Failures retry from the queue with backoff, and poison messages go to a DLQ."*

---

## SOPHIE PARALELA — koju treba držati u glavi

| moments (moj demo) | Sophie (Prospera) |
|---|---|
| `event_id` | `signal_id` |
| `tenant_id` | `advisor_id` |
| `client_id` | `client_id` (klijent advisora) |
| `event_type` (email/calendar/transaction) | isto |
| Mock LLM "is this a moment?" | Real multi-agent scoring |
| 1 worker (extract) | 3+ workers (extract → score → notify) |
| sqlite | Postgres + vector DB |

**Ključna paralela:** *event-driven, pull-based ingestion → queue → workers → action.*

Nije Q&A search (kao PravoAI). Nije RAG search. To je **trigger system** koji odlučuje *"WHEN to act"*, ne *"WHAT to retrieve"*.

---

## KAKO POKRENUTI — quick reference

```bash
# Aktiviraj venv
cd ~/Desktop/PROJECTS/moments
source venv/bin/activate

# Pokreni server
uvicorn app.main:app --reload

# Open browser
http://127.0.0.1:8000/docs

# DB inspekcija
sqlite3 moments.db "SELECT * FROM events"
sqlite3 moments.db ".schema"

# Brzi test
python -c "from app.db import find_event; print(find_event('test-x1'))"
```

---

## STRUKTURA FAJLOVA

```
moments/
├── PLAN.md                    ← ovaj fajl
├── README.md                  ← (TODO za petak)
├── moments.db                 ← SQLite (gitignored)
├── .env                       ← (gitignored)
├── .gitignore
├── venv/                      ← (gitignored)
├── app/
│   ├── __init__.py
│   ├── main.py                ← FastAPI endpoint-i
│   ├── schemas.py             ← Pydantic
│   ├── db.py                  ← SQLite layer
│   ├── worker.py              ← TODO ponedjeljak
│   ├── llm.py                 ← TODO ponedjeljak (mock LLM)
│   └── queue.py               ← TODO ponedjeljak (može biti dio db.py)
└── tests/
    └── __init__.py
```

---

## OPEN QUESTIONS — što još treba da se razjasni

- [ ] Sync/async u praksi: drill više primjera dok ne klikne
- [ ] Parameterized queries — *zašto* placeholder je bezbjedniji od escape-a
- [ ] Razlika thread pool (FastAPI sync handler) vs event loop (FastAPI async handler)
- [ ] Što tačno znači "Sophie je event-driven, ne query-driven" — diagram + sample flow
- [ ] Multi-agent orchestration — gdje agent A predaje agent B-u

---

## PRINCIPI KOJIH SE DRŽIMO

1. **Education mode** — Demir piše sav kod, Claude objašnjava
2. **Concept > syntax** — bolje razumjeti zašto, nego pamtiti kako
3. **Active recall** — povremeno provjera bez gledanja koda
4. **Working > complete** — bolje 70% radi nego 100% planirano-fragilno
5. **Talking points** — svaki feature mapiran u rečenicu za Sergija
6. **NIVO objašnjenja:** Demir ima 3.5 god Python iskustva + 70 kurseva. Zna koncepte, gap je u fluentnosti pisanja iz glave. NE tretirati kao početnika — objašnjavaj mehanizme, tradeoff-e, dublju logiku. Kad pita — odgovaraj precizno, ne basic.
