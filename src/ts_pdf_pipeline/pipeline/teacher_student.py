from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from ts_pdf_pipeline.domain.models import Document, PipelineEvent, RunContext, SensitivityLabel
from ts_pdf_pipeline.domain.types import ArtifactStore, DocumentLoader, EventSink, Student, Teacher
from ts_pdf_pipeline.utils.time_utils import now_iso, run_id

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PipelineResult:
    run_id: str
    document: Document
    teacher_output: SensitivityLabel
    student_output: SensitivityLabel
    teacher_artifact: Path
    student_artifact: Path
    sft_artifact: Path | None
    event: PipelineEvent


class TeacherStudentPipeline:
    def __init__(
        self,
        loader: DocumentLoader,
        teacher: Teacher,
        student: Student,
        artifact_store: ArtifactStore,
        event_sinks: list[EventSink],
        prompt_version: str,
        artifacts_dir: Path,
        kb_dir: Path,
        generate_sft: bool = False,
    ) -> None:
        self._loader = loader
        self._teacher = teacher
        self._student = student
        self._artifact_store = artifact_store
        self._event_sinks = event_sinks
        self._prompt_version = prompt_version
        self._artifacts_dir = artifacts_dir
        self._kb_dir = kb_dir
        self._generate_sft = generate_sft

    def run(self, pdf_path: Path, notes: str | None = None) -> PipelineResult:
        ctx = RunContext(
            run_id=run_id(),
            artifacts_dir=self._artifacts_dir,
            kb_dir=self._kb_dir,
        )
        logger.info("Starting pipeline run_id=%s", ctx.run_id)
        doc = self._loader.load(pdf_path)
        teacher_out = self._teacher.label(doc)
        student_out = self._student.label(doc)

        teacher_path = self._artifact_store.save_teacher(ctx, doc, teacher_out)
        student_path = self._artifact_store.save_student(ctx, doc, student_out)

        sft_path = None
        if self._generate_sft:
            sft_path = self._artifact_store.save_sft_example(ctx, doc, teacher_out)

        event = PipelineEvent(
            ts=now_iso(),
            doc_hash=doc.doc_hash,
            pdf_path=str(doc.pdf_path),
            teacher=self._teacher.model_name,
            student=self._student.model_name,
            prompt_version=self._prompt_version,
            artifacts_dir=str(ctx.artifacts_dir / ctx.run_id),
            notes=notes,
            versions={
                "teacher": self._teacher.model_name,
                "student": self._student.model_name,
            },
        )
        for sink in self._event_sinks:
            sink.log(event)

        logger.info("Pipeline completed run_id=%s", ctx.run_id)
        return PipelineResult(
            run_id=ctx.run_id,
            document=doc,
            teacher_output=teacher_out,
            student_output=student_out,
            teacher_artifact=teacher_path,
            student_artifact=student_path,
            sft_artifact=sft_path,
            event=event,
        )
