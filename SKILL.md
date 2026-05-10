---
name: posture-generator
description: Generate a clean transparent-background PNG of a male or female white model matching the pose from a user-provided character image, plus an AIGC-ready pose prompt. Use when the user wants a white mannequin/body template to imitate a reference person's posture while preserving the template body's proportions and removing clothing, hair, accessories, background, and all unrelated visual details.
---

# Posture Generator

Use this skill when the user provides an image and wants a white model to copy the character's pose.

## Inputs

- User reference image containing a person or character.
- White model templates in `template/`:
  - `template/male.png`
  - `template/female.png`

If the image contains multiple people, use the primary/most central subject unless the user identifies another subject. If the subject's gender presentation is unclear, state the uncertainty briefly and choose the closest template.

## Output Defaults

- Pose image format: transparent-background `.png`.
- Pose image size: `1024x1024`.
- Framing: full body, with no cropped head, hands, feet, limbs, or props.
- Model style: clean white model silhouette only.
- Also output a concise pose description suitable for AIGC image-generation prompts.

## Workflow

1. Inspect the reference image.
2. Identify the subject's apparent gender presentation for template selection:
   - Male subject: use `template/male.png`.
   - Female subject: use `template/female.png`.
3. Extract only the body pose:
   - overall stance or seated/lying position
   - head direction and tilt
   - spine/torso angle
   - shoulder and hip rotation
   - arm, hand, leg, and foot placement
   - weight distribution and gesture energy
4. Generate or edit the selected white model template so it matches the reference pose.
5. Export a transparent PNG at `1024x1024`.
6. Provide the AIGC prompt text describing the pose.

## Image Generation Constraints

Preserve the selected white model's existing material, light, shadow, and color. Do not add texture, skin tone, clothing, hair, facial details, accessories, props, background elements, floor, scenery, text, watermark, or decorative effects.

Do not modify the selected template's body proportions based on the uploaded image. Preserve the template's original shoulder width, waist-to-hip ratio, torso length, arm length, leg length, hand/foot scale, and overall body build. Transfer only the pose and gesture, not the reference subject's physique.

The output must be only a clean full-body white model in the extracted pose, isolated on a transparent background. Keep the silhouette readable and anatomical proportions coherent. Leave enough canvas margin around the body so no body part touches or crosses the image edge.

## Prompt Pattern

When calling an image generation or image editing model, include the user image as the pose reference and the selected template as the identity/style reference. Use a prompt like:

```text
Create a transparent-background PNG, 1024x1024, showing the [male/female] white mannequin from the provided template matching only the body pose of the reference subject. Preserve the mannequin's original body proportions, including shoulder width, waist-to-hip ratio, torso length, arm length, leg length, and overall build. Preserve the mannequin's original white material, lighting, color, and clean contour. Full body visible, no cropped head, hands, feet, or limbs. Do not copy clothing, hair, accessories, facial details, physique, props, background, scenery, text, or any unrelated detail. Output only the posed white model on transparency.
```

## AIGC Pose Description

Return a short prompt-friendly description after the image. Focus on pose mechanics rather than character identity or styling:

```text
Full-body [male/female] figure pose: [stance/action], head [direction/tilt], torso [angle/rotation], left arm [position], right arm [position], left leg [position], right leg [position], weight balanced on [support point], [gesture mood/energy].
```

Avoid mentioning clothing, hairstyle, facial likeness, accessories, background, or any visual detail that should not transfer.
