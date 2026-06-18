import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession


async def main():
    mcp_url = "http://localhost:8080/mcp/sse"

    print(f"Connecting to {mcp_url}")

    async with sse_client(mcp_url) as (read_stream, write_stream):

        print("SSE connected")

        async with ClientSession(read_stream, write_stream) as session:

            print("Initializing MCP session...")
            await session.initialize()

            print("Fetching tools...")
            result = await session.list_tools()

            print("\n=== TOOLS ===")

            for tool in result.tools:
                print(f"\nName: {tool.name}")
                print(f"Description: {tool.description}")

                if hasattr(tool, "inputSchema"):
                    print("Schema:", tool.inputSchema)

            print("\nTotal tools:", len(result.tools))


if __name__ == "__main__":
    asyncio.run(main())