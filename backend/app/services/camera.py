from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CameraContext:
    scene_type: Optional[str] = None
    lighting: Optional[str] = None
    motion: Optional[str] = None
    desired_depth_of_field: Optional[str] = None


@dataclass
class CameraSettings:
    iso: int
    shutter_speed: float
    aperture: float
    white_balance: str
    notes: Optional[str] = None


class CameraAdvisor:
    @staticmethod
    def recommend(context: CameraContext) -> CameraSettings:
        lighting = (context.lighting or "daylight").lower()
        scene = (context.scene_type or "general").lower()
        motion = (context.motion or "none").lower()
        dof = (context.desired_depth_of_field or "medium").lower()

        # ISO baseline by lighting
        if lighting in {"night", "low-light", "indoors"}:
            iso = 1600
            white_balance = "tungsten" if lighting != "night" else "auto"
        elif lighting in {"cloudy"}:
            iso = 400
            white_balance = "cloudy"
        elif lighting in {"fluorescent"}:
            iso = 800
            white_balance = "fluorescent"
        else:  # daylight, sunny, default
            iso = 100
            white_balance = "daylight"

        # Shutter by motion
        if motion == "fast":
            shutter_speed = 1 / 1000
        elif motion == "slow":
            shutter_speed = 1 / 250
        else:
            shutter_speed = 1 / 60

        # Aperture by DoF and scene
        if dof == "shallow" or scene == "portrait":
            aperture = 2.0
        elif dof == "deep" or scene == "landscape":
            aperture = 8.0
        else:
            aperture = 4.0

        notes = ""
        if scene == "night":
            notes = "Use tripod or stabilization to avoid blur."
        if motion == "fast":
            notes = (notes + " ").strip() + "Consider raising ISO to maintain exposure."

        return CameraSettings(
            iso=iso,
            shutter_speed=shutter_speed,
            aperture=aperture,
            white_balance=white_balance,
            notes=notes or None,
        )
