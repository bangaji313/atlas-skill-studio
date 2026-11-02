# Verification record — 1.3.0

Checked locally on Windows, 2 November 2026. These are packaging and bounded runtime checks, not a guarantee that every production workflow or provider will run on every host.

| Check | Result | Scope |
|---|---|---|
| Full source-pinned build | PASS | 8,163 recipe files reconstructed from 31 verified upstream source archives; upstream and output SHA-256 checks passed |
| Live Git sparse/partial source path | PASS | Growth studio built from a fresh Git source cache, including 79 skills / 782 recipe files; archive cache not used for this check |
| Assembler unit tests | PASS — 7 tests | Catalog uniqueness, path traversal/control characters/Git-directory rejection, symlink escape, patch ranges, line endings, local payload checks, and full-guide adaptation without modifying other host copies |
| Antigravity native validation | PASS — strict | CLI 1.4.5; Growth 79, Creative 79, Engineering 69; no findings |
| Claude native validation | PASS — strict | Claude Code 2.1.303; all three plugin manifests; local marketplace validation also passed |
| Codex native reading | PASS | App-server `plugin/read` parsed the local marketplace and discovered 79 / 79 / 69 skill entrypoints without installing the packages globally |
| README artwork | PASS — visual review | Hero and architecture rendered to PNG and inspected; accessible vector titles/descriptions included |

## Antigravity long-skill adaptation

The native validator reported that skill bodies exceeding 24,000 bytes are truncated. The Antigravity adapter now preserves original trigger metadata, places the complete instructions beside the entrypoint as `ATLAS-FULL-GUIDE.md`, and uses a short entrypoint directing the agent to read it before working. Nine Growth, five Creative and four Engineering skills use this adapter. Native strict validation passes after the change. Codex and Claude instruction copies are not replaced by these wrappers.

## Evidence inherited from the private 1.2.1 reference installation

- 227 unique skills were installed, enabled and discoverable after the five original source plugins were removed.
- 8,172 installed skill/support files matched the prepared reference release. The public assembler intentionally excludes old root metadata, generates host manifests, normalizes text line endings and removes owner-specific runtime assumptions; its recipe-file count is a different measurement.
- Hypit CLI 0.3.1 rendered a local two-scene 3-second 360×640 / 30 fps H.264/AAC fixture; all 10 specification checks passed. An upstream duplicate-window fixture had failed before the input was corrected.
- OpenMontage passed 109 contract/regression tests, discovered 155 tools and completed local FFmpeg trim, audio extraction/mix/fade, composition, grading, subtitle and frame/metadata checks.
- Local Foley/audio mixing passed the continuous eight-second fixture. A sparse three-second loudness fixture missed the target and was not treated as a pass.

These are reference-environment results. The public installer does not install those renderer environments or transfer their credentials.

## Not verified / not supplied

- Upload and account activation in Claude Desktop/Chat/Cowork, and actual GUI skill execution in Antigravity Desktop. Native local format validation does not prove cloud acceptance or plan permissions.
- End-to-end tasks for all 227 skills; paid provider calls, model downloads, GPU pipelines, live social publishing, or Penpot design changes.
- Live sparse Git retrieval of every source repository; all sources passed the full verified-archive build, while the fresh Git network test covered Growth’s sources.
- Universal security certification. Earlier static SkillSpector framework scans had warnings and partial coverage; helper/shell/Git instructions require task-appropriate review. A recursive OpenMontage scan timed out and was not treated as clean.
- Local applications, cloud accounts, API credits or service permissions. See RUNTIME.md and THIRD_PARTY_NOTICES.md.

## Repeat the checks

```sh
python -m unittest discover -s tests -v
python atlas.py build
```

Open the directory from `dist/latest-build.json`, then run the native commands on its package paths:

```sh
agy plugin validate <build>/antigravity/plugins/atlas-creative-production --strict --json
claude plugin validate <build>/claude/plugins/atlas-creative-production --strict --json
claude plugin validate <build>/claude --json
```

Repeat per studio. Use each host’s actual installed-plugin list and a small task to verify an installation after enabling it. No GitHub Actions workflow or CI badge is used for these locally recorded checks.
