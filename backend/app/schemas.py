from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GenerateScriptRequest(BaseModel):
    prompt: str = Field(..., description="User prompt or description for the script")
    title: Optional[str] = Field(None, description="Optional title for the script")
    model: Optional[str] = Field(None, description="OpenAI model override")
    temperature: float = 0.7
    max_tokens: int = 1200
    language: Optional[str] = Field("ru", description="Language code, e.g., ru or en")
    extra_instructions: Optional[str] = None


class GenerateScriptResponse(BaseModel):
    content: str


class GenerateStoryboardRequest(BaseModel):
    prompt: str
    num_images: int = 1
    width: int = 1024
    height: int = 576
    quality: str = "high"
    additional_params: Optional[Dict[str, Any]] = None


class StoryboardItem(BaseModel):
    image_url: str
    prompt: str


class GenerateStoryboardResponse(BaseModel):
    storyboards: List[StoryboardItem]


class CameraSettingsRequest(BaseModel):
    scene_type: Optional[str] = Field(None, description="e.g., portrait, landscape, sports, night")
    lighting: Optional[str] = Field(None, description="e.g., daylight, cloudy, tungsten, fluorescent, low-light")
    motion: Optional[str] = Field(None, description="none, slow, fast")
    desired_depth_of_field: Optional[str] = Field(None, description="shallow, medium, deep")
    camera_model: Optional[str] = None


class CameraSettingsResponse(BaseModel):
    iso: int
    shutter_speed: float
    aperture: float
    white_balance: str
    notes: Optional[str] = None


class StoryboardsListResponse(BaseModel):
    items: List[StoryboardItem]
