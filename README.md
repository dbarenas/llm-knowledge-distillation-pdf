# Teacher → Student PDF Pipeline

Este repositorio convierte notebooks exploratorios en una **librería modular** para etiquetar PDFs con un flujo teacher→student. El objetivo es mantener la funcionalidad original, pero con una base de código extensible, con principios SOLID, sin lógica duplicada en notebooks.

## ¿Qué hace?
- Carga un PDF y extrae texto.
- Calcula el hash del documento.
- Ejecuta un **teacher** (LLM) que produce un `SensitivityLabel` en JSON válido.
- Ejecuta un **student** (SLM/LLM) que produce el mismo esquema en JSON válido.
- Guarda artefactos en `artifacts/<run_id>/`.
- Registra el evento en `knowledge_base/events.jsonl` y `knowledge_base/kb.sqlite`.
- Opcionalmente genera ejemplos para SFT (JSONL).

## Requisitos
- Python 3.10+
- `pip install -e .`
- Para teacher OpenAI: `OPENAI_API_KEY`
- Para student Ollama: Ollama instalado y modelo descargado

## Setup rápido
```bash
cp .env.example .env
export OPENAI_API_KEY=sk-...
# Ejemplo de modelo local
ollama pull qwen2.5:7b-instruct
pip install -e .[llm,test]
```

## Ejecutar

### CLI
```bash
ts-pdf-pipeline \
  --pdf path/to/file.pdf \
  --teacher openai_sdk \
  --student ollama_rest \
  --notes "demo"
```

### Notebooks
Ver `notebooks/`. Los notebooks sólo importan la librería y ejecutan el pipeline.

## Estructura
```
repo/
  pyproject.toml
  .env.example
  notebooks/
  src/ts_pdf_pipeline/
    config.py
    domain/
    loaders/
    llms/
    pipeline/
    prompts/
    storage/
    utils/
  tests/
```

### Responsabilidades
- `domain/models.py`: modelos Pydantic del dominio (ej. `SensitivityLabel`).
- `domain/types.py`: protocolos e interfaces.
- `loaders/`: carga de documentos (PDF → texto).
- `llms/`: implementaciones teacher/student.
- `pipeline/teacher_student.py`: orquestación sin dependencia de proveedores.
- `storage/`: persistencia de artefactos y eventos.
- `utils/`: hashing, JSON robusto, time utilities.

## Cómo extender
### Nuevo Student
1. Crear clase en `llms/` que implemente `Student`.
2. Registrar en `factories.py`.
3. Ejecutar con `--student nuevo_nombre`.

### Nuevo Teacher
1. Crear clase en `llms/` que implemente `Teacher`.
2. Registrar en `factories.py`.
3. Ejecutar con `--teacher nuevo_nombre`.

### Nuevas tareas
- Crear nuevos modelos Pydantic en `domain/models.py` o módulo nuevo.
- Versionar prompts en `prompts/` y usarlos en nuevas implementaciones.

## Persistencia
- `artifacts/<run_id>/teacher/<doc_hash>.label.json`
- `artifacts/<run_id>/student/<doc_hash>.label.json`
- `knowledge_base/events.jsonl`
- `knowledge_base/kb.sqlite`

## Seguridad / PII
- La librería evita loggear texto completo del PDF.
- Se guardan hashes y rutas, no el contenido completo en logs.

## Roadmap sugerido
- Evaluación teacher vs student.
- Gestión de datasets y versionado.
- Hooks para fine-tuning/LoRA.
- Batching multi-documento.
