from __future__ import annotations

import logging
from pathlib import Path

import typer

from ts_pdf_pipeline.config import Config
from ts_pdf_pipeline.factories import get_event_sinks, get_student, get_teacher, list_students, list_teachers
from ts_pdf_pipeline.loaders import PDFPlumberLoader
from ts_pdf_pipeline.pipeline.teacher_student import TeacherStudentPipeline
from ts_pdf_pipeline.storage.artifacts import FileArtifactStore

app = typer.Typer(add_completion=False)


@app.command()
def run(
    pdf: Path = typer.Option(..., exists=True, help="Path to PDF"),
    teacher: str = typer.Option("openai_sdk", help=f"Teacher name: {', '.join(list_teachers())}"),
    student: str = typer.Option("ollama_rest", help=f"Student name: {', '.join(list_students())}"),
    notes: str | None = typer.Option(None, help="Optional notes"),
    generate_sft: bool = typer.Option(False, help="Generate SFT JSONL"),
    artifacts_dir: Path | None = typer.Option(None, help="Override artifacts dir"),
    kb_dir: Path | None = typer.Option(None, help="Override knowledge base dir"),
    log_level: str = typer.Option("INFO", help="Logging level"),
) -> None:
    logging.basicConfig(level=log_level.upper(), format="%(levelname)s %(name)s: %(message)s")

    cfg = Config()
    if artifacts_dir:
        cfg.artifacts_dir = artifacts_dir
    if kb_dir:
        cfg.kb_dir = kb_dir
    cfg.ensure_dirs()

    loader = PDFPlumberLoader()
    teacher_impl = get_teacher(teacher, cfg)
    student_impl = get_student(student, cfg)
    artifacts = FileArtifactStore()
    sinks = get_event_sinks(cfg)

    pipeline = TeacherStudentPipeline(
        loader=loader,
        teacher=teacher_impl,
        student=student_impl,
        artifact_store=artifacts,
        event_sinks=sinks,
        prompt_version=cfg.prompt_version,
        artifacts_dir=cfg.artifacts_dir,
        kb_dir=cfg.kb_dir,
        generate_sft=generate_sft,
    )

    result = pipeline.run(pdf, notes=notes)
    typer.echo(f"Run ID: {result.run_id}")
    typer.echo(f"Teacher artifact: {result.teacher_artifact}")
    typer.echo(f"Student artifact: {result.student_artifact}")
    if result.sft_artifact:
        typer.echo(f"SFT artifact: {result.sft_artifact}")


if __name__ == "__main__":
    app()
