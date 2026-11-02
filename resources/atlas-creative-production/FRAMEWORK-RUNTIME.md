# Atlas framework runtime

These are portable skill instructions with their local references and helpers.
The merge registers no session-start hooks, MCP servers, slash-command handlers,
or global settings. Invoking Ponytail applies its conversational mode to the
current chat; its original native plugin may still activate independently.

Read a requested skill from the host's skill catalog. In Codex, use the Atlas
package-qualified name when supported, or open the SKILL.md at its catalog path.
In ChatGPT, attached or installed skill instructions require the corresponding
file, shell, browser, and multi-agent tools to be available; an account plugin
does not itself supply a local shell, Node, Python, Git, Bash, or subagents.
If a capability is unavailable, explain that limitation and use the documented
inline or text workflow. Never fabricate tool execution.

Current system/developer instructions and the actual tool schema take priority.
Do not change host configuration or enable agents merely because an upstream
guide suggests it. Use agents only when authorized and available. Inherit the
parent model/effort unless an explicit request or applicable instruction allows
an override; obey the current host's fork and model restrictions.

Resolve helper paths relative to the actual installed skill folder, not the
project working directory. Run Bash helpers through a compatible Bash runtime;
Windows PowerShell does not interpret shell scripts. Node/Python/Graphviz are
optional helper requirements and are not installed by this payload. No target
helper was executed during packaging. Stop on errors instead of claiming a
helper ran. Existing user authorization governs file changes and git actions.

Superpowers' optional visual companion is an authenticated local Node server.
It remains opt-in through the skill. The packaged copy disables remote brand
image loading, preserving local functionality without that tracking request.
Keep the loopback bind unless the user explicitly requests remote exposure;
protect its session key and session files. Before deleting a session directory,
resolve it and verify it is the intended temporary session, never a parent.
Diagnostics can inspect chat transcripts; review and redact the local report
before sharing, and obtain explicit permission before posting any issue.

Anti Slop may read its documented global mode preference as data. Its bundled
contrast Python files are optional local helpers; the MCP helper is not
registered or started. Its formula remains usable without Python.
Ponytail's native hook configuration, prompt band, session import, plugin
marketplace update commands and native auto-activation belong to the separate
upstream installation. They are not installed or managed by this Atlas merge.
