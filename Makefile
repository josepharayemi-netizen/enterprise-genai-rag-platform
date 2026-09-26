.PHONY: ingest evaluate test lint run docker
ingest:
	python -m src.rag_platform.cli ingest examples/knowledge
evaluate: ingest
	python -m src.rag_platform.cli evaluate evaluation/golden_set.json
test:
	pytest -q
lint:
	ruff check src tests
run: ingest
	uvicorn src.rag_platform.api:app --reload
docker:
	docker compose up --build
