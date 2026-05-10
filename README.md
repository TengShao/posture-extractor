# Posture Generator

[English](#posture-generator) | [中文](#姿势生成器)

Posture Generator is an agent skill for creating clean white-model pose references from an uploaded character or person image. It extracts the subject's pose, applies it to a male or female white-model template, and outputs both a transparent PNG pose image and an AIGC-ready pose description. It keeps only the subject's action and removes character-specific styling and scene details such as clothing, hair, accessories, props, backgrounds, and facial likeness.

## Templates

White-model templates are stored in:

```text
template/
├── female.png
└── male.png
```

`female.png` is used for female-presenting subjects, and `male.png` is used for male-presenting subjects.

## Installation

Send this to an agent that can install local skills:

```text
Install the skill from https://github.com/TengShao/Posture-Generator and keep the installed skill name as posture-generator.
```

Restart the agent application after installation. In Codex, invoke it with `$posture-generator`.

---

# 姿势生成器

[English](#posture-generator) | [中文](#姿势生成器)

姿势生成器是一个 agent skill，用于根据用户上传的人物或角色图片生成干净的白模姿势参考图。它会提取参考图中主体的姿势，应用到男性或女性白模模板上，并输出透明背景 PNG 姿势图和一段可用于 AIGC 图片生成的动作描述。它只保留主体动作，去掉服饰、头发、饰品、道具、背景、面部相似性等角色造型和场景细节。

## 模板

白模模板位于：

```text
template/
├── female.png
└── male.png
```

`female.png` 用于女性主体，`male.png` 用于男性主体。

## 安装

把下面这段话发送给支持安装本地 skill 的 agent：

```text
请从 https://github.com/TengShao/Posture-Generator 安装这个 skill，并保持安装后的 skill 名称为 posture-generator。
```

安装后重启对应的 agent 应用。在 Codex 中，可以通过 `$posture-generator` 调用。
