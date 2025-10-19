from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Script(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    prompt: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Storyboard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    script_id: int = Field(index=True, foreign_key="script.id")
    prompt: str
    image_url: str
    # Store additional params as JSON string for broad DB compatibility
    params_json: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CameraSetting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    script_id: Optional[int] = Field(default=None, index=True, foreign_key="script.id")
    scene_type: Optional[str] = None
    lighting: Optional[str] = None
    motion: Optional[str] = None
    desired_depth_of_field: Optional[str] = None

    iso: int
    shutter_speed: float  # seconds
    aperture: float  # f-number
    white_balance: str
    notes: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
