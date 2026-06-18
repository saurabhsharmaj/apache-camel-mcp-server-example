@echo off

wt ^
new-tab --title "Camel MCP" cmd /k "jbang -Dquarkus.http.host-enabled=true -Dquarkus.http.port=8080 org.apache.camel:camel-jbang-mcp:LATEST:runner" ^
; new-tab --title "MCP Inspector" cmd /k "npx @modelcontextprotocol/inspector"