import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel, Field

from .service import RAGService

app = FastAPI(title="Enterprise Multi-Cloud GenAI RAG Platform", version="1.0.0")
service = RAGService()
QUERIES = Counter("rag_queries_total", "RAG queries", ["grounded"])
LATENCY = Histogram("rag_query_latency_seconds", "RAG query latency")
app.mount("/metrics", make_asgi_app())


class Query(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    tenant_id: str = Field(default="demo", pattern=r"^[a-z0-9-]{1,64}$")


@app.middleware("http")
async def secure_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.update({"X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Cache-Control": "no-store"})
    return response


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready", "indexed_chunks": len(service.index.chunks)}


@app.post("/v1/query")
def query(payload: Query):
    started = time.perf_counter()
    try:
        result = service.answer(payload.question, payload.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    QUERIES.labels(str(result["grounded"]).lower()).inc()
    LATENCY.observe(time.perf_counter() - started)
    return result | {"request_id": str(uuid.uuid4()), "prompt_version": "rag-v1"}
