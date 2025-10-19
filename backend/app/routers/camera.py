from __future__ import annotations

from fastapi import APIRouter
from ..schemas import CameraSettingsRequest, CameraSettingsResponse
from ..services.camera import CameraAdvisor, CameraContext

router = APIRouter(prefix="/camera-settings", tags=["camera"])


@router.post("", response_model=CameraSettingsResponse)
def generate_camera_settings(payload: CameraSettingsRequest):
    context = CameraContext(
        scene_type=payload.scene_type,
        lighting=payload.lighting,
        motion=payload.motion,
        desired_depth_of_field=payload.desired_depth_of_field,
    )
    result = CameraAdvisor.recommend(context)

    return CameraSettingsResponse(
        iso=result.iso,
        shutter_speed=result.shutter_speed,
        aperture=result.aperture,
        white_balance=result.white_balance,
        notes=result.notes,
    )
