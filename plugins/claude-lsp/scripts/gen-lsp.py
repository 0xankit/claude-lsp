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

PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", "")


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
    output_path = os.path.join(PLUGIN_ROOT, ".lsp.json")

    try:
        with open(template_path) as f:
            template = json.load(f)
    except Exception as e:
        print(f"[claude-lsp] gen-lsp: cannot read template: {e}", file=sys.stderr)
        sys.exit(1)

    enabled = read_enabled_languages()

    # If no languages configured, generate empty file (no servers)
    filtered = {k: v for k, v in template.items() if k in enabled} if enabled else {}

    # Resolve ${CLAUDE_PLUGIN_ROOT} to the actual absolute path
    text = json.dumps(filtered, indent=2)
    text = text.replace("${CLAUDE_PLUGIN_ROOT}", PLUGIN_ROOT)
    # Also resolve ${CLAUDE_PLUGIN_DATA} for intelephense storage path
    plugin_data = os.environ.get("CLAUDE_PLUGIN_DATA", os.path.join(PLUGIN_ROOT, "data"))
    text = text.replace("${CLAUDE_PLUGIN_DATA}", plugin_data)

    with open(output_path, "w") as f:
        f.write(text)

    langs = ", ".join(filtered.keys()) if filtered else "none"
    print(f"[claude-lsp] LSP config generated for: {langs}")
    print(f"[claude-lsp] Run /reload-plugins to activate.")


if __name__ == "__main__":
    main()
