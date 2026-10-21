"""Version guard and shared error type for the taskmaestro helper.

The helper uses taskmaestro's public ``definition``, ``introspection`` and
``discovery`` APIs, which are available from taskmaestro 0.4.
"""

from __future__ import annotations

try:
    from taskmaestro.exceptions import DefinitionError
except ImportError:  # taskmaestro missing or too old; require_taskmaestro reports it

    class DefinitionError(Exception):  # type: ignore[no-redef]
        def __init__(self, message, *, task=None, field=None):
            super().__init__(message)
            self.message = message
            self.task = task
            self.field = field

        def to_json(self):
            return {"message": self.message, "task": self.task, "field": self.field}


MIN_TASKMAESTRO_VERSION = (0, 4)
MAX_TASKMAESTRO_VERSION = (0, 5)


class HelperError(DefinitionError):
    """An error reported to ResInsight as ``{"status": "invalid", "error": ...}``."""


def _version_tuple(version: str) -> tuple[int, ...]:
    parts: list[int] = []
    for part in version.split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


def taskmaestro_version() -> str:
    import taskmaestro

    return str(getattr(taskmaestro, "__version__", "0"))


def require_taskmaestro() -> None:
    """Raise HelperError unless a supported taskmaestro version is installed."""
    try:
        version = taskmaestro_version()
    except ImportError as exc:
        raise HelperError(f"taskmaestro is not installed: {exc}") from exc
    parsed = _version_tuple(version)
    if parsed < MIN_TASKMAESTRO_VERSION or parsed >= MAX_TASKMAESTRO_VERSION:
        raise HelperError(
            f"taskmaestro {version} is not supported; "
            "install taskmaestro>=0.4,<0.5 to edit workflows"
        )
