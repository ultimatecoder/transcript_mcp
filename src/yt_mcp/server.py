from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

from yt_mcp.transcript.entities import Transcript, TranscriptMetadata, TranscriptLanguage, TranscriptLineItem

server = FastMCP(name="yt_mcp", host="0.0.0.0", port=8000)


@server.tool()
def add(
        a: Annotated[int, Field(description="First addend")],
        b: Annotated[int, Field(description="Second addend")]
) -> int:
    """Add two integers and return their sum"""
    return a + b

@server.tool()
def get_transcript(url: Annotated[str, Field(description="URL of a video")]) -> Transcript:
    """This tool is responsible for downloading transcript of a video from its urls. Below are supported services:
        - Youtube
    """
    return Transcript(
        metadata=TranscriptMetadata(language=TranscriptLanguage.English, video_id="video123"),
        transcripts=[
            TranscriptLineItem(start_time=0.1, text="This is first line"),
            TranscriptLineItem(start_time=0.2, text="This is second line"),
            TranscriptLineItem(start_time=0.3, text="This is third line"),
        ]
    )


if __name__ == "__main__":
    server.run(transport="streamable-http")