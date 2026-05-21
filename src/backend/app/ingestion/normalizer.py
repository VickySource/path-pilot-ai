import re


def normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text
