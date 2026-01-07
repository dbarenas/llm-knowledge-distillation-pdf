from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest


def _skip_if_missing() -> None:
    pytest.importorskip("pydantic")


def test_pipeline_smoke(tmp_path: Path) -> None:
    _skip_if_missing()
    from ts_pdf_pipeline.domain.models import Document, SensitivityLabel
    from ts_pdf_pipeline.domain.types import DocumentLoader, Student, Teacher
    from ts_pdf_pipeline.pipeline.teacher_student import TeacherStudentPipeline
    from ts_pdf_pipeline.storage.artifacts import FileArtifactStore
    from ts_pdf_pipeline.storage.event_sinks import JsonlEventSink

    @dataclass
    class DummyLoader:
        def load(self, pdf_path: Path) -> Document:
            return Document(pdf_path=pdf_path, text="dummy text", doc_hash="hash123")

    @dataclass
    class DummyTeacher:
        @property
        def model_name(self) -> str:
            return "dummy-teacher"

        def label(self, doc: Document) -> SensitivityLabel:
            return SensitivityLabel(label=1, confidence=0.9, signals=["signal"], rationale_short="ok")

    @dataclass
    class DummyStudent:
        @property
        def model_name(self) -> str:
            return "dummy-student"

        def label(self, doc: Document) -> SensitivityLabel:
            return SensitivityLabel(label=0, confidence=0.4, signals=[], rationale_short="ok")

    loader: DocumentLoader = DummyLoader()
    teacher: Teacher = DummyTeacher()
    student: Student = DummyStudent()
    artifacts = FileArtifactStore()
    event_sink = JsonlEventSink(tmp_path / "events.jsonl")

    pipeline = TeacherStudentPipeline(
        loader=loader,
        teacher=teacher,
        student=student,
        artifact_store=artifacts,
        event_sinks=[event_sink],
        prompt_version="test",
        artifacts_dir=tmp_path,
        kb_dir=tmp_path,
        generate_sft=True,
    )

    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.write_text("placeholder", encoding="utf-8")

    result = pipeline.run(pdf_path, notes="smoke")

    assert result.teacher_artifact.exists()
    assert result.student_artifact.exists()
    assert result.sft_artifact is not None
    assert result.sft_artifact.exists()
    assert (tmp_path / "events.jsonl").exists()


def test_parse_model_success() -> None:
    _skip_if_missing()
    from ts_pdf_pipeline.domain.models import SensitivityLabel
    from ts_pdf_pipeline.utils.json_utils import parse_model

    text = '{"label":1,"confidence":0.7,"signals":["a"],"rationale_short":"ok"}'
    out = parse_model(text, SensitivityLabel, source="student")
    assert out.label == 1


def test_parse_model_invalid() -> None:
    _skip_if_missing()
    from ts_pdf_pipeline.domain.models import SensitivityLabel
    from ts_pdf_pipeline.utils.json_utils import parse_model

    text = "not json"
    with pytest.raises(Exception):
        parse_model(text, SensitivityLabel, source="student")
