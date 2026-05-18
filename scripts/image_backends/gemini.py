from __future__ import annotations

import base64
import json
import mimetypes
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "gemini-2.5-flash-image"
DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class GeminiImageError(RuntimeError):
    """Raised when Gemini does not return a usable image."""


@dataclass(frozen=True)
class GeminiImageRequest:
    template_path: Path
    reference_path: Path
    prompt: str
    output_path: Path
    response_path: Path | None = None
    model: str = DEFAULT_MODEL
    aspect_ratio: str = "1:1"
    image_size: str | None = None
    timeout: int = 180


def generate_image(request: GeminiImageRequest) -> Path:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise GeminiImageError("GEMINI_API_KEY is not set")

    _require_file(request.template_path, "template")
    _require_file(request.reference_path, "reference")

    payload = _build_payload(request)
    result = _post_generate_content(api_key=api_key, model=request.model, payload=payload, timeout=request.timeout)
    if request.response_path:
        request.response_path.parent.mkdir(parents=True, exist_ok=True)
        request.response_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    image_bytes = _first_inline_image(result)
    if image_bytes is None:
        raise GeminiImageError("Gemini response did not contain an inline image")

    request.output_path.parent.mkdir(parents=True, exist_ok=True)
    request.output_path.write_bytes(image_bytes)
    return request.output_path


def _require_file(path: Path, label: str) -> None:
    if not path.exists() or not path.is_file():
        raise GeminiImageError(f"{label} image does not exist: {path}")


def _build_payload(request: GeminiImageRequest) -> dict[str, Any]:
    image_config: dict[str, Any] = {}
    if request.aspect_ratio:
        image_config["aspectRatio"] = request.aspect_ratio
    if request.image_size:
        image_config["imageSize"] = request.image_size

    generation_config: dict[str, Any] = {"responseModalities": ["TEXT", "IMAGE"]}
    if image_config:
        generation_config["imageConfig"] = image_config

    return {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": request.prompt},
                    _inline_image_part(request.template_path),
                    _inline_image_part(request.reference_path),
                ],
            }
        ],
        "generationConfig": generation_config,
    }


def _inline_image_part(path: Path) -> dict[str, Any]:
    mime_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return {
        "inline_data": {
            "mime_type": mime_type,
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
        }
    }


def _post_generate_content(*, api_key: str, model: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    url = DEFAULT_ENDPOINT.format(model=model)
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise GeminiImageError(f"Gemini HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise GeminiImageError(f"Gemini request failed: {exc}") from exc


def _first_inline_image(result: dict[str, Any]) -> bytes | None:
    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    return None

