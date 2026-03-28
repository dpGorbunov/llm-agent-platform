"""Model router - maps model names to providers via balancer strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException

from src.balancer.round_robin import RoundRobinStrategy
from src.providers.registry import provider_registry

if TYPE_CHECKING:
    from src.balancer.base import BalancerStrategy
    from src.providers.models import Provider
    from src.providers.registry import ProviderRegistry


class ModelRouter:
    """Routes model requests to providers using a configured strategy."""

    def __init__(
        self,
        registry: ProviderRegistry | None = None,
        strategy: BalancerStrategy | None = None,
    ) -> None:
        self._registry = registry or provider_registry
        self._strategy = strategy or RoundRobinStrategy()

    async def route(self, model: str) -> Provider:
        """Select a provider for the given model.

        Raises HTTPException 404 if no providers serve this model.
        """
        providers = await self._registry.get_providers_for_model(model)
        if not providers:
            raise HTTPException(
                status_code=404,
                detail=f"No providers available for model: {model}",
            )
        return self._strategy.select_provider(providers)


model_router = ModelRouter()
