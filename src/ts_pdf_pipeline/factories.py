from __future__ import annotations

from typing import Callable

from ts_pdf_pipeline.config import Config
from ts_pdf_pipeline.domain.types import EventSink, Student, Teacher
from ts_pdf_pipeline.llms.student_langchain import LangChainStudent
from ts_pdf_pipeline.llms.student_ollama_rest import OllamaStudentREST
from ts_pdf_pipeline.llms.teacher_langchain import LangChainTeacher
from ts_pdf_pipeline.llms.teacher_openai_sdk import OpenAITeacherSDK
from ts_pdf_pipeline.prompts.student_prompts import STUDENT_SYSTEM, build_student_user_prompt
from ts_pdf_pipeline.prompts.teacher_prompts import PROMPT_VERSION, TEACHER_SYSTEM, build_teacher_user_prompt
from ts_pdf_pipeline.storage.event_sinks import JsonlEventSink, SqliteEventSink

TeacherBuilder = Callable[[Config], Teacher]
StudentBuilder = Callable[[Config], Student]


_TEACHERS: dict[str, TeacherBuilder] = {
    "openai_sdk": lambda cfg: OpenAITeacherSDK(
        api_key=cfg.openai_api_key or "",
        model=cfg.openai_model,
        system_prompt=TEACHER_SYSTEM,
        user_prompt_builder=build_teacher_user_prompt,
    ),
    "langchain_openai": lambda cfg: LangChainTeacher(
        api_key=cfg.openai_api_key or "",
        model=cfg.openai_model,
        system_prompt=TEACHER_SYSTEM,
        user_prompt_builder=build_teacher_user_prompt,
    ),
}

_STUDENTS: dict[str, StudentBuilder] = {
    "ollama_rest": lambda cfg: OllamaStudentREST(
        base_url=cfg.ollama_url,
        model=cfg.ollama_model,
        system_prompt=STUDENT_SYSTEM,
        user_prompt_builder=build_student_user_prompt,
    ),
    "langchain_ollama": lambda cfg: LangChainStudent(
        base_url=cfg.ollama_url,
        model=cfg.ollama_model,
        system_prompt=STUDENT_SYSTEM,
        user_prompt_builder=build_student_user_prompt,
    ),
}


def list_teachers() -> list[str]:
    return sorted(_TEACHERS.keys())


def list_students() -> list[str]:
    return sorted(_STUDENTS.keys())


def get_teacher(name: str, cfg: Config) -> Teacher:
    if name not in _TEACHERS:
        raise ValueError(f"Unknown teacher: {name}")
    return _TEACHERS[name](cfg)


def get_student(name: str, cfg: Config) -> Student:
    if name not in _STUDENTS:
        raise ValueError(f"Unknown student: {name}")
    return _STUDENTS[name](cfg)


def get_event_sinks(cfg: Config) -> list[EventSink]:
    return [
        JsonlEventSink(cfg.kb_dir / "events.jsonl"),
        SqliteEventSink(cfg.kb_dir / "kb.sqlite"),
    ]


def get_teacher_prompt_builder() -> tuple[str, Callable[[str], str]]:
    return PROMPT_VERSION, build_teacher_user_prompt


def get_student_prompt_builder() -> Callable[[str], str]:
    return build_student_user_prompt
