# test_mcp.py

import asyncio

from mcp.client.sse import sse_client
from mcp import ClientSession


async def main():

    async with sse_client(
        "http://localhost:8080/mcp/sse"
    ) as streams:

        read_stream, write_stream = streams

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("\nTOOLS\n")

            for tool in tools.tools:
                print(tool.name)


asyncio.run(main())