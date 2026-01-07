from __future__ import annotations

import json
import logging
from typing import Any

from pydantic import BaseModel, ValidationError

from ts_pdf_pipeline.domain.exceptions import StudentOutputParseError, TeacherOutputParseError

logger = logging.getLogger(__name__)


def safe_dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _extract_json_candidate(text: str) -> str | None:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start : end + 1]


def parse_json_text(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        candidate = _extract_json_candidate(text)
        if not candidate:
            raise
        return json.loads(candidate)


def parse_model(text: str, model: type[BaseModel], *, source: str) -> BaseModel:
    try:
        data = parse_json_text(text)
    except json.JSONDecodeError as exc:
        logger.debug("Failed to parse JSON from %s output", source)
        if source == "teacher":
            raise TeacherOutputParseError("Invalid JSON from teacher") from exc
        raise StudentOutputParseError("Invalid JSON from student") from exc

    try:
        return model.model_validate(data)
    except ValidationError as exc:
        if source == "teacher":
            raise TeacherOutputParseError("Teacher output schema mismatch") from exc
        raise StudentOutputParseError("Student output schema mismatch") from exc
