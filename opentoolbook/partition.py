"""Filename partition between an author install and a distribution list.

The two sides are names. A name that occurs on both sides is not marked as
something a book needs in order to open.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NamePartition:
    """Author-only names, names in both, and distribution-only names.

    ``both`` keeps the first author spelling. ``distribution_only`` keeps
    the first distribution spelling. Comparison ignores case.
    """

    author_only: tuple[str, ...]
    both: tuple[str, ...]
    distribution_only: tuple[str, ...]


def install_partition(author_names, distribution_names) -> NamePartition:
    """Split two filename lists into author-only, shared, and distribution-only."""
    author = _first(author_names)
    distribution = _first(distribution_names)
    author_keys = set(author)
    distribution_keys = set(distribution)
    shared = author_keys & distribution_keys
    return NamePartition(
        author_only=tuple(author[key] for key in sorted(author_keys - distribution_keys)),
        both=tuple(author[key] for key in sorted(shared)),
        distribution_only=tuple(
            distribution[key] for key in sorted(distribution_keys - author_keys)
        ),
    )


def _first(names) -> dict[str, str]:
    found: dict[str, str] = {}
    for name in names:
        key = name.casefold()
        if key not in found:
            found[key] = name
    return found
