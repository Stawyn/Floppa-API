"""Wrappers around g4f for prompt generation."""
from __future__ import annotations

from typing import Literal

import g4f


IMAGE_PROMPT_TEMPLATE = """Analyze the given input text, and create a summary.\nThe output text is intended for an image-generation AI and must describe an image that is appropriate to the text.\nThe image style and theme should match the style and genre of the text.\nThe input text is delimited by triple backticks.\nDo not include the sentence \"Generate a charming image\" in the summary.\nEach summary should be 150 words long.\n```{text}```"""


def build_prompt(text: str, prompt_type: Literal["text", "image"] = "text") -> str:
    if prompt_type == "image":
        return IMAGE_PROMPT_TEMPLATE.format(text=text)
    return text


def generate_completion(prompt: str) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4_turbo,
        messages=[{"role": "user", "content": prompt}],
    )
    return response or "Nao foi possivel processar"


def gpt_input(text: str, prompt_type: Literal["text", "image"] = "text") -> str:
    prompt = build_prompt(text, prompt_type)
    try:
        return generate_completion(prompt)
    except Exception:  # pragma: no cover - defensive guard around external dependency
        return "Nao foi possivel processar"
