import streamlit as st
import os
from datetime import date 

from langchain_core.messages import AIMessage, HumanMessage
from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config() # config
        self.user_controls = {}

    def initialize_session(self):
        return {
            "current_step": "requirements",
            "requirements": "",
            "user_stories": "",
            "po_feedback": "",
            "generated_code": "",
            "review_feedback": "",
            "decision": None
        }

    def load_streamlit_ui(self):
        
        # set page config
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClick = False
        st.session_state.IsSDLC = False 


        # Sidebar content
        with st.sidebar:
            st.header("Configuration")

            # LLM selection
            llm_options = self.config.get_llm_options()
            selected_llm = st.selectbox("Select LLM", llm_options)
            self.user_controls["selected_llm"] = selected_llm

            if self.user_controls["selected_llm"] == 'Groq':
                
                # Model selection
                groq_model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", groq_model_options)

                # API key input
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")

                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your GROQ API key to proceed. Don't have? refer: https://console.groq.com/keys")

            # Use case selection
            usecase_options = self.config.get_usecase_options()
            selected_usecase = st.selectbox("Select Use Case", usecase_options)
            self.user_controls["selected_usecase"] = selected_usecase

            if self.user_controls["selected_usecase"] == "Chatbot with Tools":
                # APIKey input
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY_API_KEY", type="password")

                # Validate API Key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY to proceed. Don't have?, refer: https://app.tavily.com/home")

            if "state" not in st.session_state:
                st.session_state.state = self.initialize_session()


        return self.user_controls


