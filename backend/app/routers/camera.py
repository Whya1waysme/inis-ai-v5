from __future__ import annotations

from fastapi import APIRouter, Depends

from ..db import get_session
from ..models import CameraSetting
from ..schemas import CameraSettingsRequest, CameraSettingsResponse
from ..services.camera import CameraAdvisor, CameraContext

router = APIRouter(prefix="/camera-settings", tags=["camera"])


@router.post("", response_model=CameraSettingsResponse)
def generate_camera_settings(payload: CameraSettingsRequest, session=Depends(get_session)):
    context = CameraContext(
        scene_type=payload.scene_type,
        lighting=payload.lighting,
        motion=payload.motion,
        desired_depth_of_field=payload.desired_depth_of_field,
    )
    result = CameraAdvisor.recommend(context)

    entity = CameraSetting(
        script_id=payload.script_id,
        scene_type=payload.scene_type,
        lighting=payload.lighting,
        motion=payload.motion,
        desired_depth_of_field=payload.desired_depth_of_field,
        iso=result.iso,
        shutter_speed=result.shutter_speed,
        aperture=result.aperture,
        white_balance=result.white_balance,
        notes=result.notes,
    )
    session.add(entity)
    session.commit()
    session.refresh(entity)

    return CameraSettingsResponse(
        iso=entity.iso,
        shutter_speed=entity.shutter_speed,
        aperture=entity.aperture,
        white_balance=entity.white_balance,
        notes=entity.notes,
        script_id=entity.script_id,
    )
