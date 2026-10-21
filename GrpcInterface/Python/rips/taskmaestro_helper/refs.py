"""ResInsight object references in taskmaestro input files.

The Workflow UI writes a `{__resinsight_ref__: <type>, ...id...}` map into
input.yaml for fields that refer to a ResInsight object. `run` resolves these
maps back to live `rips` objects. The C++ side maps Python types to the
`<type>` labels in RimWorkflowDescribeTools.
"""

from __future__ import annotations

from typing import Any

# Marker used inside input.yaml to denote a ResInsight object reference.
REF_MARKER = "__resinsight_ref__"


def strip_refs(value: Any) -> Any:
    """Remove ResInsight object references, which are only valid for one run."""
    if isinstance(value, dict):
        return {
            key: strip_refs(item)
            for key, item in value.items()
            if not (isinstance(item, dict) and REF_MARKER in item)
        }
    if isinstance(value, list):
        return [
            strip_refs(item)
            for item in value
            if not (isinstance(item, dict) and REF_MARKER in item)
        ]
    return value
