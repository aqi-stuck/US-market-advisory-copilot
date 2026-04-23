from typing import List

from app.core.config import settings


def simple_embedding(text: str, dimensions: int = 64) -> List[float]:
    """
    Temporary lightweight embedding for development.
    Replace with OpenAI or another embedding model later.
    """
    text = (text or "").strip().lower()
    vector = [0.0] * dimensions

    for index, char in enumerate(text):
        vector[index % dimensions] += (ord(char) % 31) / 31.0

    return vector