from __future__ import annotations

from datetime import datetime, timezone
import uuid


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def run_id() -> str:
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{ts}-{uuid.uuid4().hex[:8]}"
