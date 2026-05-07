.PHONY: run stop test lint format build logs clean

# ── Local stack ────────────────────────────────────────────────────────────────
run:
	docker compose up --build

stop:
	docker compose down

# ── Testing ───────────────────────────────────────────────────────────────────
test:
	docker compose run --rm app pytest tests/ -v

# Run tests locally without Docker (requires local venv + DB/Redis)
test-local:
	pytest tests/ -v

# ── Code quality ──────────────────────────────────────────────────────────────
lint:
	ruff check .

format:
	ruff format --check .

format-fix:
	ruff format .

# ── Docker ────────────────────────────────────────────────────────────────────
build:
	docker compose build

logs:
	docker compose logs -f app

# ── Health check ──────────────────────────────────────────────────────────────
health:
	curl -s http://localhost:8000/health | python -m json.tool

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	docker compose down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
