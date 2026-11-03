# Cryptonite Engine

A Python-based distributed crypto-intelligence compute engine. The current codebase combines ledger normalization, wallet and token analysis, market signals, network pipelines, asynchronous workers, and PostgreSQL / Neo4j / Redis infrastructure.

> **Project status:** this repository contains the engine modules and worker infrastructure. It does not currently expose a documented public HTTP API or a production deployment guide.

## Architecture at a glance

- **Domain** — ledger mapping and normalization, token analysis, wallet scoring, market signals, and shared utilities.
- **Pipelines** — wallet, token, signal, and network processing.
- **Workers** — Celery tasks for ingestion, metrics, graph, contract, market, signal, and orchestration workloads.
- **Infrastructure** — SQLAlchemy async PostgreSQL sessions, Neo4j connectivity, Redis configuration, and application settings.
- **Events and models** — event publishers/subscribers and ML feature/model registry modules.

## Requirements

- Python 3.11+
- Docker Engine and Docker Compose (for the local service stack)

The Python dependencies and development tools are declared in `pyproject.toml`.

## Local setup

Create and activate a virtual environment, then install the project with its development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The application settings are loaded from environment variables and optionally from a root-level `.env` file. The current defaults are:

| Variable | Default |
| --- | --- |
| `POSTGRES_DSN` | `postgresql+asyncpg://postgres:postgres@localhost:5432/cryptonite` |
| `NEO4J_DSN` | `neo4j://neo4j:password@localhost:7687` |
| `REDIS_URL` | `redis://localhost:6379/0` |
| `CELERY_BROKER` | `redis://localhost:6379/1` |
| `CELERY_BACKEND` | `redis://localhost:6379/2` |

For non-local environments, replace the development credentials and connection strings with managed secrets. Do not commit real credentials or production `.env` files.

## Start the local infrastructure

From the repository root:

```bash
docker compose -f docker/docker-compose.yml up --build
```

The Compose stack defines:

- PostgreSQL 16 on port `5432`
- Neo4j 5 Community on ports `7474` (browser) and `7687` (Bolt)
- Redis 7 on port `6379`
- A Celery worker subscribed to the configured task queues
- Celery Beat

Stop the stack with:

```bash
docker compose -f docker/docker-compose.yml down
```

Add `-v` only when you intentionally want to remove the persisted PostgreSQL and Neo4j volumes.

## Run tests and lint

Run the test suite:

```bash
pytest
```

Run Ruff:

```bash
ruff check .
ruff format --check .
```

The tests currently cover domain logic and pipeline behavior. Integration tests in this repository exercise pipeline composition; they should not be confused with tests against live PostgreSQL, Neo4j, or Redis services.

## Repository layout

```text
apps/             Infrastructure bootstrap
domain/           Ledger, market, token, wallet, and shared domain logic
events/           Event types, publishers, and subscribers
infrastructure/   Database, graph database, cache, and configuration
models/            ML feature extractors, wrappers, and registry
pipelines/         Wallet, token, signal, and network pipelines
workers/           Celery task modules
docker/            Dockerfile and local Compose stack
tests/             Domain and pipeline tests
```

## Development notes

1. Keep business rules in `domain/` and pipeline orchestration in `pipelines/`.
2. Keep external service access in `infrastructure/`.
3. Add or update focused tests when changing domain or pipeline behavior.
4. Keep credentials out of source control; use environment configuration for local and deployed environments.
5. Document operational assumptions whenever adding a worker, queue, or infrastructure dependency.
