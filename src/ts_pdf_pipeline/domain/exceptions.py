class PipelineError(Exception):
    """Base error for pipeline failures."""


class TeacherOutputParseError(PipelineError):
    """Raised when teacher output cannot be parsed into expected schema."""


class StudentOutputParseError(PipelineError):
    """Raised when student output cannot be parsed into expected schema."""


class LoaderError(PipelineError):
    """Raised when document loading fails."""
