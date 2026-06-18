import json
import re

from llm.groq_client import GroqClient


class PlannerAgent:

    def __init__(self):
        self.llm = GroqClient()

    def analyze(self, user_prompt):

        prompt = f"""
                You are an integration architect.

                Extract source and target systems.

                User Request:
                {user_prompt}

                Return ONLY JSON.

                Example:

                {{
                "source": "salesforce",
                "target": "oracle"
                }}

                No markdown.
                No explanation.
                No code fences.
                JSON only.
                """

        response = self.llm.chat(prompt)

        print("\n==== GROQ RESPONSE ====")
        print(response)
        print("=======================\n")

        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        try:
            return json.loads(response)

        except Exception:

            source_match = re.search(
                r'"source"\s*:\s*"([^"]+)"',
                response
            )

            target_match = re.search(
                r'"target"\s*:\s*"([^"]+)"',
                response
            )

            if source_match and target_match:
                return {
                    "source": source_match.group(1),
                    "target": target_match.group(1)
                }

            raise Exception(
                f"Unable to parse planner response:\n{response}"
            )