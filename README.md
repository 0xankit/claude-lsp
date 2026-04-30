# claude-lsp

A single Claude Code plugin that brings real-time LSP code intelligence to any combination of languages. Select which languages you want — Claude Code activates only those servers. Update settings and reload to change at any time.

## Supported languages

| Language key | Server                        | Quick install                                    |
| ------------ | ----------------------------- | ------------------------------------------------ |
| `rust`       | `rust-analyzer`               | `rustup component add rust-analyzer`             |
| `go`         | `gopls`                       | `go install golang.org/x/tools/gopls@latest`     |
| `typescript` | `typescript-language-server`  | `npm i -g typescript-language-server typescript` |
| `python`     | `pylsp`                       | `pip install python-lsp-server`                  |
| `lua`        | `lua-language-server`         | `brew install lua-language-server`               |
| `c-cpp`      | `clangd`                      | `brew install llvm` / `apt install clangd`       |
| `java`       | `jdtls`                       | `brew install jdtls`                             |
| `ruby`       | `solargraph`                  | `gem install solargraph`                         |
| `php`        | `intelephense`                | `npm i -g intelephense`                          |
| `html`       | `vscode-html-language-server` | `npm i -g vscode-langservers-extracted`          |
| `css`        | `vscode-css-language-server`  | `npm i -g vscode-langservers-extracted`          |
| `yaml`       | `yaml-language-server`        | `npm i -g yaml-language-server`                  |

Install the binary for each language you want before enabling it.

---

## Quick start

### 1. Install the binary for each language you need

See the install column above. For example, for Rust and Go:

```shell
rustup component add rust-analyzer
go install golang.org/x/tools/gopls@latest
```

### 2. Register the marketplace

Add `claude-lsp` as a known marketplace in your settings file.

**User-wide** (`~/.claude/settings.json`) — available in every project:

```json
{
  "extraKnownMarketplaces": {
    "claude-lsp": {
      "source": {
        "source": "git",
        "url": "https://github.com/0xankit/claude-lsp.git"
      }
    }
  }
}
```

**Project-scoped** (`.claude/settings.json`) — only for one project:

```json
{
  "extraKnownMarketplaces": {
    "claude-lsp": {
      "source": {
        "source": "git",
        "url": "https://github.com/0xankit/claude-lsp.git"
      }
    }
  }
}
```

### 3. Install the plugin

Inside a Claude Code session:

```shell
/plugin install claude-lsp@claude-lsp
```

Claude Code will prompt you to select which languages to enable. Type the language keys separated by commas, e.g.:

```text
rust, go, typescript
```

### 4. Reload

```shell
/reload-plugins
```

LSP servers for your selected languages are now active.

---

## Configuring languages

Language selection is stored in the `pluginConfigs` section of whichever settings file you choose. You can edit it directly at any time — no reinstall needed.

**User-wide** (`~/.claude/settings.json`) — same languages across all your projects:

```json
{
  "pluginConfigs": {
    "claude-lsp": {
      "options": {
        "languages": ["rust", "go", "typescript"]
      }
    }
  }
}
```

**Project-scoped** (`.claude/settings.json`) — different languages per project:

```json
{
  "pluginConfigs": {
    "claude-lsp": {
      "options": {
        "languages": ["python", "yaml"]
      }
    }
  }
}
```

After editing, run `/reload-plugins` in Claude Code and the change takes effect immediately. The `ConfigChange` hook will also remind you when it detects a settings file has changed.

---

## How it works

```text
plugins/claude-lsp/
├── .claude-plugin/plugin.json   ← manifest + userConfig (language selection)
├── .lsp.json                    ← all 12 language entries, each via lsp-proxy
├── bin/lsp-proxy                ← checks CLAUDE_PLUGIN_OPTION_LANGUAGES at startup
├── scripts/null-lsp.py          ← minimal LSP for disabled languages (no errors)
└── hooks/hooks.json             ← ConfigChange hook: reminds you to /reload-plugins
```

Every language entry in `.lsp.json` launches `bin/lsp-proxy`. The proxy reads the `CLAUDE_PLUGIN_OPTION_LANGUAGES` environment variable (exported automatically by Claude Code from your `pluginConfigs`):

- **Enabled language** — proxy transparently `exec`s the real binary (e.g. `rust-analyzer`)
- **Disabled language** — proxy runs a minimal null LSP that responds to `initialize` with empty capabilities, so Claude Code starts cleanly without error messages

---

## Requirements

- Claude Code CLI, desktop app, or IDE extension
- `python3` on `$PATH` (used by the null LSP for disabled languages — ships with macOS and most Linux distros)
- LSP server binary installed for each language you enable (see [Supported languages](#supported-languages))

---

## Adding a new language

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT
