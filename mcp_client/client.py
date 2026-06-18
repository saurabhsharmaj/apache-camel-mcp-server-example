import asyncio

import asyncio

from config.settings import settings
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

class MCPClient:

    DEFAULT_MCP_URL = "http://localhost:8080/mcp/sse"

    def __init__(self):
        self.url = settings.MCP_URL or self.DEFAULT_MCP_URL

        print("\n====================================")
        print("MCP CLIENT INITIALIZED")
        print("URL:", self.url)
        print("====================================\n")

    async def _list_tools_async(self):

        print(f"Connecting to {self.url}")

        async with sse_client(self.url) as (read_stream, write_stream):

            print("✓ SSE Connected")

            async with ClientSession(
                read_stream,
                write_stream
            ) as session:

                print("✓ Session Created")

                print("Initializing MCP Session...")
                await session.initialize()

                print("✓ Session Initialized")

                print("Fetching tools...")

                result = await session.list_tools()

                print(f"✓ Retrieved {len(result.tools)} tools")

                return result

    async def _call_tool_async(self, tool_name, arguments=None):

        arguments = arguments or {}

        print("\n====================================")
        print("CALLING TOOL")
        print("Tool:", tool_name)
        print("Arguments:", arguments)
        print("====================================\n")

        async with sse_client(self.url) as (read_stream, write_stream):

            print("✓ SSE Connected")

            async with ClientSession(
                read_stream,
                write_stream
            ) as session:

                print("✓ Session Created")

                print("Initializing MCP Session...")
                await session.initialize()

                print("✓ Session Initialized")

                print(f"Executing tool: {tool_name}")

                result = await session.call_tool(
                    tool_name,
                    arguments
                )

                print("\n========== TOOL RESULT ==========")
                print(result)
                print("=================================\n")

                return result

    def list_tools(self):
        return asyncio.run(
            self._list_tools_async()
        )

    def call_tool(self, tool_name, arguments=None):
        return asyncio.run(
            self._call_tool_async(
                tool_name,
                arguments or {}
            )
        )