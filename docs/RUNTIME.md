# Runtime and host boundaries

Atlas packages instructions and their supporting references/helpers. It does not supply the host agent, a model subscription, a shell, API keys, local applications or preconfigured MCP connections.

Use the actual host’s tools and permissions. A tool name in an upstream example may need to be translated to an available host tool; never invent a successful tool call. Instruction priority and existing user authorization still apply. A host without local execution can plan, write and reason from a skill, but cannot claim it rendered a local video, edited a Blender scene, simulated a circuit or ran a test.

| Workflow | Additional setup |
|---|---|
| Copy, concepts, scripts and research planning | An appropriate model and, for factual retrieval, permitted search/source access |
| Hypit / Remotion / HyperFrames / Lemo | Matching Node/Python environments, browser/FFmpeg and selected renderer dependencies |
| OpenMontage | An isolated Python environment for its bundled runtime or pinned upstream checkout; use its preflight before choosing providers |
| Voice, music, dubbing and hosted generation | Chosen provider account, credentials, plan permissions and credits |
| ComfyUI, ACE-Step, Manim and model workflows | Separate application/model/renderer installation, and GPU/LaTeX where required |
| KiCad / wiring / SPICE | Compatible KiCad/pcbnew, WireViz/Graphviz; a SPICE simulator for actual simulation |
| Penpot / Blender | Compatible application/MCP server and an active connected design/scene session |
| Social data / analytics / publishing | Authorized provider/account connections such as ScrapeCreators or Publora |

Reference-environment installation notes retained from upstream integrations are historical evidence, not a dependency probe on your computer. The portable distribution removes the owner-specific Impeccable/Lemo launcher assumptions. Generated material is not automatically approved for publication, fabrication or commercial use; review the task-specific output and applicable component/media terms.

For a complete creator project, invoke `creator-production` and supply the audience, format, duration and assets. Choose one primary renderer, preserve an existing project’s dependency versions, render a short sample, check frames/audio and export metadata, and deliver the editable project with asset credits. Ask for external publication separately when it is not already authorized.
