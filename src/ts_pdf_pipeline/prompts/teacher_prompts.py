from __future__ import annotations

PROMPT_VERSION = "teacher_sensitivity_v1"

TEACHER_SYSTEM = """Eres un clasificador de sensibilidad. Devuelve SOLO JSON válido.
Formato: {"label":0|1, "confidence":0..1, "signals":["..."], "rationale_short":"..."}
"""


def build_teacher_user_prompt(text: str) -> str:
    return (
        "Analiza el siguiente documento y etiqueta sensibilidad (0=normal,1=sensible).\n"
        "Texto:\n"
        f"{text}\n"
        "Responde únicamente con JSON válido según el esquema."
    )
