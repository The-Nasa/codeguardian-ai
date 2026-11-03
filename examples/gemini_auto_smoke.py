"""Synthetic example for automatic PR review."""


def first_or_default(values: list[int], default: int = 0) -> int:
    """Return the first value, or the default when empty."""
    return values[0] if values else default
