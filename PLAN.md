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

## EXPANDED SCOPE — Demir's senior-level problem awareness

Demir je sam imenovao **prave senior probleme** koje Sophie/Prospera ima u produkciji. Pokrivamo ih u kodu:

| Problem | Šta to znači | Kad gradimo |
|---|---|---|
| **Temporal weighting** | "Bio anksiozan 5 god, sad nije" — recency decay | Wed |
| **Memory / state** | Šta sistem zna o klijentu kroz vrijeme | Tue |
| **Suppression** | "Već poslao isti signal pre 3 dana, ne ponavljaj" | Tue |
| **Multi-tenant isolation** | Advisor A ne smije vidjeti podatke advisor-a B | Tonight |
| **Bulk onboarding** | Kako prebaciti 1100 advisora bez downtime-a | Tue |
| **Score combination** | Confidence × recency × advisor preference | Wed |
| **A/B advisor prefs** | Neki advisori žele sve signale, neki high-confidence only | Tonight |
| **Stale data handling** | Email od pre 6 mjeseci nije isti signal kao danas | Wed |
| **Backfill vs incremental** | Onboarding = sve istorijski + live | Tue |
| **Rate limiting per tenant** | 1 advisor ne smije pojesti sve LLM cikluse | Tue |

Ovi problemi razdvajaju **mid kandidate** od **senior kandidata** u Sergio očima.

---

## PRISTUP — CODE-FIRST + INSTANT VERBAL (Demir's learning style)

Demir uči **kroz pravljenje + testiranje**, ne kroz suvi teoretski drill (boring + ne ostaje).

**Posle SVAKE pattern koju izgradimo:**
1. **Build** (15-30 min) — pišem kod
2. **Test** (5 min) — pokrenem, vidim da radi
3. **Verbal walkthrough** (5-10 min) — TI objašnjavaš MENI na ENGLESKOM kao da sam Sergio
4. Feedback + talking-point fraze za zapamtiti

Tako gradimo **fluency + dubinsko razumijevanje** istovremeno, bez dosade.

Sav drugi verbal drill (auth, real LLM, deployment, cloud) — **kompaktno u ČET mock interview**.

---

## SPRINT PLAN — DEADLINE PETAK 6 PM

Cilj: završiti SVE do **petak 18:00**. Interview poslije.

### TONIGHT (Mon eve 2026-05-11) — 2-2.5h
- ✅ DLQ završeno
- 🔲 **Circuit breaker** (30 min build + 10 min verbal)
- 🔲 **Multi-tenant enforcement** (45 min build + 10 min verbal)
- 🔲 **Tenant config tabela** + 5 min verbal (35 min)
- 🔲 Commit + push

### TUE 2026-05-12 (Day 3) — 4-5h
- ✅ Active recall recap (4/6 čvrsto, 2 gap)
- ✅ HTML prep doc redesigned (27 patterns + glossary + flashcards)
- ✅ Bulk schemas (`BulkOnboardRequest`, `BulkOnboardResponse`)
- ✅ `POST /onboard` endpoint code (added, not yet tested)
- 🔲 Test POST /onboard
- 🔲 **Mock CONNECTOR layer** (Gmail, Salesforce, Calendar) — Demir's key learning ask
- 🔲 **Rate limiting per tenant** (45 min build + 10 min verbal)
- 🔲 **Suppression rules** (45 min build + 10 min verbal)
- 🔲 **Client memory tabela** (45 min build + 10 min verbal)
- 🔲 Commit + push

### IMPORTANT — Demir explicit ask 2026-05-12

**Build mock connectors end-to-end to UNDERSTAND the full Sophie flow.**

Demir needs to see HOW connectors actually work, not just the API endpoints. Plan:

1. **Create `app/connectors/` directory**
2. **Base connector class** (`base_connector.py`) — shared loop, error handling, POST to Sophie
3. **Mock connector per source** (~30 lines each):
   - `mock_gmail_connector.py` — reads from `fixtures/gmail_emails.json`, transforms to canonical, POSTs to `/onboard`
   - `mock_salesforce_connector.py` — reads from `fixtures/sf_notes.json`
   - `mock_calendar_connector.py` — reads from `fixtures/calendar_events.json`
4. **Fixtures** — JSON files with fake but realistic source data (50-100 records per source)
5. **Run all connectors** + verify events flow through to worker → done status
6. **Webhook handler** (single-email flow) — `POST /webhooks/gmail` shows real-time path

**Why this matters:** Without mock connectors, Demir doesn't have intuition for HOW data gets in. With them, he can explain the entire E2E flow with confidence to Sergio.

**Sergio talking point unlocked:** *"My connectors share a base class — loop, error handling, OAuth lookup, POST to Sophie. Each source-specific connector is ~30 lines: client creation + transform. Adding a new source is a one-day task."*

### WED 2026-05-13 (Day 4) — 4-5h
- 🔲 **Temporal weighting** (1h build + 10 min verbal)
- 🔲 **Multi-agent orchestration** (1.5h build + 15 min verbal)
- 🔲 **Score combination** (45 min build + 10 min verbal)
- 🔲 **Sophie arhitektura drill** (1h verbal — crtanje + objašnjenje na engleskom)
- 🔲 Commit + push

### THU 2026-05-14 (Day 5) — 4-5h
- 🔲 **Observability** (45 min build) — strukturirani logs + counters
- 🔲 **PravoAI story v2 polish** (1h verbal) — engleski narrative
- 🔲 **Breadth verbal drill** (1h) — auth, real LLM SDK, vector DB, deployment, cost
- 🔲 **MOCK INTERVIEW** (1.5-2h) — full simulacija sa feedback-om

### FRI 2026-05-15 — do 18:00
- 🔲 **Jutro (~2h):** ponovo PravoAI story + Sophie arhitektura naglas
- 🔲 **Popodne (~2h):** breadth questions drill (sve crveno iz tabele)
- 🔲 **18:00:** kraj prep-a, odmori se do intervjua
- 🔲 Interview sa Sergio (vrijeme TBD, vjerovatno popodne/veče)

**Ukupno preostalog rada: ~15-18h kroz 5 sesija.** Realističan workload za nekoga ko stvarno gura.

---

## EXPANDED TALKING POINTS — sa novim scope-om

### Temporal weighting
> *"Signal recency matters. A 'client seems anxious' signal from yesterday isn't the same as one from 5 years ago. I implement exponential decay — `final_score = base_score × e^(-λ × age_days)`. Old signals fade naturally; recent ones dominate."*

### Suppression / anti-fatigue
> *"Anti-fatigue is critical for advisor trust. If I sent the same signal type 3 days ago, I won't re-send it. Per (advisor, client, signal_type) cooldown tracked in `last_signaled_at`. Tunable per advisor preference."*

### Multi-tenant + onboarding 1100 advisors
> *"Bulk onboarding goes in phases: pilot 50, ramp 500, full 1100. Each batch is idempotent — re-runnable on partial failure. Per-tenant rate limit prevents a single advisor's backfill from starving live traffic. Tenant_id enforced at query level — no shared state across advisors."*

### Score combination
> *"Final score combines multiple inputs: LLM confidence × temporal_decay × advisor_sensitivity. The LLM is one input, not the entire decision. Production-realistic — the model doesn't decide alone, the system does."*

### Client memory
> *"Sophie needs to remember context per client — life events, preferences, past interactions. Without memory, every signal is judged in isolation. Memory store grows incrementally as signals process."*

---

## ZAŠTO TO IMPRESIONIRA SERGIJA

Sergio na LinkedIn-u eksplicitno traži *"depth, taste, judgment, real interest in building."*

Demonstracija problema iznad pokazuje:
- **Taste** — bira pravi problem (ne samo "build CRUD")
- **Depth** — razumiješ što su **state** i **memory** u AI sistemima
- **Judgment** — koje su **tradeoff** odluke (decay rate, suppression window)
- **Real interest** — Demir je sam pomenuo: temporal weighting, memory, suppression. To je hardcore engineer thinking.

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

---

## KOMPLETAN SOPHIE PIPELINE (end-to-end) — sve što Sergio može pitati

```
1. SOURCE LAYER
   - Email (Gmail/Outlook API), CRM (Salesforce/HubSpot), Calendar
   - Documents, News feeds, Transactions
                            ↓ POST /event
2. INGESTION LAYER
   - Pydantic validation                ✅
   - Idempotency (event_id)             ✅
   - Multi-tenant tag                   🔲 sutra
   - Rate limit per tenant              🔲 sutra
   - Bulk endpoint                       🔲 sutra
                            ↓
3. STORAGE / QUEUE
   - SQLite events table                ✅
   - Status state machine               ✅
   - Audit log                          🟡 verbal
                            ↓ worker pop
4. EXTRACTION (Agent 1)
   - LLM call: structured signal        ✅ mock
   - Token counting / cost              🟡 verbal
                            ↓
5. SCORING (Agent 2)
   - LLM: "is this a moment?"           ✅ mock
   - Vector similarity (RAG)            🟡 verbal (PravoAI)
   - Reranking                          🟡 verbal (PravoAI)
                            ↓
6. CONTEXTUAL FILTERING
   - Temporal weighting (decay)         🔲 sri
   - Client memory lookup               🔲 sutra
   - Suppression / anti-fatigue         🔲 sutra
   - Advisor sensitivity prefs          🔲 sutra
                            ↓
7. NOTIFICATION (Agent 3)
   - Channel selection                  🟡 verbal
   - Format recommendation              🟡 verbal
   - Audit log                          🟡 verbal
                            ↓
                         ADVISOR
```

---

## ALL PATTERNS CHECKLIST — Sergio bi mogao pitati o bilo čemu od ovoga

| Pattern | Status | Source |
|---|---|---|
| Pydantic schema validation | ✅ | moments |
| Idempotency (PK + read-before-write) | ✅ | moments |
| Parameterized queries | ✅ | moments |
| Sync/async/background decision | ✅ | moments |
| Decoupled architecture (API/worker) | ✅ | moments |
| Polling queue | ✅ | moments |
| Mock with deliberate failures | ✅ | moments |
| Retry + exp backoff + jitter | ✅ | moments |
| Dead Letter Queue | ✅ | moments |
| Circuit breaker (open/half-open/closed) | ✅ | moments |
| Rate limiting (token bucket) | 🔲 | sutra |
| Bulk onboarding | 🔲 | sutra |
| Suppression / anti-fatigue | 🔲 | sutra |
| Client memory store | 🔲 | sutra |
| Temporal weighting (exponential decay) | 🔲 | sri |
| Multi-agent orchestration | 🔲 | sri |
| Score combination | 🔲 | sri |
| Multi-tenant isolation | 🔲 | sutra |
| Observability (logs/metrics) | 🔲 | čet |
| Hybrid search (BM25 + dense) | 🟡 verbal | PravoAI |
| Reranking (cross-encoder) | 🟡 verbal | PravoAI |
| Citation grounding | 🟡 verbal | PravoAI |
| RAG evaluation framework | 🟡 verbal | PravoAI |
| Vector DB (pgvector) | 🟡 verbal | PravoAI |
| Auth/RBAC multi-tenant | 🟡 verbal | — |
| Audit logging compliance | 🟡 verbal | — |
| Cost optimization (LLM) | 🟡 verbal | — |
| Real Anthropic SDK patterns | 🟡 verbal | — |

**Cifre:**
- Već u kodu: **10** patterns
- Dodaćemo u kodu: **9** patterns
- Verbal coverage: **9** patterns
- **Ukupno: 28 patterns. Pokrivaš sve.**

---

## VERBAL TALKING POINTS BANK (sa PravoAI bazom)

### Embeddings + Vector DB
> *"PravoAI uses pgvector with HNSW index. Documents chunked at ~500 tokens with 100 token overlap. Embedding model: text-embedding-3-large."*

### Hybrid search
> *"BM25 for keyword + dense retrieval for semantic. Reciprocal Rank Fusion to combine. RRF beats weighted sum because it's score-distribution-agnostic."*

### Reranking
> *"Top 50 from hybrid retrieval → cross-encoder rerank → top 5 to LLM. Cross-encoder is slower but much higher precision than bi-encoder alone."*

### Citation grounding
> *"LLM forced to cite source chunks. Post-generation check: every claim must trace back to retrieved context. Hallucination rate ~12% → ~2%."*

### Eval framework
> *"Golden set of 200 query-answer pairs. Measured: precision@k, recall@k, faithfulness (LLM-as-judge), context relevance. Re-run after every model swap or prompt change."*

### Agentic orchestration
> *"Each agent has single responsibility. Failures isolate — if notifier breaks, signals queue up but scoring keeps going. Each scales independently. State flows through the queue, not shared memory."*

### Reliability stacked patterns
> *"Three stacked patterns: retry with exp backoff + jitter (1, 2, 4s + random jitter — prevents thundering herd), DLQ after 4 exhausted attempts (audit trail + replay), circuit breaker after 5 consecutive failures (30s cooldown, then half-open test, then closed). In-memory per worker — production would persist to Redis."*

### Real LLM patterns (Anthropic SDK)
> *"messages.create with system + user messages. Streaming for advisor UI responsiveness. Tool calling for structured outputs — JSON schema enforced by the model. Token counting via response.usage. Rate limit handling via 429 + Retry-After header. Cost tracking per tenant in a metering table."*

### Auth / multi-tenant
> *"JWT with tenant_id claim. Middleware extracts tenant from token, injects into every downstream call. Row-level: all queries filtered by tenant_id, enforced in DAL not at endpoint. Audit log per request."*

### Cost optimization at 1100 advisors
> *"Tier signals — cheap first-pass classifier (small model) filters obvious non-moments. Expensive scoring (Sonnet/Opus) only on candidates. Cache embeddings (deterministic). Batch where possible. Cost ceiling per tenant per day."*

---

## REALISTIC SUCCESS PROBABILITY

**Coverage: ~85-90%** of likely Sergio questions.

**Remaining 10-15% risk:**
1. Unexpected production-experience question (we don't have one)
2. English fluency under stress (drill heavily ČET)
3. Behavioral ("disagreement with co-founder", "biggest failure") — not yet drilled

**Mitigation:** ČET mock interview hits all three.
