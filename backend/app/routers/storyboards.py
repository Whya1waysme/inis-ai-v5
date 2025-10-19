from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from ..clients.higgsfield_client import HiggsfieldClient
from ..schemas import (
    GenerateStoryboardRequest,
    GenerateStoryboardResponse,
    StoryboardItem,
    StoryboardsListResponse,
)

router = APIRouter(prefix="", tags=["storyboards"])


@router.post("/generate-storyboard", response_model=GenerateStoryboardResponse)
async def generate_storyboard(payload: GenerateStoryboardRequest):
    prompt = payload.prompt

    client = HiggsfieldClient()
    urls = await client.generate_images(
        prompt=prompt,
        num_images=payload.num_images,
        width=payload.width,
        height=payload.height,
        quality=payload.quality,
        additional_params=payload.additional_params,
    )

    items: List[StoryboardItem] = [
        StoryboardItem(image_url=url, prompt=prompt) for url in urls
    ]

    return GenerateStoryboardResponse(storyboards=items)


@router.get("/storyboards", response_model=StoryboardsListResponse)
async def list_storyboards(script_id: int | None = None):
    # Stateless mode: no persistence; listing is always empty
    return StoryboardsListResponse(items=[])
