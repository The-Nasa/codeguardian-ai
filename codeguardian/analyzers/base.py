"""Adapter boundary. A future runner is responsible for actual isolation."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from codeguardian.core.config import EffectivePolicy


@dataclass(frozen=True)
class ReviewContext:
    changed_files: tuple[Path, ...]
    policy: EffectivePolicy


@dataclass(frozen=True)
class AnalyzerPlan:
    command: tuple[str, ...]
    timeout_seconds: int
    required: bool


@dataclass(frozen=True)
class IsolatedContext:
    checkout: Path
    plan: AnalyzerPlan


@dataclass(frozen=True)
class RawResult:
    exit_code: int | None
    stdout: str
    stderr: str
    duration_ms: int


class AnalyzerAdapter(Protocol):
    id: str
    version: str
    languages: tuple[str, ...]
    file_patterns: tuple[str, ...]
    requirements: tuple[str, ...]
    supports_untrusted_pr: bool

    def supports(self, context: ReviewContext) -> bool: ...
    def plan(self, context: ReviewContext) -> AnalyzerPlan: ...
    def run(self, context: IsolatedContext) -> RawResult: ...
    def normalize(self, raw_result: RawResult) -> Mapping[str, object]: ...
