from __future__ import annotations

import re
from typing import Iterable, List


def simple_markdown_to_text(md: str) -> str:
    # strip code fences and images/links to text
    md = re.sub(r"```[\s\S]*?```", " ", md)
    md = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", md)
    md = re.sub(r"\[[^\]]*\]\([^\)]*\)", " ", md)
    # headers and emphasis
    md = re.sub(r"[#*_>`]+", " ", md)
    return md


def chunk_text(text: str, chunk_chars: int = 1200, overlap: int = 200) -> List[str]:
    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_chars, n)
        # try to break at nearest sentence end
        window = text[start:end]
        m = re.search(r"[\.\?\!]\s", window[::-1])
        if m and end - (m.start() + 1) > start + 200:
            end = end - (m.start() + 1)
        chunks.append(text[start:end].strip())
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks


def count_tokens_approx(s: str) -> int:
    # Rough heuristic: ~4 chars per token
    return max(1, len(s) // 4)

