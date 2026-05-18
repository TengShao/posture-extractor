#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from image_backends.gemini import GeminiImageRequest, generate_image


DEFAULT_PROMPT = """Edit Image 1 only. Image 1 is the base template and the only appearance source. Preserve its smooth white material, featureless head, body proportions, silhouette, lighting, and overall look.

Use Image 2 only as a pose reference. Match the body pose, limb angles, support points, head direction, torso lean, shoulder tilt, hip rotation, arm placement, hand gesture, leg placement, and balance shown in Image 2.

Full-body framing is required. Show the entire head, torso, both arms, both hands, both legs, and both feet. No cropping. No body part touches the image edge. Use a centered square composition with generous empty margin on all sides.

Keep the whole figure continuous plain white template material. Do not add or copy clothing, hair, face, facial features, accessories, colors, texture, props, scene, platform, watermark, text, or background from Image 2.

Output a raw chroma-key source image on one flat, uniform, saturated bright green background. The background must have no gradient, no vignette, no lighting falloff, no texture, no floor plane, no cast shadow, no contact shadow, no transparency, no checkerboard, and no text."""


def main() -> int:
    args = parse_args()
    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else DEFAULT_PROMPT

    if args.backend != "gemini":
        raise SystemExit(f"Unsupported backend: {args.backend}")

    output = generate_image(
        GeminiImageRequest(
            template_path=args.template,
            reference_path=args.reference,
            prompt=prompt,
            output_path=args.out,
            response_path=args.response,
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            image_size=args.image_size,
            timeout=args.timeout,
        )
    )
    print(output.resolve())
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a white-model posture image through an image backend.")
    parser.add_argument("--backend", default="gemini", choices=["gemini"])
    parser.add_argument("--template", required=True, type=Path, help="White-model template image path.")
    parser.add_argument("--reference", required=True, type=Path, help="Pose reference image path.")
    parser.add_argument("--out", required=True, type=Path, help="Output raw backend image path.")
    parser.add_argument("--response", type=Path, help="Optional path to save the full backend JSON response.")
    parser.add_argument("--prompt-file", type=Path, help="Optional prompt text file. Uses a built-in posture prompt if omitted.")
    parser.add_argument("--model", default="gemini-2.5-flash-image")
    parser.add_argument("--aspect-ratio", default="1:1", help="Gemini imageConfig.aspectRatio. Default: 1:1.")
    parser.add_argument("--image-size", help="Gemini imageConfig.imageSize, for models that support it, e.g. 1K.")
    parser.add_argument("--timeout", default=180, type=int)
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())

