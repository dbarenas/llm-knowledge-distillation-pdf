"""Teacher-student PDF pipeline package."""

from ts_pdf_pipeline.config import Config
from ts_pdf_pipeline.factories import (
    get_event_sinks,
    get_student,
    get_teacher,
    get_teacher_prompt_builder,
    get_student_prompt_builder,
    list_students,
    list_teachers,
)
from ts_pdf_pipeline.pipeline.teacher_student import TeacherStudentPipeline

__all__ = [
    "Config",
    "TeacherStudentPipeline",
    "get_teacher",
    "get_student",
    "get_event_sinks",
    "get_teacher_prompt_builder",
    "get_student_prompt_builder",
    "list_teachers",
    "list_students",
]
