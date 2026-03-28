from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.completions import router as completions_router
from src.providers.openrouter import openrouter_client


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    await openrouter_client.close()


app = FastAPI(
    title="LLM Agent Platform",
    description="API gateway for LLM requests with load balancing, agent registry, and telemetry",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(completions_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
