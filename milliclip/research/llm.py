"""Pluggable topic tagging. OFF by default: the built-in tagger makes no API calls.

To add an LLM tagger, implement TopicTagger and register it with register_tagger();
select it with `--tagger NAME`. Nothing in this package calls an LLM on its own.
"""
from __future__ import annotations

from typing import Callable, Protocol


class TopicTagger(Protocol):
    def tag(self, video: dict) -> str | None: ...


class NullTagger:
    def tag(self, video: dict) -> str | None:
        return None


_REGISTRY: dict[str, Callable[[], TopicTagger]] = {"none": NullTagger}


def register_tagger(name: str, factory: Callable[[], TopicTagger]) -> None:
    _REGISTRY[name] = factory


def get_tagger(name: str = "none") -> TopicTagger:
    try:
        return _REGISTRY[name]()
    except KeyError:
        raise ValueError(f"unknown tagger {name!r}; available: {sorted(_REGISTRY)}") from None
