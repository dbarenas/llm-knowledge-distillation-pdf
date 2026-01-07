from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ts_pdf_pipeline.domain.models import Document, PipelineEvent, RunContext, SensitivityLabel


class DocumentLoader(Protocol):
    def load(self, pdf_path: Path) -> Document:
        ...


class Teacher(Protocol):
    @property
    def model_name(self) -> str:
        ...

    def label(self, doc: Document) -> SensitivityLabel:
        ...


class Student(Protocol):
    @property
    def model_name(self) -> str:
        ...

    def label(self, doc: Document) -> SensitivityLabel:
        ...


class ArtifactStore(Protocol):
    def save_teacher(self, ctx: RunContext, doc: Document, out: SensitivityLabel) -> Path:
        ...

    def save_student(self, ctx: RunContext, doc: Document, out: SensitivityLabel) -> Path:
        ...

    def save_sft_example(self, ctx: RunContext, doc: Document, teacher: SensitivityLabel) -> Path:
        ...


class EventSink(Protocol):
    def log(self, event: PipelineEvent) -> None:
        ...
