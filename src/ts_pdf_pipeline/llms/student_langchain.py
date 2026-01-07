from __future__ import annotations

import logging
from typing import Callable

from langchain_ollama import ChatOllama

from ts_pdf_pipeline.domain.models import Document, SensitivityLabel
from ts_pdf_pipeline.utils.json_utils import parse_model

logger = logging.getLogger(__name__)


class LangChainStudent:
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
        self._client = ChatOllama(base_url=self._base_url, model=self._model)

    @property
    def model_name(self) -> str:
        return self._model

    def label(self, doc: Document) -> SensitivityLabel:
        user_prompt = self._user_prompt_builder(doc.text)
        logger.info("Calling LangChain student model=%s", self._model)
        response = self._client.invoke(
            [
                ("system", self._system_prompt),
                ("user", user_prompt),
            ]
        )
        return parse_model(str(response.content), SensitivityLabel, source="student")
