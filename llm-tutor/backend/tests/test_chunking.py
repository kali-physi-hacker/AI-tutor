from app.services.chunking import chunk_text, count_tokens_approx


def test_chunker_basic():
    text = "This is a test. " * 200
    chunks = chunk_text(text, chunk_chars=200, overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 220 for c in chunks)


def test_token_count():
    s = "abcd" * 10
    assert count_tokens_approx(s) == 10

