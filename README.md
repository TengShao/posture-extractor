# Posture Extractor

[English](#posture-extractor) | [中文](#姿态提取器)

Posture Extractor is an agent skill for creating clean white-model pose references from an uploaded character or person image. It extracts the subject's pose, applies it to a male or female white-model template, and outputs both a transparent PNG pose image and bilingual Chinese-English AIGC-ready pose descriptions. The workflow generates the posed white model on a high-contrast solid-color background first, with a subtly strengthened contour for cleaner separation, then locates the generated raster, removes the background as a post-processing step, and validates the saved transparent PNG with smooth anti-aliased edges. Only the validated transparent cutout PNG is a final image output; solid-background generations, uncut images, checkerboard previews, templates, and other intermediate images must not be delivered unless explicitly requested for diagnostics. It keeps only the subject's action and removes character-specific styling and scene details such as clothing, hair, accessories, props, backgrounds, facial likeness, facial features, and expression details. The final white-model head must stay smooth and featureless, preserving only head direction and tilt.

## Templates

White-model templates are stored in:

```text
template/
├── female.png
└── male.png
```

`female.png` is used for female-presenting subjects, and `male.png` is used for male-presenting subjects.

## Usage

Provide an image directly, or pass an image path when invoking the skill. Codex uses `$posture-extractor`; Openclaw, Hermes Agent, and Claude Code use `/posture-extractor`.

```text
$posture-extractor path/to/image
/posture-extractor path/to/image
```

## Sample

![Posture Extractor sample](Sample.jpg)

## Installation

Send this to an agent that can install local skills:

```text
Install the skill from https://github.com/TengShao/posture-extractor and keep the installed skill name as posture-extractor.
```

---

# 姿态提取器

[English](#posture-extractor) | [中文](#姿态提取器)

姿态提取器是一个 agent skill，用于根据用户上传的人物或角色图片生成干净的白模姿态参考图。它会提取参考图中主体的姿态，应用到男性或女性白模模板上，并输出透明背景 PNG 姿态图和中英双语的 AIGC 图片生成动作描述。工作流会先生成带高色差纯色背景、轮廓线略微强化的白模姿态图，再找到生成图落盘文件，经过带抗锯齿边缘处理的后处理抠图，并校验保存后的透明 PNG。只有通过校验的透明抠图 PNG 才是最终图片输出；纯色背景生成图、未抠图图片、棋盘格预览、模板图和其他中间图片都不能交付，除非用户明确要求用于诊断。它只保留主体动作，去掉服饰、头发、饰品、道具、背景、面部相似性、五官和表情细节等角色造型和场景细节。最终白模头部必须保持光滑无五官，只保留头部朝向和倾斜。

## 模板

白模模板位于：

```text
template/
├── female.png
└── male.png
```

`female.png` 用于女性主体，`male.png` 用于男性主体。

## 使用方式

可以直接上传图片，也可以在唤醒 skill 时传入图片路径。Codex 使用 `$posture-extractor`；Openclaw、Hermes Agent、Claude Code 使用 `/posture-extractor`。

```text
$posture-extractor path/to/image
/posture-extractor path/to/image
```

## 示例

![姿态提取器示例](Sample.jpg)

## 安装

把下面这段话发送给支持安装本地 skill 的 agent：

```text
请从 https://github.com/TengShao/posture-extractor 安装这个 skill，并保持安装后的 skill 名称为 posture-extractor。
```
