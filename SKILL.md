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
- Model style: clean white model silhouette only.
- Also output a concise pose description suitable for AIGC image-generation prompts.

## Workflow

1. Resolve reference image(s):
   - If the user uploaded one or more images, use those images directly.
   - If the user provided `/posture-generator path/to/image`, resolve and load the provided path(s).
   - If a provided path is a directory, collect all supported image files inside it and ask for confirmation before processing.
   - If both uploaded images and paths are present, use uploaded images unless the user explicitly says to use the paths too.
2. Prefer an image generation or editing API/tool that supports explicit output parameters. Set `background: transparent`, `output_format: png`, `size: 1024x1024`, and `quality: high` when those parameters are available. If the active tool only accepts a prompt, state that the file requirements will be enforced by validation and regeneration.
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
7. Generate or edit the selected white model template so it matches the reference pose.
8. Export a transparent PNG at `1024x1024`.
9. Validate the exported file before delivery:
   - The file must be a real `RGBA` PNG, not `RGB`.
   - The alpha channel must contain transparent pixels outside the mannequin.
   - A checkerboard transparency preview, solid color background, or any visible background is invalid.
10. If native transparent output validation fails, try regenerating or re-editing for native transparency first.
11. If native transparent output still fails after reasonable attempts, fall back to post-processing transparency:
   - Prefer a flat chroma-key background workflow when possible.
   - Use background removal, chroma-key removal, matting, or local cutout tools only as fallback.
   - Re-run validation after fallback processing; the final delivered file must still be a real `RGBA` PNG with transparent pixels outside the mannequin.
   - If fallback processing creates messy edges, color fringe, missing body parts, or altered mannequin appearance, reject the result and try again.
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

For each processed image, send or summarize the generated pose image, report its saved path, and provide its pose prompt text. Keep the output order aligned with the input order.

## Image Generation Constraints

Preserve the selected white model's existing material, light, shadow, and color. Do not add texture, skin tone, clothing, hair, facial details, accessories, props, background elements, floor, scenery, text, watermark, or decorative effects.

Do not modify the selected template's body proportions based on the uploaded image. Preserve the template's original shoulder width, waist-to-hip ratio, torso length, arm length, leg length, hand/foot scale, and overall body build. Transfer only the pose and gesture, not the reference subject's physique.

The output must be only a clean full-body white model in the extracted pose, isolated on a transparent background. Keep the silhouette readable and anatomical proportions coherent. Leave enough canvas margin around the body so no body part touches or crosses the image edge.

The transparent background must be real file transparency in the final delivered file. The delivered PNG must contain an alpha channel with transparent pixels outside the mannequin. Do not draw, simulate, or bake in a checkerboard transparency preview.

Native transparent output is preferred. If native transparency fails validation after reasonable attempts, fallback post-processing is allowed. The fallback may use background removal, chroma-key removal, matting, or local cutout tools, but the final file must pass the same `RGBA`, alpha transparency, clean contour, full-body, and template-preservation checks before delivery.

## Prompt Pattern

When calling an image generation or image editing model, include the user image as the pose reference and the selected template as the identity/style reference. Use a prompt like:

```text
Create a transparent-background PNG, 1024x1024, showing the [male/female] white mannequin from the provided template matching only the body pose of the reference subject. Prefer native true transparency: the output file itself should contain a real alpha channel, with pixels outside the mannequin transparent in the PNG file. Do not render a checkerboard transparency preview. Preserve the mannequin's original body proportions, including shoulder width, waist-to-hip ratio, torso length, arm length, leg length, and overall build. Preserve the mannequin's original white material, lighting, color, and clean contour. Full body visible, no cropped head, hands, feet, or limbs. Do not copy clothing, hair, accessories, facial details, physique, props, background, scenery, text, or any unrelated detail. Output only the posed white model on true transparency.
```

## AIGC Pose Description

Return a short prompt-friendly description after the image is sent to the conversation, saved under `posture/`, and the user has been told where the image was saved. Focus on pose mechanics rather than character identity or styling.

Use the current conversation language for the section labels. Keep this structure:

```text
<localized label meaning "The following can be used as an image-generation prompt:">
<pose description>

<localized label meaning "Keywords:">
<keyword 1>, <keyword 2>, <keyword n>
```

Avoid mentioning clothing, hairstyle, facial likeness, accessories, background, or any visual detail that should not transfer.

For `<pose description>`, describe the pose in one compact paragraph, such as:

```text
Full-body [male/female] figure pose: [stance/action], head [direction/tilt], torso [angle/rotation], left arm [position], right arm [position], left leg [position], right leg [position], weight balanced on [support point], [gesture mood/energy].
```

For `<keyword 1>, <keyword 2>, <keyword n>`, provide concise pose keywords only, such as action type, body orientation, arm placement, leg placement, balance, and gesture energy.
