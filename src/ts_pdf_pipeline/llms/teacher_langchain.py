from __future__ import annotations

import logging
from typing import Callable

from langchain_openai import ChatOpenAI

from ts_pdf_pipeline.domain.models import Document, SensitivityLabel

logger = logging.getLogger(__name__)


class LangChainTeacher:
    def __init__(
        self,
        api_key: str,
        model: str,
        system_prompt: str,
        user_prompt_builder: Callable[[str], str],
    ) -> None:
        self._model = model
        self._system_prompt = system_prompt
        self._user_prompt_builder = user_prompt_builder
        self._client = ChatOpenAI(model=model, api_key=api_key)

    @property
    def model_name(self) -> str:
        return self._model

    def label(self, doc: Document) -> SensitivityLabel:
        user_prompt = self._user_prompt_builder(doc.text)
        logger.info("Calling LangChain teacher model=%s", self._model)
        llm = self._client.with_structured_output(SensitivityLabel)
        result = llm.invoke(
            [
                ("system", self._system_prompt),
                ("user", user_prompt),
            ]
        )
        return result
