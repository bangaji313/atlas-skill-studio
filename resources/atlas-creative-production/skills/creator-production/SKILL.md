---
name: creator-production
description: Plan and deliver an end-to-end creator video, from audience and concept through script, storyboard, animation or footage, voice, music, sound effects, captions, editing, quality checks and export. Use for a complete production workflow or a multi-stage creator project, rather than an isolated render or API integration.
---

# Creator production

Turn the user's brief into an editable production and a verified delivery file. Use their requested format, language, audience, runtime and supplied material. If they delegate the creative decisions, choose reasonable defaults and record them; ask only for inputs that actually block production.

## Choose the production path

- For an agent-directed production with footage, pipeline stages and a tool registry, use [OpenMontage](../openmontage/SKILL.md). Its provider menu distinguishes configured services from local capabilities.
- For a reusable semantic video composition with generated or supplied material, use [Hypit](../hypit/SKILL.md). Use its local/code-rendered path when generation services are not configured.
- For a film in a named visual style, use [Lemo-Opuscar](../lemo-opuscar/SKILL.md).
- For a product promo from real screens and shot cards, use [Video Shotcraft](../video-shotcraft/SKILL.md).
- For editable HTML motion graphics, use [HyperFrames](../hyperframes/SKILL.md); for React compositions, use [Remotion](../remotion-best-practices/SKILL.md).

Pick one renderer for a production unless a separate asset genuinely benefits from another tool. Preserve an existing project and its pinned dependencies. A host without file execution can develop the brief, script and shot plan, but cannot claim a local render occurred.

## Produce the work

1. Write the production brief: audience, purpose, platform, language, aspect ratio, target duration, key message and delivery requirements. For audience or topic research, use the relevant installed Atlas Growth & Social skill when available; do not invent engagement evidence.
2. Develop the hook, structure, narration and on-screen text with [scriptwriting](../scriptwriting/SKILL.md). Produce a shot list with durations, visuals, spoken lines and audio cues. Revise the timing to fit the actual narration rather than rushing it to an arbitrary length.
3. Use supplied material, original code animation, licensed stock or a configured generation service. Record source and usage information for external assets. Use [visual-style](../visual-style/SKILL.md) to maintain the visual direction and the chosen production skill for storyboards and assets.
4. Direct narration with [voice-direction](../voice-direction/SKILL.md). When the user selects ElevenLabs, use [text-to-speech](../text-to-speech/SKILL.md). For supplied speech, use [speech-to-text](../speech-to-text/SKILL.md) and correct captions against the audio.
5. Score and mix with [sound-design](../sound-design/SKILL.md), [music](../music/SKILL.md) and [sound-effects](../sound-effects/SKILL.md), choosing only configured services or provided/local assets. Confirm the selected provider and actual cost-bearing operation before paid generation where required by the host; installation supplies no credits or credentials.
6. Build and edit with the selected production path. Read the reference video as a creative input; do not assume permission to impersonate its presenter or redistribute its footage. Check motion continuity, pacing, subtitle line breaks, safe areas, color and speech intelligibility.
7. Render a short representative section before an expensive full render. Check the exported file with FFprobe for duration, resolution, frame rate, video/audio streams and decodability. Inspect representative frames at starts, transitions and the ending; listen to the audio when an audio playback tool is available. State any check that could not be performed.
8. Deliver the final media file, editable project, concise production notes and asset credits. Report provider/runtime limitations specifically. Publishing or scheduling is a separate action governed by the user's request; exporting a video does not publish it.

## Completion record

Keep the record proportional to the job: production path and versions, final output path, format and duration, assets/providers used, checks that passed, and any remaining issue. A skill being discoverable is not proof that its external provider or every production branch has been tested.
