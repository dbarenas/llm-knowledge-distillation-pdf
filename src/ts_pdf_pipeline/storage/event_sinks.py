from __future__ import annotations

from pathlib import Path

from ts_pdf_pipeline.domain.models import PipelineEvent
from ts_pdf_pipeline.storage.jsonl_store import append_jsonl
from ts_pdf_pipeline.storage.kb_sqlite import insert_event


class JsonlEventSink:
    def __init__(self, path: Path) -> None:
        self._path = path

    def log(self, event: PipelineEvent) -> None:
        append_jsonl(self._path, event.model_dump())


class SqliteEventSink:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def log(self, event: PipelineEvent) -> None:
        insert_event(self._db_path, event)
