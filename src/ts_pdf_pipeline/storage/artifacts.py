from __future__ import annotations

import json
from pathlib import Path

from ts_pdf_pipeline.domain.models import Document, RunContext, SensitivityLabel
from ts_pdf_pipeline.utils.json_utils import safe_dump


class FileArtifactStore:
    def _ensure_dir(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def _write_json(self, path: Path, payload: dict) -> Path:
        path.write_text(safe_dump(payload), encoding="utf-8")
        return path

    def save_teacher(self, ctx: RunContext, doc: Document, out: SensitivityLabel) -> Path:
        base = ctx.artifacts_dir / ctx.run_id / "teacher"
        self._ensure_dir(base)
        return self._write_json(base / f"{doc.doc_hash}.label.json", out.model_dump())

    def save_student(self, ctx: RunContext, doc: Document, out: SensitivityLabel) -> Path:
        base = ctx.artifacts_dir / ctx.run_id / "student"
        self._ensure_dir(base)
        return self._write_json(base / f"{doc.doc_hash}.label.json", out.model_dump())

    def save_sft_example(self, ctx: RunContext, doc: Document, teacher: SensitivityLabel) -> Path:
        base = ctx.artifacts_dir / ctx.run_id / "sft"
        self._ensure_dir(base)
        payload = {
            "doc_hash": doc.doc_hash,
            "prompt": doc.text,
            "completion": json.dumps(teacher.model_dump(), ensure_ascii=False),
        }
        path = base / "train.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return path
