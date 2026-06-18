import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from services.route_service import RouteService

st.set_page_config(
    page_title="Camel AI Platform",
    layout="wide"
)

st.title("Enterprise Camel AI Platform")

user_prompt = st.text_area(
    "Business Requirement",
    value="Create a Camel route from Salesforce to Oracle"
)

if st.button("Generate"):

    service = RouteService()

    with st.spinner("Generating route..."):

        try:
            result = service.create_route(
                user_prompt
            )
            st.success("Generated Successfully")
            st.markdown(result)
        except Exception as e:
            st.error(f"Error generating route: {str(e)}")