from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from ..config import settings


class HiggsfieldClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self.api_key = api_key or settings.higgsfield_api_key
        self.base_url = base_url or settings.higgsfield_api_url or "https://api.higgsfield.ai/v1"
        self._headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json",
        }

    async def generate_images(
        self,
        prompt: str,
        num_images: int = 1,
        width: int = 1024,
        height: int = 576,
        quality: str = "high",
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "num_images": num_images,
            "width": width,
            "height": height,
            "quality": quality,
        }
        if additional_params:
            payload.update(additional_params)

        if not self.api_key:
            raise RuntimeError("Higgsfield API key is not configured")
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.base_url}/images/generate",
                headers=self._headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            # Expecting { images: [ { url: "..."}, ... ] }
            images = data.get("images") or []
            urls = []
            for item in images:
                url = item.get("url") or item.get("image_url")
                if url:
                    urls.append(url)
            return urls
