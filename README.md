# Component Prices

A containerised Python application that tracks daily prices of PC components across Polish online shops and stores them in a PostgreSQL database for historical analysis.

---

## Project Goal

Provide a reliable, automated price-history store for PC components. On each scheduled run the scraper fetches the current price of every tracked component from every tracked shop and persists a timestamped record. A price chart for any component can then be rendered from the stored records.

---

## MVP Scope

| Feature | Included in MVP |
|---|---|
| Track two components (Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6, AMD Ryzen 9 5950X) | ✅ |
| Track a single shop (x-kom.pl) | ✅ |
| Daily price collection via cron job | ✅ |
| Persist prices in PostgreSQL | ✅ |
| Price chart (tabular / time-series query) | ✅ |
| Multi-component / multi-shop support | Post-MVP |
| Web UI / dashboard | Post-MVP |
| Price-drop alerts | Post-MVP |

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│  Host / CI scheduler                                 │
│  cron: 0 9 * * *  →  docker compose run scraper      │
└────────────────────────┬─────────────────────────────┘
                         │
           ┌─────────────▼──────────────┐
           │   scraper (Python)         │
           │                            │
           │  1. Read component & shop  │
           │     records from DB        │
           │  2. HTTP GET product page  │
           │  3. Parse current price    │
           │  4. INSERT price_snapshot  │
           └─────────────┬──────────────┘
                         │  TCP 5432
           ┌─────────────▼──────────────┐
           │   postgres                 │
           │   database: component_prices│
           └────────────────────────────┘
```

Both services are managed with **Docker Compose**.  
The scraper container exits after each run (one-shot); the database container runs persistently.

---

## Data Model

All models are defined as **SQLAlchemy ORM mapped classes** in `scraper/models.py`. Schema changes are managed exclusively through **Alembic** migration scripts — the raw `init.sql` file is not used.

### `shops`

| Column | Type | Notes |
|---|---|---|
| `id` | SERIAL PK | |
| `name` | VARCHAR(255) | e.g. `x-kom` |
| `base_url` | TEXT | e.g. `https://www.x-kom.pl` |
| `created_at` | TIMESTAMPTZ | record creation time |

### `components`

| Column | Type | Notes |
|---|---|---|
| `id` | SERIAL PK | |
| `name` | VARCHAR(255) | e.g. `Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6` |
| `category` | VARCHAR(100) | e.g. `GPU` |
| `created_at` | TIMESTAMPTZ | record creation time |

### `component_shop_urls`

Joins a component to a shop and stores the exact product-page URL to scrape.

| Column | Type | Notes |
|---|---|---|
| `id` | SERIAL PK | |
| `component_id` | INT FK → components | |
| `shop_id` | INT FK → shops | |
| `product_url` | TEXT | full product page URL |
| `active` | BOOLEAN | set to false to pause scraping |

### `price_snapshots`

One row per component-shop-day.

| Column | Type | Notes |
|---|---|---|
| `id` | BIGSERIAL PK | |
| `component_shop_url_id` | INT FK → component_shop_urls | |
| `price_pln` | NUMERIC(10,2) | price in PLN at time of scrape |
| `currency` | CHAR(3) | always `PLN` for x-kom |
| `scraped_at` | TIMESTAMPTZ | exact timestamp of the HTTP request |
| `date` | DATE | derived from `scraped_at`; used for daily deduplication |

Unique constraint on `(component_shop_url_id, date)` — only one price record per component-shop pair per calendar day.

---

## Seeded MVP Data

On first startup Alembic applies all pending migrations, then a seed script (idempotent, using `INSERT … ON CONFLICT DO NOTHING`) populates:

**Shop**
- name: `x-kom`
- base_url: `https://www.x-kom.pl`

**Components**
- name: `Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6`, category: `GPU`
- name: `AMD Ryzen 9 5950X`, category: `CPU`

**component_shop_url**
- product_url: `https://www.x-kom.pl/p/1339802-karta-graficzna-amd-gigabyte-radeon-rx-9060-xt-gaming-oc-16gb-gddr6.html`
- product_url: `https://www.x-kom.pl/p/597434-procesor-amd-ryzen-9-amd-ryzen-9-5950x.html`

---

## Scraper Behaviour

1. **Startup** — connect to PostgreSQL; wait for readiness with exponential back-off.
2. **Fetch targets** — query all `component_shop_urls` where `active = true`.
3. **Scrape** — for each target, send an HTTP GET request with a realistic `User-Agent` header.
4. **Parse** — locate the price element in the HTML response using CSS selectors or XPath. Extract numeric value; strip currency symbol.
5. **Persist** — `INSERT … ON CONFLICT DO NOTHING` using the unique constraint on `(component_shop_url_id, date)`, so re-runs on the same day are idempotent.
6. **Exit** — log summary; exit 0 on success, non-zero on failure so the cron host can alert.

## Project Setup

The project is managed with **uv**. All runtime and development dependencies are declared in `pyproject.toml`.

```bash
# install all dependencies (including dev extras)
uv sync --all-extras

# run linter + formatter check
uv run ruff check .
uv run ruff format --check .

# run type checker
uv run pyright

# run tests
uv run pytest

# apply migrations (inside the scraper container or locally against a running DB)
uv run alembic upgrade head
```

The `pyproject.toml` configures `ruff` and `pyright` directly — no separate config files are needed.

---

## Migrations

Alembic is the sole mechanism for all schema changes.

```
migrations/
├── env.py           # imports SQLAlchemy metadata from models.py
├── script.py.mako   # migration template
└── versions/        # auto-generated revision files
```

Workflow for schema changes:

1. Edit the SQLAlchemy model in `scraper/models.py`.
2. `uv run alembic revision --autogenerate -m "description"` to generate a migration.
3. Review the generated file under `migrations/versions/`.
4. `uv run alembic upgrade head` to apply.

The scraper container runs `alembic upgrade head` automatically before executing the scrape, ensuring the schema is always up to date.

---

## Testing

Tests live in `tests/` and are executed with **pytest**.

```
tests/
├── conftest.py           # shared fixtures (DB session, HTTP mock)
├── test_scraper.py       # HTML parsing and price extraction logic
├── test_db.py            # ORM model round-trips and upsert behaviour
└── test_integration.py   # end-to-end scrape against a mock HTTP server + real DB
```

- Database tests spin up an ephemeral PostgreSQL instance via `pytest-postgresql` and run Alembic migrations before each session.
- HTTP tests mock responses with `pytest-httpx` so no real network calls are made.
- Type coverage is verified by `pyright` in strict mode as part of the CI pipeline.

---



The scraper is triggered externally via a **host-level cron job** (or a CI/CD scheduled pipeline):

```
0 9 * * *  /usr/bin/docker compose -f /opt/component_prices/docker-compose.yml run --rm scraper
```

Recommended run time: **09:00 local time daily** — after x-kom typically updates prices overnight.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Package manager | `uv` |
| HTTP client | `httpx` (async-capable, modern API) |
| HTML parsing | `beautifulsoup4` + `lxml` |
| ORM / query builder | `SQLAlchemy` (Core + ORM) |
| Migrations | `Alembic` |
| Database | PostgreSQL 16 |
| Containerisation | Docker + Docker Compose v2 |
| Scheduling | Host cron / CI scheduled job |
| Testing | `pytest` + `pytest-postgresql` (ephemeral DB per test run) |
| Linting & formatting | `ruff` |
| Type checking | `pyright` |

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `POSTGRES_HOST` | DB hostname (service name in Compose) | `db` |
| `POSTGRES_PORT` | DB port | `5432` |
| `POSTGRES_DB` | Database name | `component_prices` |
| `POSTGRES_USER` | DB user | `scraper` |
| `POSTGRES_PASSWORD` | DB password | *(secret)* |

---

## Directory Structure (planned)

```
component_prices/
├── pyproject.toml           # dependencies, ruff + pyright config, pytest config
├── docker-compose.yml
├── migrations/              # Alembic migration environment
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── scraper/
│   ├── Dockerfile
│   ├── __init__.py
│   ├── main.py              # entry point: run migrations then scrape
│   ├── scraper.py           # HTTP fetch + HTML parse
│   ├── models.py            # SQLAlchemy ORM models
│   ├── db.py                # engine / session factory
│   ├── seed.py              # idempotent seed data
│   └── config.py            # env-var loading (via pydantic-settings)
└── tests/
    ├── conftest.py
    ├── test_scraper.py
    ├── test_db.py
    └── test_integration.py
```

---

## Future Enhancements (Post-MVP)

- Support multiple components and shops via the existing data model (no schema changes required).
- Lightweight web UI (e.g. Streamlit or FastAPI + Chart.js) to visualise price charts.
- Price-drop notification via e-mail or Telegram.
- Configurable scrape schedule per shop.
- Proxy rotation and rate-limiting to avoid bot-detection blocks.
