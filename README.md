# transcript-mcp

MCP server that downloads video transcripts. Supports YouTube.

## Architecture

![Request and response flow: an LLM client such as Claude or Codex calls get_transcript(url) on Transcript MCP over Streamable HTTP, which fetches captions from YouTube via youtube-transcript-api and returns the transcript as JSON](docs/architecture.svg)

The editable source is [`docs/architecture.excalidraw`](docs/architecture.excalidraw). Open it at [excalidraw.com](https://excalidraw.com), then re-export `docs/architecture.svg` after changes so the two stay in sync.

## Low-level design

Class diagrams of the `transcript` package, showing public members only. Click a diagram to open it at full size.

### Request flow

How a `get_transcript` call travels from the MCP server through the `transcript` package to the YouTube Transcript API.

![Class diagram: the MCP server asks Factory for a TranscriptProviderManager, which selects a TranscriptProvider. YtTranscriptApiBasedProvider extracts the video ID through YtURLAttributeExtractorCoordinator and fetches captions with YouTubeTranscriptApi](docs/uml/request-flow.svg)

### Domain model

How the library's response objects are translated into the package's own domain entities by the mappers.

![Class diagram in three lanes: external entities from youtube_transcript_api on the left, mappers in the middle, and domain entities on the right. FetchedTranscript and FetchedTranscriptSnippet are inputs to the mappers, which output Transcript, TranscriptMetadata, TranscriptLineItem, and Language](docs/uml/domain-model.svg)

### Error model

Where each error starts and what the caller receives. Library errors are translated by `YtTranscriptApiBasedProvider`; the package's own errors are grouped by whether they are retriable.

![Error translation diagram: youtube_transcript_api errors and checks inside the transcript package on the left map to the errors a caller receives on the right, grouped into RetriableError and NonRetriableError, plus DataError and the built-in ValueError](docs/uml/error-model.svg)

The PlantUML sources are in [`docs/uml/`](docs/uml/). After editing a `.puml` file, re-render its `.svg` with PlantUML so the two stay in sync.
