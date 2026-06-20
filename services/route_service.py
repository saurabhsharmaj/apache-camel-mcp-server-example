import json

from agents.planner_agent import PlannerAgent
from agents.route_generator_agent import RouteGeneratorAgent
from mcp_client.client import MCPClient
import traceback

class RouteService:

    def __init__(self):

        self.planner = PlannerAgent()
        self.generator = RouteGeneratorAgent()
        self.mcp = MCPClient()

    def create_route(self, user_prompt):
        print("create_route############")
        plan = self.planner.analyze(user_prompt)

        source = plan["source"]
        target = plan["target"]

        source_doc = self.select_mcp_tool(user_prompt,source)
        target_doc = self.select_mcp_tool(user_prompt,target)

        result = self.generator.generate(
            user_prompt,
            source_doc,
            target_doc
        )

        return result

    def select_mcp_tool(self, user_prompt, component_name):
        print(f"select_mcp_tool#####user_prompt#######{user_prompt}")
        print(f"select_mcp_tool######component_name######{component_name}")
        # Step 1: fetch all available MCP tools
        available_tools = self.get_available_tools()
        print("Available TOOL: ")
        # --------------------------------------------------- 
        #STEP 2: Select best tool dynamically 
        #--------------------------------------------------- 
        try:
            selected_tool = self.select_tool(component_name, user_prompt, available_tools.tools)
        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc() 
        print("SELECTED TOOL:")
        
        arguments = { "name": component_name }

        component_doc = self.mcp.call_tool( selected_tool, arguments )
        

        if isinstance(component_doc, dict):
            try:
                return json.dumps(component_doc, indent=2)
            except (TypeError, ValueError):
                return str(component_doc)

        return str(component_doc)

        return result
    

    def get_available_tools(self):

        """
        Expected MCP response example:

        [
            {
                "name": "camel_catalog_component_doc",
                "description": "Fetch camel component docs"
            },
            {
                "name": "camel_kamelet_doc",
                "description": "Fetch kamelet docs"
            }
        ]
        """

        tools = self.mcp.list_tools()

        if not tools:
            return []

        return tools
    

    def select_tool(self, component_name, user_prompt, available_tools):

        try:

            print(f"select_tool############")
            print(f"Available Tools Count: {len(available_tools)}")

            component_name = component_name.lower().strip()
            prompt = user_prompt.lower().strip()

            # ---------------------------------------------------
            # PRIORITY 1:
            # Match component name in tool name
            # ---------------------------------------------------

            for tool in available_tools:

               # print(f"->>Tool Object: {tool}")

                # Tool object directly
                tool_name = getattr(tool, "name", "").lower()

                description = getattr(tool, "description", "")

                if description:
                    description = description.lower()
                else:
                    description = ""

                print(f"->>#tool_name: {tool_name}")
                #print(f"->>#description: {description}")

                if component_name in tool_name:
                    #print(f"->>>=Matched by component name: {tool_name}")
                    return tool.name

            # ---------------------------------------------------
            # PRIORITY 2:
            # Match keywords from prompt
            # ---------------------------------------------------

            for tool in available_tools:

                tool_name = getattr(tool, "name", "").lower()

                description = getattr(tool, "description", "")

                if description:
                    description = description.lower()
                else:
                    description = ""

                combined = tool_name + " " + description

                #print(f"-->>>combined: {combined}")

                if "kafka" in prompt and "kafka" in combined:
                    return tool.name

                if "oracle" in prompt and "sql" in combined:
                    return tool.name

                if "mysql" in prompt and "sql" in combined:
                    return tool.name

                if "salesforce" in prompt and "salesforce" in combined:
                    return tool.name

            # ---------------------------------------------------
            # PRIORITY 3:
            # Generic fallback
            # ---------------------------------------------------

            for tool in available_tools:

                tool_name = getattr(tool, "name", "")

                if tool_name == "camel_catalog_component_doc":
                    print("Returning generic fallback tool")
                    return tool_name

            # ---------------------------------------------------
            # FINAL FALLBACK
            # ---------------------------------------------------

            if available_tools:

                fallback_tool = getattr(available_tools[0], "name", None)

                # print(f"Final fallback tool: {fallback_tool}")

                return fallback_tool

            # ---------------------------------------------------
            # NO TOOLS FOUND
            # ---------------------------------------------------

            print("##### No tools available#####")

            return None

        except Exception as e:

            import traceback

            print("Error inside select_tool:", str(e))
            traceback.print_exc()

            return "camel_catalog_component_doc"