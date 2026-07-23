# app.py
# Streamlit web interface for the research assistant

import streamlit as st
import time
from graph import research_assistant

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Title
st.title("Multi-Agent Research Assistant")
st.markdown("""
*An AI-powered research assistant that uses multiple agents to research any topic*
""")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown("""
This research assistant uses 4 AI agents:
1. **Planner** - Creates research plan
2. **Researcher** - Gathers information
3. **Verifier** - Checks completeness
4. **Summarizer** - Writes final report

**Features:**
- Web search
- Document retrieval (RAG)
- Self-correction loop
- Professional reports
""")

# Main interface
st.header("Enter your research topic")

# Input
topic = st.text_input(
    "Research Topic",
    placeholder="Example: Artificial General Intelligence"
)

# Research button
if st.button("Start Research", type="primary"):
    if not topic:
        st.error("Please enter a research topic")
    else:
        # Create placeholder for results
        status_placeholder = st.empty()
        result_placeholder = st.empty()

        try:
            # Show status
            status_placeholder.info("Starting research...")

            # Run research
            with st.spinner("Research in progress..."):
                result = research_assistant.research(topic)

            # Display results
            status_placeholder.success("Research Complete!")

            # Show metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sections Researched", len(result["plan"]))
            with col2:
                st.metric("Iterations", result["iterations"])
            with col3:
                status = "Verified" if result["is_verified"] else "Partial"
                st.metric("Status", status)

            # Show plan
            with st.expander("Research Plan"):
                for i, section in enumerate(result["plan"], 1):
                    st.write(f"{i}. {section}")

            # Show report
            st.markdown("---")
            st.header("Research Report")
            st.markdown(result["report"])

            # Download options
            st.download_button(
                label="Download Report",
                data=result["report"],
                file_name=f"{topic.replace(' ', '_')}_report.txt",
                mime="text/plain"
            )

        except Exception as e:
            status_placeholder.error(f"Error: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "*Powered by LangGraph, Multi-Agent Systems, and RAG*"
)