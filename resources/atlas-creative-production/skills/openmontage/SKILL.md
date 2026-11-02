---
name: openmontage
description: Plan and produce videos from concepts, scripts, supplied footage, animation, effects, narration and music with OpenMontage pipelines, checkpoints, local FFmpeg, Remotion and HyperFrames.
---

# OpenMontage

Use for a complete video production or an OpenMontage project. For one local media edit, use ffmpeg or video-edit. For existing Atlas Remotion/HyperFrames tasks, continue using those native skills.

## Runtime and working directory

Portability: the paths and test results below describe the original Windows reference environment. On a new host, provision dependencies in an isolated environment for the bundled `runtime/` or a verified upstream checkout; resolve its actual location before running any command. The installer does not create this environment.

On this Windows installation the tested runtime is `$env:USERPROFILE/.local/share/atlas/OpenMontage`. Use its `.venv/Scripts/python.exe` and run commands with that runtime as the working directory. Do not use a global Python. Production projects belong under `projects/<project-id>/` with explicit output paths.

Read `AGENT_GUIDE.md` and the relevant manifest in `pipeline_defs/` from the installed runtime before production. It contains concept → script → scene plan → assets → edit → render, source/reference review, cost tracking and stage review. The guide's production rules apply to OpenMontage production; they do not govern unrelated tasks or this plugin's installation checks.

Run preflight before offering a production path:

```powershell
Set-Location "$env:USERPROFILE/.local/share/atlas/OpenMontage"
& ./.venv/Scripts/python.exe -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"
```

Report actual capability availability. A configured provider is not proof of successful generation. Do not print credentials. Provider API calls can cost money; follow the user's authorized provider/model and budget. Missing model weights or credentials require setup before those capabilities work. Never silently replace approved motion with still images or switch render engines.

Read each pipeline stage's director guide before that stage. Follow the manifest's approval/checkpoint fields, review outputs, and respect explicit user authorization recorded through OpenMontage's approval policy. For an open brief, begin with concepts and the pipeline/tool plan; for supplied footage, inspect the media first. Keep provider, runtime, music and asset choices visible to the user.

## Bundled portable support

`runtime/` contains pinned OpenMontage code, pipeline manifests, stage guides, schemas, style playbooks and composer source. It excludes virtual environments, node_modules, generated media and model weights. On another machine, copy it into a writable directory and install `requirements.txt` in an isolated Python environment, then `npm ci` inside `remotion-composer/`. Do not install GPU extras or download models until needed for an authorized production.

Technology/provider references under `runtime/.agents/skills/<name>/` use **SKILL.reference.md** so they are supporting documents rather than duplicate skill entrypoints. Resolve a tool's `agent_skills` names to the installed runtime's original `.agents/skills/<name>/SKILL.md` first, otherwise the bundled reference or the same named native plugin skill. Large alternate HyperFrames/Remotion packs are omitted here; use the installed Atlas skills, or original runtime source if needed. `runtime/skills/core/` and `runtime/skills/meta/` contain shared execution and review guidance.

Local animation knowledge exposed separately includes character rigging, SVG/canvas animation, GSAP, Three.js, visual style, and ManimCE. These knowledge packs do not prove their optional renderers/models are installed. Use the character-animation pipeline for rigged characters; use animation or animated-explainer for motion graphics. Audio generation/transcription uses the canonical installed provider skills; OpenMontage keeps provider-specific references internally.

## Verification

On this machine core contract tests and a local synthetic clip check passed. The smoke check covers trim, audio extraction/mixing/fades, composition, color grade, burned subtitles, frame extraction, and media structure. To repeat it without provider calls:

```powershell
& "$env:USERPROFILE/.local/share/atlas/OpenMontage/.venv/Scripts/python.exe" '<this-skill-directory>/smoke.py' "$env:USERPROFILE/.local/share/atlas/OpenMontage"
```

It overwrites only generated fixtures in `projects/atlas-install-smoke/`. A four-second synthetic render is a local integration check, not an end-to-end generated production. Inspect and listen to the actual deliverable and run pipeline quality review before presenting it.

OpenMontage code is AGPL-3.0; preserve `LICENSE`. Native reference packs can carry additional upstream license notices. Check provider/media/model terms for the specific production.
