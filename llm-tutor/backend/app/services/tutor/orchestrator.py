from __future__ import annotations

import asyncio
from typing import AsyncGenerator


async def stream_tutor_response(db, chat_id: int) -> AsyncGenerator[str, None]:
    # Minimal simulated stream for MVP dev
    text = "Thinking about your question and retrieving context..."
    for token in text.split(" "):
        await asyncio.sleep(0.05)
        yield f"data: {token}\n\n"
    yield "event: done\n\n"

