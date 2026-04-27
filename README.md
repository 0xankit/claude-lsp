# claude-lsp

A Claude Code plugin that provides ready-to-use LSP (Language Server Protocol) configuration templates. Each language is a standalone plugin — install only what your project needs.

## Supported languages

| Language      | Server                        | Install                                          |
| ------------- | ----------------------------- | ------------------------------------------------ |
| Rust          | `rust-analyzer`               | `rustup component add rust-analyzer`             |
| Go            | `gopls`                       | `go install golang.org/x/tools/gopls@latest`     |
| TypeScript/JS | `typescript-language-server`  | `npm i -g typescript-language-server typescript` |
| Python        | `pylsp`                       | `pip install python-lsp-server`                  |
| Lua           | `lua-language-server`         | `brew install lua-language-server`               |
| C / C++       | `clangd`                      | `brew install llvm` / `apt install clangd`       |
| Java          | `jdtls`                       | `brew install jdtls`                             |
| Ruby          | `solargraph`                  | `gem install solargraph`                         |
| PHP           | `intelephense`                | `npm i -g intelephense`                          |
| HTML          | `vscode-html-language-server` | `npm i -g vscode-langservers-extracted`          |
| CSS / SCSS    | `vscode-css-language-server`  | `npm i -g vscode-langservers-extracted`          |
| YAML          | `yaml-language-server`        | `npm i -g yaml-language-server`                  |

---

## Quick start

### 1. Register the marketplace

Add `claude-lsp` as a known marketplace in `~/.claude/settings.json` (user-wide) or `.claude/settings.json` (project-scoped):

```json
{
  "extraKnownMarketplaces": {
    "claude-lsp": {
      "source": {
        "git": "https://github.com/0xankit/claude-lsp"
      }
    }
  }
}
```

### 2. Install a language plugin

Inside a Claude Code session, install whichever languages your project needs:

```shell
/plugin install lsp/rust-analyzer@claude-lsp
/plugin install lsp/gopls@claude-lsp
/plugin install lsp/typescript-language-server@claude-lsp
```

That's it — Claude Code picks up the LSP config automatically on the next session start.

> **Tip:** Put the `extraKnownMarketplaces` entry in `~/.claude/settings.json` to make the marketplace available in every project, or in `.claude/settings.json` at your project root to scope it to one project.

---

## How it works

Each `lsp/<server>/` directory contains two files:

```text
lsp/rust-analyzer/
├── plugin.json    ← server metadata and install instructions
└── .lsp.json      ← ready-to-use Claude Code LSP config template
```

Install the plugin for a language and Claude Code picks up its `.lsp.json` automatically on the next session start.

---

## Manual template use

You don't have to use the plugin system. Each `lsp/<server>/.lsp.json` is a self-contained config block you can copy directly.

For example, to add Go support manually, copy from [lsp/gopls/.lsp.json](lsp/gopls/.lsp.json):

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    },
    "transport": "stdio",
    "settings": {
      "gopls": {
        "staticcheck": true,
        "gofumpt": true
      }
    },
    "startupTimeout": 20000,
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

Paste it into your project's `.claude/.lsp.json`, merging with any existing entries.

---

## `.lsp.json` field reference

| Field                   | Required | Type    | Description                                   |
| ----------------------- | -------- | ------- | --------------------------------------------- |
| `command`               | yes      | string  | LSP server binary                             |
| `extensionToLanguage`   | yes      | object  | Maps `".ext"` → `"language-id"`               |
| `args`                  | no       | array   | CLI arguments for the server                  |
| `transport`             | no       | string  | `"stdio"` (default) or `"socket"`             |
| `env`                   | no       | object  | Extra environment variables                   |
| `initializationOptions` | no       | object  | Passed to server at initialization            |
| `settings`              | no       | object  | Passed via `workspace/didChangeConfiguration` |
| `startupTimeout`        | no       | number  | ms to wait for server start                   |
| `shutdownTimeout`       | no       | number  | ms to wait for graceful shutdown              |
| `restartOnCrash`        | no       | boolean | Auto-restart on crash                         |
| `maxRestarts`           | no       | number  | Max restart attempts before giving up         |

---

## Directory structure

```text
claude-lsp/
├── .claude-plugin/
│   ├── plugin.json                      — Plugin manifest
│   └── marketplace.json                 — Per-language plugin registry
├── lsp/
│   ├── rust-analyzer/
│   │   ├── plugin.json                  — Server metadata and install commands
│   │   └── .lsp.json                    — Config template
│   ├── gopls/
│   │   ├── plugin.json
│   │   └── .lsp.json
│   ├── typescript-language-server/
│   ├── pylsp/
│   ├── lua-language-server/
│   ├── clangd/
│   ├── jdtls/
│   ├── solargraph/
│   ├── intelephense/
│   ├── vscode-html-language-server/
│   ├── vscode-css-language-server/
│   └── yaml-language-server/
├── .lsp.json                            — Plugin-level LSP config (empty by default)
├── settings.json                        — Plugin defaults
├── README.md
└── CONTRIBUTING.md                      — How to add a new language
```

---

## Requirements

- Claude Code CLI, desktop app, or IDE extension
- LSP server binaries installed separately (see install commands in each `lsp/*/plugin.json`)

---

## Adding a new language

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: add `lsp/<server-name>/plugin.json` and `lsp/<server-name>/.lsp.json`. No other changes required.

---

## License

MIT
