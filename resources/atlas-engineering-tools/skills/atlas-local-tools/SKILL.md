---
name: atlas-local-tools
description: "Set up and diagnose optional Atlas integrations for Penpot, Blender, SkillSpector and TradingAgents. Use when connecting a local runtime, not for general design or research advice."
---

# Atlas local integrations

Probe the current host before claiming a dependency or connection exists. This plugin installs instructions, not applications, credentials or MCP servers. Respect the actual host tools and permissions.

## Penpot
Follow https://github.com/penpot/penpot/blob/develop/docs/mcp/index.md for the official MCP. Start the server locally, open a design, load its browser plugin and connect that design session. A listening server alone does not establish a design connection. Keep secrets outside chat and preserve existing files.

## Blender
Use https://github.com/ahujasid/mcp-for-blender for the matching server and addon. Inspect the installed Blender version, open a scene and start with a read-only scene-information call. Preserve the user's scene. Optional generation providers need their own accounts.

## TradingAgents
See https://github.com/TauricResearch/TradingAgents. Create an isolated environment from the selected release and inspect its CLI help. The user configures model and market-data providers separately. Do not run paid analysis or trades as an installation check, solicit secrets in chat, or present generated research as a verified market result.

## SkillSpector
Follow https://github.com/NVIDIA/SkillSpector. Probe the installed CLI version and use a static, no-LLM scan when available. Save JSON outside the scanned tree and retain failures; an empty scan is not a safety verdict. Model-backed scans require the user's configured provider.
