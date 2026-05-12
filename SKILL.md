---
name: posture-extractor
description: Generate clean transparent-background PNGs of male or female white models matching poses from one or more user-provided character images, plus same-path Markdown files containing bilingual AIGC-ready pose prompts. Use when the user wants white mannequin/body templates to imitate reference postures while preserving template body proportions and removing clothing, hair, accessories, background, and all unrelated visual details.
---

# Posture Extractor

Use this skill when the user provides one or more person or character images and wants a white model to copy only the body pose.

## Inputs

- Reference image(s), provided as uploaded image attachments, image file paths, or a directory path.
- Path-style invocation is supported, for example: `/posture-extractor path/to/image`.
  - Resolve relative paths from the current working directory.
  - If a path does not exist, ask for a valid image or directory path.
  - If a path is a directory, collect supported image files and ask for confirmation before generating.
- White model templates:
  - `template/male.png`
  - `template/female.png`

Supported image extensions: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`, `.tiff`.

If an image contains multiple people, use the primary or most central subject unless the user identifies another one. If gender presentation is unclear, state the uncertainty briefly and choose the closest template.

## Output Contract

- Final pose image: target-path `1024x1024` transparent-background `RGBA` PNG that exists on disk and passes the validation checks below. A conversation-visible generated image is not a saved PNG deliverable by itself.
- Final image content: one clean full-body white model with no cropped head, hands, feet, limbs, props, or facial features. The head must stay smooth and featureless; preserve only head direction and tilt.
- Final response images: only the validated transparent cutout PNG(s). Do not attach, display, or present the original reference image, template image, solid-background generation, uncut `RGB` image, checkerboard preview, conversation-only image, or any other intermediate image unless the user explicitly asks for diagnostic artifacts.
- Prompt file: sibling Markdown file with the same basename, containing only the bilingual pose prompt block unless the user asks for extra notes.
- For source file paths, save outputs beside each source image as `<input-stem>-posture.png` and `<input-stem>-posture.md`; if needed, use a non-destructive suffix such as `<input-stem>-posture-2`.
- For uploaded attachments without an accessible source path, save outputs under `posture/` in the current working directory.
- For multiple inputs, process independently and keep output order aligned with input order.

## Workflow

1. Resolve the reference image(s). If both uploads and paths are present, use uploads unless the user explicitly asks to use the paths too.
2. Select `template/male.png` or `template/female.png` from the subject's apparent gender presentation.
3. Extract only pose mechanics: stance or seated/lying position, head direction and tilt, torso angle, shoulder and hip rotation, arm/hand placement, leg/foot placement, weight distribution, and gesture energy.
4. Generate or edit the selected template so it matches the reference pose. Use a valid image generation or editing tool as defined below; do not draw the model manually.
5. Generate on a flat, high-saturation solid chroma background such as bright green or bright blue. Do not request native alpha, transparent background, transparent-background PNG style, cutout-on-transparent style, checkerboard transparency, or transparency previews.
6. If using Codex conversation image generation, locate the generated raster before post-processing. Check `$CODEX_HOME/generated_images/` if `CODEX_HOME` is set, otherwise check `~/.codex/generated_images/`; use the newest PNG created for the current generation, then copy it to a working path. Do not assume the conversation image has already been saved to the target output path.
7. Remove the solid background with background removal, chroma key, matting, or local cutout tools. Use edge smoothing and color-spill cleanup; export the final PNG at `1024x1024`.
8. Validate the PNG against the checks below. Treat any visible solid background, `RGB` mode output, missing alpha channel, uncut generation, or missing target file as a failed final image, not as an acceptable companion output. Retry post-processing first for cutout failures; regenerate only when the source image or template preservation is invalid.
9. Write the sibling Markdown prompt file using the exact bilingual block format below.
10. Send only the validated transparent cutout PNG to the conversation, report the PNG and Markdown paths when available, and provide the same bilingual pose prompt text. If the target PNG could not be created and validated, say so explicitly and do not present any image as the final PNG output.

## Valid Generation Channels

The generation/editing step is required. A valid tool can use both the selected white-model template and the user reference image as visual context through explicit image inputs, local image paths, uploaded attachments, or visible conversation images.

For Codex, the built-in conversation image generation/editing capability is valid when it can see or use the reference image and selected template. Do not refuse just because there is no shell API key or the tool does not immediately return a local file path.

If the generation tool first returns only an in-conversation image, use any available export, cache, attachment, download, file-save mechanism, or Codex generated-image cache to obtain a local raster file before cutout and validation. If no local raster can be accessed after a valid image is generated, do not fabricate a PNG with drawing code, do not send the generated image as an output substitute, and clearly state that local PNG saving, cutout, and alpha validation could not be completed.

If no image generation or editing capability of any kind is available, stop and tell the user the pose image cannot be generated reliably in this session. You may still provide the bilingual pose description if useful.

## Prohibited Fallbacks

Do not replace generation/editing with a local drawing script, SVG, canvas, vector tracing, skeleton overlay, geometric mannequin, or hand-built figure made from polygons, ellipses, lines, or limb shapes.

Programmatic tools may only be used after template-preserving image generation/editing has produced the posed mannequin, and only for post-processing, background removal, alpha validation, file conversion, or diagnostics.

## Generation Rules

- Preserve the selected template's body proportions, including shoulder width, waist-to-hip ratio, torso length, arm length, leg length, hand/foot scale, and overall build.
- Preserve the template's white material, lighting, smooth body volumes, and light/shadow character.
- Transfer only the pose and gesture. Do not copy clothing, hair, accessories, props, facial likeness, facial features, expression, physique, scenery, text, watermark, or background details.
- Keep the head smooth and featureless. Facial anatomy or expression details are invalid even if they are generic and not copied from the reference.
- Keep the full body visible with enough canvas margin so no body part touches or crosses the image edge.
- Use one removable, flat, high-saturation solid chroma background with strong contrast against the white mannequin. Avoid white, off-white, gray, beige, low-saturation colors, gradients, shadows, textures, scenery, transparency previews, alpha-style cutouts, and checkerboards.
- A thin, soft, neutral-gray contour or edge shading is allowed only to improve silhouette separation. Do not use thick black, cartoon, inked, or decorative outlines.
- If the generated image contains a baked checkerboard, transparency preview, gradient, texture, or non-solid background, discard it and regenerate on a clean solid background. Do not attempt checkerboard-removal as a workaround.

## Validation Checks

Before delivery, verify:

- The target sibling PNG exists on disk at the reported path.
- The file is a real `RGBA` PNG, not `RGB`.
- The image dimensions are exactly `1024x1024`.
- The alpha channel contains transparent pixels outside the mannequin.
- The silhouette edge is smooth and anti-aliased, without stair-step jaggies, harsh halos, or green/blue fringe.
- No visible background, solid color, or checkerboard preview remains.
- The mannequin still visibly preserves the selected template's proportions, material, lighting, and white-model style.
- The head is smooth and featureless, with no visible eyes, pupils, eyebrows, nose, nostrils, mouth, lips, teeth, eyelashes, makeup, face markings, or expression detail.
- The result is not a geometric pose diagram, ball-joint figure, polygon body, manually drawn mannequin, or skeleton-like illustration.

Technical validity such as `RGBA`, `1024x1024`, transparency, and anti-aliasing is necessary but not sufficient. Template identity and visual fidelity are required.

## Batch Processing

Batch processing is allowed for multiple uploads or a path that resolves to multiple images.

For directory paths, ask for confirmation before generating. Include the directory path, the number of supported images found, and the file list or a concise preview.

For multiple uploaded attachments, confirmation is not required unless the user asks to review the list first.

During batch processing, report progress before starting each image, for example: `Processing image 1/n...`.

## Prompt Pattern

When calling an image generation or editing model, include the user image as the pose reference and the selected template as the identity/style reference. If the tool supports explicit image arguments, attach both images. If the tool uses conversation context instead, make sure both images are visible or attached before calling the tool, and name their roles in the prompt.

Use a prompt like:

```text
Create a 1024x1024 image showing the [male/female] white mannequin from the provided template matching only the body pose of the reference subject. Do not generate native alpha, transparent background, transparent-background PNG style, cutout-on-transparent style, checkerboard transparency, or any transparency preview. Place the mannequin on one flat, solid, high-saturation chroma background color with strong contrast against the white mannequin, such as bright green or bright blue, so that single color can be removed precisely in post-processing. Preserve the mannequin's original body proportions, white material, lighting, and overall build. Slightly strengthen the outer silhouette and major limb separation contours with thin, soft, neutral-gray edge shading; keep it realistic and minimal. Full body visible, no cropped head, hands, feet, or limbs. Keep the head smooth and featureless; do not include eyes, pupils, eyelashes, eyebrows, nose, nostrils, mouth, lips, teeth, ears with inner detail, makeup, face markings, facial expression, or any other facial detail. Do not copy clothing, hair, accessories, facial details, physique, props, scenery, text, or any unrelated detail. Output only the posed white model on the removable solid-color chroma background; the background will be cut out after generation.
```

## AIGC Pose Description

Return short prompt-friendly descriptions after the PNG and sibling Markdown prompt file have been saved, or after explaining why local PNG saving was not possible. Focus on pose mechanics rather than character identity or styling.

The user-facing pose prompt describes the pose only. Do not frame it as a prompt to generate another white model, mannequin, male/female template, or character identity. Do not start the Chinese description with labels that mean "full-body female white mannequin pose", "full-body male white mannequin pose", or similar white-model wording. Do not start the English description with labels like `Full-body female white mannequin pose:` or `Full-body male white mannequin pose:`.

Always provide semantically aligned Chinese and English versions. Use the current conversation language for surrounding delivery text, but keep this prompt block structure:

```text
可用于图片生成的提示词：
<中文姿态描述>

关键词：
<中文关键词 1>, <中文关键词 2>, <中文关键词 n>

Image-generation prompt:
<English pose description>

Keywords:
<English keyword 1>, <English keyword 2>, <English keyword n>
```

Avoid mentioning clothing, hairstyle, facial likeness, accessories, background, or any visual detail that should not transfer.

Describe the pose in one compact paragraph per language, using details such as stance/action, head direction, torso angle, arm placement, leg placement, support point, balance, and gesture energy.

For each keyword line, provide concise pose keywords only. The Chinese and English keywords should describe the same pose mechanics.
