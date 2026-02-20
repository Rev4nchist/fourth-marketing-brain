"""YAML frontmatter utilities for knowledge base documents."""

import re
from datetime import datetime, timezone

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a document into frontmatter dict and body text.

    Returns (metadata_dict, body_text).  If no frontmatter is present,
    returns ({}, original_text).
    """
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    raw = match.group(1)
    body = text[match.end():]
    metadata: dict = {}

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        # Strip surrounding quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]

        # Parse YAML-style lists: ["a", "b"]
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            items = []
            for item in inner.split(","):
                item = item.strip().strip('"').strip("'")
                if item:
                    items.append(item)
            metadata[key] = items
        else:
            metadata[key] = value

    return metadata, body


def generate_frontmatter(metadata: dict) -> str:
    """Generate YAML frontmatter string from a metadata dict.

    Returns the full frontmatter block including --- delimiters, or empty
    string if metadata is empty.
    """
    if not metadata:
        return ""

    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, list):
            formatted = "[" + ", ".join(f'"{v}"' for v in value) + "]"
            lines.append(f'{key}: {formatted}')
        else:
            lines.append(f'{key}: "{value}"')
    lines.append("---")
    lines.append("")  # trailing newline after frontmatter
    return "\n".join(lines)


def merge_metadata(existing: dict, updates: dict | None) -> dict:
    """Merge update metadata into existing, preserving unspecified fields.

    Always sets last_updated to current UTC date.
    """
    merged = dict(existing)
    if updates:
        for k, v in updates.items():
            if v is not None:
                merged[k] = v
    merged["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return merged


def sanitize_filename(name: str) -> str:
    """Sanitize a filename: lowercase, hyphens for spaces, strip special chars."""
    name = name.lower().strip()
    name = name.replace(" ", "-")
    # Keep only alphanumeric, hyphens, underscores
    name = re.sub(r"[^a-z0-9\-_]", "", name)
    # Collapse multiple hyphens
    name = re.sub(r"-{2,}", "-", name)
    return name.strip("-_")
