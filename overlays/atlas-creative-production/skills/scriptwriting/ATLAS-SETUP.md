> Reference environment notes: these statements describe the original Windows installation, not prerequisites supplied by this installer. Probe your own host before claiming a runtime is installed.

# Atlas installation status

This skill is installed for private use. Source and license are recorded in ATLAS-SOURCE.json and LICENSE.

Python scripts use PEP 723 dependencies: invoke `uv run --script <script.py> ...`.
Python >=3.11, uv and FFmpeg/ffprobe are available. Script dependencies were cached by uv for the tested audio and video QA commands.
Foley synthesis, an eight-second offline mix, audio QA and offline voice metrics passed using synthetic test signals.
Real voice generation, speech transcription, external media judging and image generation were not tested; provider keys and credits remain project requirements.
Shell scripts require Bash. The reference environment used Git Bash 5.3.15 outside PATH; locate a compatible Bash on your own host. All four bundled .sh files passed bash -n; their complete workflows were not executed.
video-director uses the existing imagegen skill. Upstream image craft is retained as its nonregistered references/image-generation/GUIDE.md.
Remotion APIs and dependency versions belong to the installed Remotion skill/project. Do not infer runtime compatibility from this guide alone.

