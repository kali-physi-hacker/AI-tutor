from __future__ import annotations

import hashlib
import os
import struct
from abc import ABC, abstractmethod
from typing import Iterable, List

import httpx

from ..core.config import settings


class EmbeddingsClient(ABC):
    @abstractmethod
    async def embed(self, texts: Iterable[str]) -> List[List[float]]:  # 1536 dims
        ...


class FakeEmbeddings(EmbeddingsClient):
    def __init__(self, dim: int = 1536):
        self.dim = dim

    async def embed(self, texts: Iterable[str]) -> List[List[float]]:
        out: List[List[float]] = []
        for t in texts:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            # Expand hash to dim floats deterministically
            buf = (h * ((self.dim * 4 // len(h)) + 1))[: self.dim * 4]
            floats = list(struct.unpack(f"<{self.dim}f", buf))
            # Normalize
            norm = sum(x * x for x in floats) ** 0.5 or 1.0
            out.append([x / norm for x in floats])
        return out


class OpenAICompatibleEmbeddings(EmbeddingsClient):
    def __init__(self, api_key: str, base_url: str | None = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.base_url = base_url or "https://api.openai.com/v1"
        self.model = model

    async def embed(self, texts: Iterable[str]) -> List[List[float]]:
        url = f"{self.base_url}/embeddings"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, json={"model": self.model, "input": list(texts)}, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return [d["embedding"] for d in data["data"]]


def get_embeddings_client() -> EmbeddingsClient:
    provider = (settings.embeddings_provider or "fake").lower()
    if provider == "openai" and settings.openai_api_key:
        base = os.getenv("OPENAI_BASE_URL")
        return OpenAICompatibleEmbeddings(settings.openai_api_key, base_url=base)
    # Default to fake for offline dev
    return FakeEmbeddings()

