import json

from agents.planner_agent import PlannerAgent
from agents.route_generator_agent import RouteGeneratorAgent
from mcp_client.client import MCPClient


class RouteService:

    def __init__(self):

        self.planner = PlannerAgent()
        self.generator = RouteGeneratorAgent()
        self.mcp = MCPClient()

    def create_route(self, user_prompt):

        plan = self.planner.analyze(user_prompt)

        source = plan["source"]
        target = plan["target"]

        source_doc = self.get_component_documentation(source)
        target_doc = self.get_component_documentation(
            "sql" if target.lower() == "oracle" else target
        )

        result = self.generator.generate(
            user_prompt,
            source_doc,
            target_doc
        )

        return result

    def get_component_documentation(self, component_name):
        component_doc = self.mcp.call_tool(
            "camel_catalog_component_doc",
            {
                "name": component_name
            }
        )

        if isinstance(component_doc, dict):
            try:
                return json.dumps(component_doc, indent=2)
            except (TypeError, ValueError):
                return str(component_doc)

        return str(component_doc)

        return result