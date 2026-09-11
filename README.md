# transcript-mcp

MCP server that downloads video transcripts. Supports YouTube.

## Architecture

![Request and response flow: an LLM client such as Claude or Codex calls get_transcript(url) on Transcript MCP over Streamable HTTP, which fetches captions from YouTube via youtube-transcript-api and returns the transcript as JSON](docs/architecture.svg)

The editable source is [`docs/architecture.excalidraw`](docs/architecture.excalidraw). Open it at [excalidraw.com](https://excalidraw.com), then re-export `docs/architecture.svg` after changes so the two stay in sync.
