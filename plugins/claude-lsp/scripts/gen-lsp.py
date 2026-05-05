#!/usr/bin/env python3
"""
Generate .lsp.json from lsp-servers.json template.

Reads enabled languages from Claude Code settings files, filters the template
to only those languages, and resolves ${CLAUDE_PLUGIN_ROOT} to the actual path.
Called by SessionStart and ConfigChange hooks.
"""
import json
import os
import sys

"""
${CLAUDE_PLUGIN_ROOT} is the absolute path for plugin installation directory .
"""
PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
"""
${CLAUDE_PROJECT_DIR} is the project root. Wrap in quotes to handle paths with 
spaces. It can be used to configure files from project in .claude directory.
"""
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", "")
"""
${CLAUDE_PLUGIN_DATA} is a persistent directory for plugin state that survives 
updates. Use this for installed dependencies such as node_modules or Python 
virtual environments, generated code, caches, and any other files that should 
persist across plugin versions. The directory is created automatically the first 
time this variable is referenced. The data directory is deleted automatically 
when you uninstall the plugin from the last scope where it is installed.
# https://code.claude.com/docs/en/plugins-reference#persistent-data-directory
"""
PLUGIN_DATA = os.environ.get("CLAUDE_PLUGIN_DATA","")


def find_install_paths():
    """Return all installPath values for claude-lsp from installed_plugins.json."""
    registry = os.path.expanduser("~/.claude/plugins/installed_plugins.json")
    try:
        with open(registry) as f:
            data = json.load(f)
        entries = data.get("plugins", {}).get("claude-lsp@claude-lsp", [])
        return [e["installPath"] for e in entries if "installPath" in e]
    except Exception:
        return []


def read_enabled_languages():
    candidates = [
        os.path.join(PROJECT_DIR, ".claude", "settings.json"),
        os.path.join(PROJECT_DIR, ".claude", "settings.local.json"),
        os.path.expanduser("~/.claude/settings.json"),
        os.path.expanduser("~/.claude/settings.local.json"),
    ]
    for path in candidates:
        try:
            with open(path) as f:
                d = json.load(f)
            langs = (
                d.get("pluginConfigs", {})
                .get("claude-lsp", {})
                .get("options", {})
                .get("languages", [])
            )
            if langs:
                return langs
        except Exception:
            pass
    return []


def main():
    if not PLUGIN_ROOT:
        print("[claude-lsp] gen-lsp: CLAUDE_PLUGIN_ROOT not set", file=sys.stderr)
        sys.exit(1)

    template_path = os.path.join(PLUGIN_ROOT, "lsp-servers.json")

    try:
        with open(template_path) as f:
            template = json.load(f)
    except Exception as e:
        print(f"[claude-lsp] gen-lsp: cannot read template: {e}", file=sys.stderr)
        sys.exit(1)

    enabled = read_enabled_languages()

    # If no languages configured, generate empty file (no servers)
    filtered = {k: v for k, v in template.items() if k in enabled} if enabled else {}

    # Resolve template variables. ${CLAUDE_PLUGIN_ROOT} always points to PLUGIN_ROOT
    # because that's where the actual plugin files (lsp-proxy, etc.) live.
    plugin_data = PLUGIN_DATA or os.path.join(PLUGIN_ROOT, "data")
    resolved = (
        json.dumps(filtered, indent=2)
        .replace("${CLAUDE_PLUGIN_ROOT}", PLUGIN_ROOT)
        .replace("${CLAUDE_PLUGIN_DATA}", plugin_data)
    )

    # Write .lsp.json to PLUGIN_ROOT and every registered install path so
    # Claude Code finds it regardless of which directory it uses as the plugin root.
    for out_dir in {PLUGIN_ROOT} | set(find_install_paths()):
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, ".lsp.json"), "w") as f:
            f.write(resolved)

    langs = ", ".join(filtered.keys()) if filtered else "none"
    print(f"[claude-lsp] LSP config generated for: {langs}")
    print(f"[claude-lsp] Run /reload-plugins to activate.")


if __name__ == "__main__":
    main()
