from __future__ import annotations

import sqlite3
from pathlib import Path

from ts_pdf_pipeline.domain.models import PipelineEvent


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                doc_hash TEXT NOT NULL,
                pdf_path TEXT NOT NULL,
                teacher TEXT NOT NULL,
                student TEXT NOT NULL,
                prompt_version TEXT NOT NULL,
                artifacts_dir TEXT NOT NULL,
                notes TEXT,
                versions TEXT
            )
            """
        )
        conn.commit()


def insert_event(db_path: Path, event: PipelineEvent) -> None:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO events (
                ts, doc_hash, pdf_path, teacher, student, prompt_version,
                artifacts_dir, notes, versions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.ts,
                event.doc_hash,
                event.pdf_path,
                event.teacher,
                event.student,
                event.prompt_version,
                event.artifacts_dir,
                event.notes,
                str(event.versions),
            ),
        )
        conn.commit()
