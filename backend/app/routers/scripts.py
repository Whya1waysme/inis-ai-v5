from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..clients.openai_client import OpenAIClient
from ..db import get_session
from ..models import Script
from ..schemas import GenerateScriptRequest, GenerateScriptResponse

router = APIRouter(prefix="/generate-script", tags=["scripts"])


@router.post("", response_model=GenerateScriptResponse)
def generate_script(payload: GenerateScriptRequest, session=Depends(get_session)):
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

    script = Script(
        title=payload.title or payload.prompt[:80],
        prompt=payload.prompt,
        content=content,
    )
    session.add(script)
    session.commit()
    session.refresh(script)

    return GenerateScriptResponse(script_id=script.id, content=script.content)
