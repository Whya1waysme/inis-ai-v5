from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..clients.higgsfield_client import HiggsfieldClient
from ..db import get_session
from ..models import Script, Storyboard
from ..schemas import (
    GenerateStoryboardRequest,
    GenerateStoryboardResponse,
    StoryboardItem,
    StoryboardsListResponse,
)

router = APIRouter(prefix="", tags=["storyboards"])


@router.post("/generate-storyboard", response_model=GenerateStoryboardResponse)
async def generate_storyboard(payload: GenerateStoryboardRequest, session=Depends(get_session)):
    script = session.get(Script, payload.script_id)
    if not script:
        raise HTTPException(status_code=404, detail="script not found")

    prompt = payload.prompt or f"Storyboard frame based on script: {script.title}. Key scene: {script.content[:500]}"

    client = HiggsfieldClient()
    urls = await client.generate_images(
        prompt=prompt,
        num_images=payload.num_images,
        width=payload.width,
        height=payload.height,
        quality=payload.quality,
        additional_params=payload.additional_params,
    )

    items: List[StoryboardItem] = []
    for url in urls:
        entity = Storyboard(
            script_id=script.id,
            prompt=prompt,
            image_url=url,
            params_json={
                "width": payload.width,
                "height": payload.height,
                "quality": payload.quality,
            }.__repr__(),
        )
        session.add(entity)
        session.commit()
        session.refresh(entity)
        items.append(StoryboardItem(id=entity.id, image_url=entity.image_url, prompt=entity.prompt))

    return GenerateStoryboardResponse(storyboards=items)


@router.get("/storyboards", response_model=StoryboardsListResponse)
async def list_storyboards(script_id: int, session=Depends(get_session)):
    statement = select(Storyboard).where(Storyboard.script_id == script_id).order_by(Storyboard.id.desc())
    rows = session.exec(statement).all()
    items = [StoryboardItem(id=r.id, image_url=r.image_url, prompt=r.prompt) for r in rows]
    return StoryboardsListResponse(items=items)
