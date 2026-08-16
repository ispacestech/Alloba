"""Context trimming — keep only the most relevant snippets within a token budget."""


def _estimate_tokens(text: str) -> int:
    """Cheap token proxy: split on whitespace and count words."""
    return len(text.split())


def optimize_context(retrieved_snippets: list[dict], token_limit: int) -> list[dict]:
    """Trim a list of retrieved snippets to a token budget.

    Snippets are assumed to be dicts carrying ``score`` and ``snippet`` keys.
    They are sorted by relevance (descending) and appended until the budget is
    exhausted.
    """
    sorted_by_relevance = sorted(
        retrieved_snippets, key=lambda item: item.get("score", 0.0), reverse=True
    )
    current_tokens = 0
    final_chunks = []
    for chunk in sorted_by_relevance:
        snippet_tokens = _estimate_tokens(chunk.get("snippet", ""))
        if current_tokens + snippet_tokens < token_limit:
            final_chunks.append(chunk)
            current_tokens += snippet_tokens
    return final_chunks
