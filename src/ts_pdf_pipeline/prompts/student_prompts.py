from __future__ import annotations

STUDENT_SYSTEM = """Eres un modelo estudiante. Devuelve SOLO JSON válido.
Formato: {"label":0|1, "confidence":0..1, "signals":["..."], "rationale_short":"..."}
"""


def build_student_user_prompt(text: str) -> str:
    return (
        "Clasifica el texto en sensibilidad (0=normal,1=sensible).\n"
        "Texto:\n"
        f"{text}\n"
        "Responde únicamente con JSON válido según el esquema."
    )
