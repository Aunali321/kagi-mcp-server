# Kagi MCP Server

An MCP (Model Context Protocol) server that provides Kagi search capabilities to AI assistants.

## Features

- **Authentication**: Save Kagi session cookies for persistent access
- **Search**: Perform Kagi searches and retrieve structured results (title, URL, snippet)

## Installation

1. Clone the repository and sync dependencies:

```bash
uv sync
```

2. Install Playwright Chromium browser:

```bash
uv run playwright install chromium
```

## MCP Configuration

Add the following to your MCP client configuration:

```json
{
  "Kagi Search": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "fastmcp",
      "fastmcp",
      "run",
      "/path/to/kagi-mcp-server/main.py"
    ]
  }
}
```

Replace `/path/to/kagi-mcp-server` with the actual path to this directory.

## Usage

### 1. Get Your Kagi Token

**Option A: Developer Console**

1. Log into your Kagi account at https://kagi.com
2. Open Developer Tools (F12 or Cmd+Option+I)
3. Go to **Application** > **Cookies** > `https://kagi.com`
4. Find the `kagi_session` cookie and copy its value


**Option B: Session Link**

1. Log into your Kagi account at https://kagi.com
2. Navigate to **Settings** > **Advanced** > **Session Link**
3. Copy the token from the generated URL (the part after `?token=`)

### 2. Authenticate

Provide your token to the LLM and ask it to authenticate with Kagi. The LLM will call the `authenticate` tool to save your session cookies locally.

Example prompt:
> "Authenticate with Kagi using this token: `your_token_here`"

### 3. Search

Once authenticated, simply ask the LLM to search using Kagi:

> "Search Kagi for latest AI news"

Returns a list of results with:
- `rank`: Result position
- `title`: Page title
- `url`: Page URL
- `snippet`: Description snippet

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) package manager
- Kagi account with active subscription

## License

MIT
