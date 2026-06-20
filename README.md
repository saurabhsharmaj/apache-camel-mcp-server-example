'''
mkdir camel-ai-platform
cd camel-ai-platform

type nul > README.md
type nul > requirements.txt
type nul > .env

mkdir config agents mcp llm llm\prompts services models api ui reports

type nul > config\settings.py
type nul > config\logging_config.py

type nul > agents\planner_agent.py
type nul > agents\route_generator_agent.py
type nul > agents\validation_agent.py
type nul > agents\security_agent.py

type nul > mcp\client.py
type nul > mcp\tool_registry.py
type nul > mcp\tool_executor.py

type nul > llm\groq_client.py
type nul > llm\prompts\planner.txt
type nul > llm\prompts\route_generation.txt
type nul > llm\prompts\security_review.txt

type nul > services\route_service.py
type nul > services\validation_service.py
type nul > services\dependency_service.py
type nul > services\security_service.py

type nul > models\request.py
type nul > models\route.py
type nul > models\validation.py
type nul > models\dependency.py

type nul > api\main.py

type nul > ui\streamlit_app.py

type nul > reports\report_generator.py

type nul > agents\__init__.py
type nul > config\__init__.py
type nul > llm\__init__.py
type nul > mcp\__init__.py
type nul > models\__init__.py
type nul > reports\__init__.py
type nul > services\__init__.py
type nul > ui\__init__.py
type nul > api\__init__.py
type nul > .env
'''


jbang -Dquarkus.http.host-enabled=true -Dquarkus.http.port=8080  org.apache.camel:camel-jbang-mcp:LATEST:runner


streamlit run ui/streamlit_app.py

Create a Camel route from Salesforce to Oracle

-----

python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

----
.env
GROQ_API_KEY=gsk_xxxx
MCP_URL=http://localhost:8080/mcp/sse
---

python test_mcp.py
streamlit run ui\streamlit_app.py
http://localhost:8501

Create a Camel route from Salesforce to Oracle

