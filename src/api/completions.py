"""POST /v1/chat/completions - OpenAI-compatible proxy to OpenRouter."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from src.providers.openrouter import UpstreamError, openrouter_client
from src.schemas.openai import ChatCompletionRequest  # noqa: TC001

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/v1/chat/completions", response_model=None)
async def chat_completions(request: ChatCompletionRequest) -> StreamingResponse | JSONResponse:
    kwargs = {}
    for field in ("temperature", "max_tokens", "top_p", "frequency_penalty",
                  "presence_penalty", "stop"):
        value = getattr(request, field, None)
        if value is not None:
            kwargs[field] = value

    messages = [m.model_dump(exclude_none=True) for m in request.messages]

    try:
        result = await openrouter_client.chat_completion(
            messages=messages,
            model=request.model,
            stream=request.stream,
            **kwargs,
        )
    except UpstreamError as exc:
        raise _map_upstream_error(exc) from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Upstream timeout") from exc
    except httpx.ConnectError as exc:
        raise HTTPException(status_code=502, detail="Cannot connect to upstream") from exc

    if request.stream:
        return StreamingResponse(
            _safe_stream(result),  # type: ignore[arg-type]
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

    return JSONResponse(content=result)  # type: ignore[arg-type]


async def _safe_stream(source: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """Wrap upstream stream to convert errors into SSE error events."""
    try:
        async for chunk in source:
            yield chunk
    except UpstreamError as exc:
        error_payload = {"error": {"message": exc.detail, "code": exc.status_code}}
        yield f"data: {json.dumps(error_payload)}\n\n".encode()
    except httpx.TimeoutException:
        error_payload = {"error": {"message": "Upstream timeout", "code": 504}}
        yield f"data: {json.dumps(error_payload)}\n\n".encode()
    except httpx.ConnectError:
        error_payload = {"error": {"message": "Cannot connect to upstream", "code": 502}}
        yield f"data: {json.dumps(error_payload)}\n\n".encode()


def _map_upstream_error(exc: UpstreamError) -> HTTPException:
    if exc.status_code == 429:
        return HTTPException(status_code=429, detail="Rate limit exceeded")
    if exc.status_code >= 500:
        return HTTPException(status_code=502, detail="Upstream server error")
    return HTTPException(status_code=exc.status_code, detail=exc.detail)
