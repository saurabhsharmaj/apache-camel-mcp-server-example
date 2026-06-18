from llm.groq_client import GroqClient


class RouteGeneratorAgent:

    def __init__(self):
        self.llm = GroqClient()

    def generate(
            self,
            business_requirement,
            source_docs,
            target_docs):

        prompt = f"""
You are a Senior Apache Camel Architect.

Business Requirement:
{business_requirement}

Source Documentation:
{source_docs}

Target Documentation:
{target_docs}

Generate:

1. Camel YAML DSL
2. Oracle Insert Logic
3. Required Dependencies
4. Architecture Notes
"""

        return self.llm.chat(prompt)