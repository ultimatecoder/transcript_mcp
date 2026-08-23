from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

server = FastMCP(name="yt_mcp", host="0.0.0.0", port=8000)


@server.tool()
def add(
        a: Annotated[int, Field(description="First addend")],
        b: Annotated[int, Field(description="Second addend")]
) -> int:
    """Add two integers and return their sum"""
    return a + b


if __name__ == "__main__":
    server.run(transport="streamable-http")