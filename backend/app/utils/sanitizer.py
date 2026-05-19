"""
Input Sanitization Utilities
-----------------------------
Helpers to clean and validate user-provided text before it reaches
the LLM or the database.
"""

import re
import html


def sanitize_text(text: str, max_length: int = 5000) -> str:
    """
    Clean user-provided text:
      - Strip leading/trailing whitespace
      - Escape HTML entities to prevent injection
      - Collapse excessive whitespace
      - Truncate to max_length

    Args:
        text:       Raw input string.
        max_length: Maximum allowed character count.

    Returns:
        Sanitized string.
    """
    if not text:
        return ""

    # Escape HTML to prevent XSS if output is ever rendered in a browser
    text = html.escape(text)

    # Collapse multiple spaces/tabs into a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse more than 2 consecutive newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip and truncate
    text = text.strip()[:max_length]

    return text


def sanitize_filename(filename: str) -> str:
    """
    Remove characters that are unsafe in filenames.

    Args:
        filename: Original filename.

    Returns:
        Safe filename string.
    """
    # Keep only alphanumerics, dots, dashes, and underscores
    safe = re.sub(r"[^\w.\-]", "_", filename)
    # Prevent path traversal
    safe = safe.lstrip("./")
    return safe or "unnamed_file"
