from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..clients.openai_client import OpenAIClient
from ..schemas import GenerateScriptRequest, GenerateScriptResponse

router = APIRouter(prefix="/generate-script", tags=["scripts"])


@router.post("", response_model=GenerateScriptResponse)
def generate_script(payload: GenerateScriptRequest):
    if not payload.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    client = OpenAIClient(model=payload.model)
    content = client.generate_script(
        prompt=payload.prompt,
        temperature=payload.temperature,
        max_tokens=payload.max_tokens,
        language=payload.language,
        extra_instructions=payload.extra_instructions,
    )

    return GenerateScriptResponse(content=content)
