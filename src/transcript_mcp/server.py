from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

from transcript_mcp.transcript import Factory
from transcript_mcp.transcript.entities import Transcript

server = FastMCP(name="transcript-mcp", host="0.0.0.0", port=8000)


@server.tool()
def get_transcript(url: Annotated[str, Field(description="URL of a video")]) -> Transcript:
    """This tool is responsible for downloading transcript of a video from its urls. Below are supported services:
        - Youtube
    """
    transcript_provider_manager = Factory.create_transcript_provider_manager()
    return transcript_provider_manager.get_transcript(url)
    #return Transcript(
    #    metadata=TranscriptMetadata(language=TranscriptLanguage.English, video_id="video123"),
    #    transcripts=[
    #        TranscriptLineItem(start_time=0.1, text="This is first line"),
    #        TranscriptLineItem(start_time=0.2, text="This is second line"),
    #        TranscriptLineItem(start_time=0.3, text="This is third line"),
    #    ]
    #)


if __name__ == "__main__":
    server.run(transport="streamable-http")