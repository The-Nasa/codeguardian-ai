"""Synthetic input for the Gemini PR comment test."""


def last_or_default(values: list[int], default: int = 0) -> int:
    """Return the last value, or default when the list is empty."""
    return values[-1]
