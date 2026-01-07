from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class SensitivityLabel(BaseModel):
    label: int = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    signals: list[str] = Field(default_factory=list)
    rationale_short: str


@dataclass(frozen=True)
class Document:
    pdf_path: Path
    text: str
    doc_hash: str


@dataclass(frozen=True)
class RunContext:
    run_id: str
    artifacts_dir: Path
    kb_dir: Path


class PipelineEvent(BaseModel):
    ts: str
    doc_hash: str
    pdf_path: str
    teacher: str
    student: str
    prompt_version: str
    artifacts_dir: str
    notes: str | None = None
    versions: dict[str, Any] = Field(default_factory=dict)
