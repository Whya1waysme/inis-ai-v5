from __future__ import annotations

from typing import Optional

from openai import OpenAI

from ..config import settings


class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise RuntimeError("OpenAI API key is not configured")
        self.model = model or settings.openai_model
        self._client = OpenAI(api_key=self.api_key)

    def generate_script(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1200,
        language: str = "ru",
        extra_instructions: Optional[str] = None,
    ) -> str:
        system_prompt = (
            "Ты опытный сценарист для кино и рекламы. Пиши структурированные, кинематографичные сценарии с диалогами, описаниями сцен и ремарками."
        )
        if language == "en":
            system_prompt = (
                "You are an experienced screenwriter for film and commercials. Write structured, cinematic scripts with dialogues, scene descriptions and directions."
            )
        if extra_instructions:
            system_prompt += f" Additional guidance: {extra_instructions}"

        completion = self._client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        text = completion.choices[0].message.content or ""
        return text.strip()
