# Contributing to claude-lsp

## Adding a new language

Adding a new language is **two files only** — no script changes required.

### 1. Create the server directory

```bash
mkdir lsp/<server-binary-name>
```

Use the binary name as the directory name (e.g., `lsp/elixir-ls/`).

### 2. Create `plugin.json`

Follow the schema from any existing `plugin.json`, e.g. [lsp/gopls/plugin.json](lsp/gopls/plugin.json):

```json
{
  "name": "elixir-ls",
  "language": "elixir",
  "displayName": "Elixir",
  "description": "One sentence about the language server.",
  "binary": "elixir-ls",
  "extensions": [".ex", ".exs"],
  "install": {
    "mix (recommended)": "mix escript.install hex elixir_ls",
    "brew": "brew install elixir-ls"
  },
  "homepage": "https://github.com/elixir-lsp/elixir-ls",
  "repository": "https://github.com/elixir-lsp/elixir-ls",
  "license": "Apache-2.0",
  "keywords": ["elixir", "lsp", "language-server"]
}
```

**Required fields:** `name`, `language`, `displayName`, `binary`, `extensions`, `install` (at least one entry).

**Optional fields:**

| Field          | Purpose                                              |
| -------------- | ---------------------------------------------------- |
| `alternatives` | Alternative servers for this language                |
| `note`         | Important caveat shown to users (e.g., licence info) |

### 3. Create `.lsp.json`

This is the config block that gets written into the user's `.claude/.lsp.json`. The key is the language name (matches `language` in `plugin.json`).

Follow the schema from any existing `.lsp.json`, e.g. [lsp/gopls/.lsp.json](lsp/gopls/.lsp.json):

```json
{
  "elixir": {
    "command": "elixir-ls",
    "args": [],
    "extensionToLanguage": {
      ".ex": "elixir",
      ".exs": "elixir"
    },
    "transport": "stdio",
    "initializationOptions": {},
    "settings": {},
    "startupTimeout": 20000,
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

**Notes on `settings`:** put only server-specific defaults that improve the out-of-box experience. Avoid noisy or opinionated settings — users can override in their own `.lsp.json`.

### 4. Test locally

With the plugin cloned, run:

```bash
TODO
```

### 5. Open a pull request

Title: `feat(languages): add <Language> (<server-binary>)`

Include in the description:

- Install commands you tested and your OS
- Any platform-specific notes
- Whether you have an alternative server worth documenting in `alternatives`

---

## Modifying setup.sh or check-lsp.sh

Scripts live in `scripts/`. They read all `lsp/*/plugin.json` and `lsp/*/.lsp.json` files dynamically, so adding a new language directory is automatically picked up without changing the scripts.

When modifying scripts:

- Keep them POSIX-compatible bash (not fish, zsh, etc.)
- `jq` is the only external dependency — do not add others
- Test on macOS and Linux

---

## Schema summary

### `lsp/<server>/plugin.json`

```text
name            string   required — binary name (matches directory name)
language        string   required — language key used in .lsp.json
displayName     string   required — human-readable name shown in setup menu
description     string   required — one sentence about the server
binary          string   required — exact binary name to look up with `which`
extensions      array    required — file extensions this server handles
install         object   required — { "method label": "shell command" }
alternatives    object   optional — other servers for the same language
note            string   optional — caveats displayed to users
homepage        string   optional
repository      string   optional
license         string   optional
keywords        array    optional
```

### `lsp/<server>/.lsp.json`

Top-level key is the language name (value of `language` in `plugin.json`). Value is a Claude Code LSP server config object — see the [field reference in README.md](README.md#lspjson-field-reference).
