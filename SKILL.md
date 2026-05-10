---
name: posture-generator
description: Generate clean transparent-background PNGs of male or female white models matching poses from one or more user-provided character images, plus AIGC-ready pose prompts. Use when the user wants white mannequin/body templates to imitate reference postures while preserving template body proportions and removing clothing, hair, accessories, background, and all unrelated visual details.
---

# Posture Generator

Use this skill when the user provides one or more images and wants a white model to copy the character poses.

## Inputs

- User reference image(s) containing a person or character, provided as uploaded image attachment(s), image file path(s), or a directory path in text.
- Path-style invocation is supported, for example: `/posture-generator path/to/image`.
  - Treat path arguments after `/posture-generator` as reference image paths or directory paths.
  - Resolve relative paths from the current working directory.
  - If a path does not exist, ask the user for a valid image path or directory path.
  - If a path is a directory, collect all supported image files inside it for batch processing and ask for confirmation before generating.
- White model templates in `template/`:
  - `template/male.png`
  - `template/female.png`

Supported image file extensions include `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`, and `.tiff`.

If an image contains multiple people, use the primary/most central subject unless the user identifies another subject. If the subject's gender presentation is unclear, state the uncertainty briefly and choose the closest template.

## Output Defaults

- Pose image format: transparent-background `.png`.
- Pose image size: `1024x1024`.
- Framing: full body, with no cropped head, hands, feet, limbs, or props.
- Model style: clean white model silhouette only, with a slightly strengthened contour for reliable cutout and readability.
- Also output concise bilingual pose descriptions suitable for AIGC image-generation prompts, with both Chinese and English versions.

## Workflow

1. Resolve reference image(s):
   - If the user uploaded one or more images, use those images directly.
   - If the user provided `/posture-generator path/to/image`, resolve and load the provided path(s).
   - If a provided path is a directory, collect all supported image files inside it and ask for confirmation before processing.
   - If both uploaded images and paths are present, use uploaded images unless the user explicitly says to use the paths too.
2. Prefer an image generation or editing API/tool that can preserve the selected white-model template. Do not request native alpha or transparent output from the generation model. Generate a normal `1024x1024` image first, using a flat, solid, high-saturation background with strong color contrast against the white mannequin, such as bright green or bright blue. Avoid white, off-white, gray, beige, low-saturation colors, gradients, shadows, textures, or scenery in the background. Slightly strengthen the mannequin's readable contour with a thin, soft, neutral gray edge or shading transition so the body boundary remains easy to separate from the background; avoid a thick black, cartoon, inked, or decorative outline.
3. If there are multiple reference images, process each image independently and preserve input order in outputs and prompt descriptions.
4. Inspect the current reference image.
5. Identify the subject's apparent gender presentation for template selection:
   - Male subject: use `template/male.png`.
   - Female subject: use `template/female.png`.
6. Extract only the body pose:
   - overall stance or seated/lying position
   - head direction and tilt
   - spine/torso angle
   - shoulder and hip rotation
   - arm, hand, leg, and foot placement
   - weight distribution and gesture energy
7. Generate or edit the selected white model template so it matches the reference pose on the removable high-contrast solid-color background.
8. Post-process the generated image by removing the background, using background removal, chroma-key removal, matting, or local cutout tools. Remove visible color spill from the solid background, preserve the strengthened white-model contour, and anti-alias the alpha edge so the final silhouette is smooth rather than jagged. When using local cutout tools, prefer high-resolution or supersampled matting, then downsample cleanly to `1024x1024`. Export the result as a transparent PNG at `1024x1024`.
9. Validate the cutout PNG before delivery:
   - The file must be a real `RGBA` PNG, not `RGB`.
   - The alpha channel must contain transparent pixels outside the mannequin.
   - The mannequin edge should be smooth and anti-aliased, with no stair-step jaggies, harsh halo, or bright green/blue color fringe.
   - A checkerboard transparency preview, solid color background, or any visible background is invalid.
10. If cutout validation fails, retry the post-processing step first.
11. If post-processing repeatedly creates messy edges, stair-step jaggies, color fringe, missing body parts, or altered mannequin appearance, first retry matting with edge smoothing, decontamination, and a small alpha feather. If the edge still fails, regenerate the source image with a cleaner solid-color background that is farther from the mannequin's white/gray tones and a clearer but still subtle contour, then cut it out again.
12. Send the validated generated pose image to the conversation.
13. Also create `posture/` in the current working directory and save the PNG there.
14. Tell the user that the image has been saved to `<path/to/image>`, replacing `<path/to/image>` with the saved image path and using the current conversation language.
15. After the image is delivered and saved, provide the pose prompt text in the required format below.

## Batch Processing

Batch processing is allowed when the user uploads multiple images or provides a path that resolves to multiple images.

Before processing images discovered from a directory path, ask the user for confirmation. The confirmation message should include the directory path, the number of supported image files found, and the file list or a concise preview of the file list. Do not start generation for directory-based batches until the user confirms.

For multiple uploaded image attachments, confirmation is not required unless the user asks to review the list first.

During batch processing, report progress before starting each image. Use the current conversation language and include the current index and total count, equivalent to: `Processing image 1/n...`.

Save every batch output under `posture/`. Use stable filenames derived from each input filename, such as `<input-stem>-posture.png`. If a filename already exists, create a non-destructive sibling filename such as `<input-stem>-posture-2.png`.

For each processed image, send or summarize the generated pose image, report its saved path, and provide its bilingual pose prompt text. Keep the output order aligned with the input order.

## Image Generation Constraints

Preserve the selected white model's existing material, light, shadow, and color. A subtle neutral-gray contour or edge shading is allowed only to improve silhouette separation and cutout accuracy. Do not add texture, skin tone, clothing, hair, facial details, accessories, props, background elements, floor, scenery, text, watermark, or decorative effects.

Do not modify the selected template's body proportions based on the uploaded image. Preserve the template's original shoulder width, waist-to-hip ratio, torso length, arm length, leg length, hand/foot scale, and overall body build. Transfer only the pose and gesture, not the reference subject's physique.

The output must be only a clean full-body white model in the extracted pose, isolated on a transparent background. Keep the silhouette readable, gently contoured, and anatomical proportions coherent. Leave enough canvas margin around the body so no body part touches or crosses the image edge.

The transparent background must be real file transparency in the final delivered file. The delivered PNG must contain an alpha channel with transparent pixels outside the mannequin. Its alpha edge should be smooth and anti-aliased, without hard stair-step pixels, obvious halos, or high-saturation color fringe from the temporary background. Do not draw, simulate, or bake in a checkerboard transparency preview.

Native transparent output is not the default strategy. Generate the posed white model on a removable solid-color background first, choosing a color with large visual distance from the mannequin's white/gray tones, then cut out the background in post-processing. The final file must pass the same `RGBA`, alpha transparency, smooth anti-aliased edge, clean contour, full-body, and template-preservation checks before delivery.

## Prompt Pattern

When calling an image generation or image editing model, include the user image as the pose reference and the selected template as the identity/style reference. Use a prompt like:

```text
Create a 1024x1024 image showing the [male/female] white mannequin from the provided template matching only the body pose of the reference subject. Do not generate native alpha or transparent output. Place the mannequin on a flat, solid, high-saturation background with strong color contrast against the white mannequin, such as bright green or bright blue, so it can be removed precisely in post-processing. The background must not be white, off-white, gray, beige, low-saturation, gradient, shadowed, textured, scenic, or checkerboard. Preserve the mannequin's original body proportions, including shoulder width, waist-to-hip ratio, torso length, arm length, leg length, and overall build. Preserve the mannequin's original white material, lighting, and color. Slightly strengthen the mannequin's outer silhouette and major limb separation contours with thin, soft, neutral-gray edge shading; keep it realistic and minimal, not a thick black cartoon or ink outline. Full body visible, no cropped head, hands, feet, or limbs. Do not copy clothing, hair, accessories, facial details, physique, props, scenery, text, or any unrelated detail. Output only the posed white model on the removable solid-color background; the background will be cut out after generation.
```

## AIGC Pose Description

Return short prompt-friendly descriptions after the image is sent to the conversation, saved under `posture/`, and the user has been told where the image was saved. Focus on pose mechanics rather than character identity or styling.

The user-facing pose prompt describes the pose only. Do not frame it as a prompt to generate another white model, mannequin, male/female template, or character identity. Do not start the Chinese description with labels like `全身女性白模姿势：`, `全身男性白模姿势：`, or similar white-model wording. Do not start the English description with labels like `Full-body female white mannequin pose:` or `Full-body male white mannequin pose:`.

The pose prompt output must be bilingual. Always provide both Chinese and English versions, regardless of the current conversation language. Keep the two versions semantically aligned and equally complete. Use the current conversation language for any surrounding delivery text, but keep this prompt block structure:

```text
可用于图片生成的提示词：
<Chinese pose description>

关键词：
<Chinese keyword 1>, <Chinese keyword 2>, <Chinese keyword n>

Image-generation prompt:
<English pose description>

Keywords:
<English keyword 1>, <English keyword 2>, <English keyword n>
```

Avoid mentioning clothing, hairstyle, facial likeness, accessories, background, or any visual detail that should not transfer.

For both `<Chinese pose description>` and `<English pose description>`, describe the pose in one compact paragraph, such as:

```text
[stance/action], head [direction/tilt], torso [angle/rotation], left arm [position], right arm [position], left leg [position], right leg [position], weight balanced on [support point], [gesture mood/energy].
```

For each keyword line, provide concise pose keywords only, such as action type, body orientation, arm placement, leg placement, balance, and gesture energy. The Chinese keywords and English keywords should describe the same pose mechanics.
