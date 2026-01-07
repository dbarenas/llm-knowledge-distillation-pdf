from __future__ import annotations

import logging
from typing import Callable

import requests

from ts_pdf_pipeline.domain.models import Document, SensitivityLabel
from ts_pdf_pipeline.utils.json_utils import parse_model

logger = logging.getLogger(__name__)


class OllamaStudentREST:
    def __init__(
        self,
        base_url: str,
        model: str,
        system_prompt: str,
        user_prompt_builder: Callable[[str], str],
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._system_prompt = system_prompt
        self._user_prompt_builder = user_prompt_builder

    @property
    def model_name(self) -> str:
        return self._model

    def label(self, doc: Document) -> SensitivityLabel:
        user_prompt = self._user_prompt_builder(doc.text)
        logger.info("Calling Ollama student model=%s", self._model)
        payload = {
            "model": self._model,
            "stream": False,
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        response = requests.post(f"{self._base_url}/api/chat", json=payload, timeout=180)
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "")
        return parse_model(content, SensitivityLabel, source="student")
