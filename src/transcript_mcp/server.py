from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

from transcript_mcp.transcript import Factory
from transcript_mcp.transcript.entities import Transcript

server = FastMCP(name="transcript-mcp", host="0.0.0.0", port=8000)


@server.tool()
def get_transcript(url: Annotated[str, Field(description="URL of a video")]) -> Transcript:
    """This tool is responsible for downloading transcript of a video. Provide video URL and this tool will try to
    fetch transcript if it supports respective provider. Below are supported transcript providers:
        - Youtube
    """
    transcript_provider_manager = Factory.create_transcript_provider_manager()
    return transcript_provider_manager.get_transcript(url)


if __name__ == "__main__":
    server.run(transport="streamable-http")