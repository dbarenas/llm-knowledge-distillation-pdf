from __future__ import annotations

import logging
from typing import Callable

from openai import OpenAI

from ts_pdf_pipeline.domain.models import Document, SensitivityLabel
from ts_pdf_pipeline.utils.json_utils import parse_model

logger = logging.getLogger(__name__)


class OpenAITeacherSDK:
    def __init__(
        self,
        api_key: str,
        model: str,
        system_prompt: str,
        user_prompt_builder: Callable[[str], str],
    ) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._system_prompt = system_prompt
        self._user_prompt_builder = user_prompt_builder

    @property
    def model_name(self) -> str:
        return self._model

    def label(self, doc: Document) -> SensitivityLabel:
        user_prompt = self._user_prompt_builder(doc.text)
        logger.info("Calling OpenAI teacher model=%s", self._model)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or ""
        return parse_model(content, SensitivityLabel, source="teacher")
