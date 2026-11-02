# Install Atlas Skill Studio

## Choose the surface first

| Surface | Supported path | What is actually installed |
|---|---|---|
| Antigravity **Desktop / App** | `python atlas.py install antigravity` | Three native plugin directories under `~/.gemini/config/plugins/`; reopen Customizations > Installed after restarting |
| Antigravity CLI | `agy plugin install <built-native-plugin-directory>` | A native plugin; CLI installation is not required for the Desktop folder-based path |
| Claude Code | `python atlas.py install claude` | A local `atlas-studio` marketplace and selected plugins through the official Claude CLI |
| Claude Desktop / Chat / Cowork | Build; upload the `*-claude-1.3.0.zip` files | Custom plugins through Claude’s account interface; availability depends on plan/admin controls |
| Codex | `python atlas.py install codex` | A local marketplace and selected plugins through the official Codex CLI |

The public repository is a **source assembler**, not a prebuilt marketplace. Running `claude plugin marketplace add bangaji313/atlas-skill-studio` or installing this repo URL directly with another marketplace client will not assemble its dependencies. Run the documented Python installer first.

## Prerequisites and quick start

Install Python 3.10+ and Git, and make them available in your terminal. For CLI destinations, the corresponding `claude` or `codex` command must also be available and configured for your account.

```sh
git clone https://github.com/bangaji313/atlas-skill-studio.git
cd atlas-skill-studio
python atlas.py list
python atlas.py install antigravity
```

Replace `antigravity` with `claude` or `codex`. To install only one studio, append `--studio growth`, `--studio creative` or `--studio engineering`. There is no npm install or `npx` prerequisite for the assembler. Production tools such as Remotion or Hypit may independently use Node/npm when you set them up later.

## Claude Desktop without CLI installation

1. Run `python atlas.py build` once. The JSON receipt prints the successful build directory.
2. In that directory, select each `atlas-*-claude-1.3.0.zip` file.
3. In Claude Desktop, open Customize > Plugins (or the consolidated Plugins page, depending on rollout), and use the custom-plugin upload option. In Cowork, open its tab first if needed.
4. Inspect the skills before enabling the plugins. Start a new conversation and name a studio and a concrete task.

If custom-plugin upload is unavailable, check your plan, admin permissions and Claude’s current documentation. Do not rename the archive to `.mcpb`: a local MCP desktop extension is a different package type. A chat response that says it read a repository is not proof of installation.

## What the build does

The assembler reads `catalog/atlas.lock.json`, obtains only the selected source files using Git partial/sparse checkout, verifies upstream SHA-256 values, applies recorded text adaptations, verifies the resulting bytes, and constructs the native packages. A developer can provide previously verified pinned ZIPs using `--cache-dir PATH`; ordinary installation uses Git. The initial source fetch needs internet access; repeated builds reuse the local cache.

Builds are created under a fresh `dist/atlas-build-*` directory. The assembler does not delete an older build, overwrite an existing Antigravity plugin, execute upstream scripts, install renderer dependencies, call paid APIs, register MCP servers or import session hooks. Keep a successful build and the repository in a stable folder because local CLI marketplaces refer to it.

## Verify

Antigravity Desktop: open **Customizations > Installed**, inspect each studio, and verify the skill list. CLI clients can also run `agy plugin list --json`, `claude plugin list`, or `codex plugin list --json`. Expected top-level skill counts are Growth **79**, Creative **79**, Engineering **69**. Merely counting Markdown files is insufficient: nested reference guides are not extra skills.

Try a small task, for example “Use Atlas Creative Production: scriptwriting to draft a 20-second voice-over from this brief.” Check the selected skill and actual result before attempting a complete production.

## Update and recovery

Pull this repository, inspect `CHANGELOG.md` and changes to the source lock, then build again. Before updating Antigravity, uninstall the selected Atlas package in its UI or move your existing plugin to a backup location you control; the installer intentionally refuses to overwrite it. Then reinstall. For CLI hosts, update/remove the old `atlas-studio` marketplace registration using that host’s plugin manager before registering the new successful build. Native ChatGPT account plugins are a separate installation channel; avoid enabling duplicate copies in Codex.

The build receipt, lockfile and pinned upstream commit links identify exactly what was assembled. Cache checksums that fail must be investigated; do not disable verification. A changed dependency is an update, not a reason to force an old checksum to pass.

## Official references, checked 2 November 2026

- [Antigravity plugins, including the App/Desktop](https://antigravity.google/docs/plugins)
- [Antigravity agent skills](https://antigravity.google/docs/skills)
- [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Claude plugin manifests](https://code.claude.com/docs/en/plugins-reference)
- [Claude local marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

Host packaging can be validated locally; successful upload, recognition and rendering in each Desktop account must be checked separately. See VERIFICATION.md for the tested scope of this release.
