# common_utils.py
import os
import streamlit as st


def get_openai_api_key():
    """
    Get the OpenAI API key from the user and set it as an environment variable.
    Returns True if the API key is provided, False otherwise.
    """
    api_key = st.text_input("Enter your OpenAI API key:",
                            type="password", key="openai_api_key")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        return True
    return False


def display_markdown_content(content: str, title: str = "Generated Content"):
    """
    Display markdown content in Streamlit with a title.
    """
    st.markdown(f"## {title}")
    st.markdown(content)


def create_download_button(content: str, filename: str, button_text: str = "Download Markdown"):
    """
    Create a download button for the given content.
    """
    st.download_button(
        label=button_text,
        data=content,
        file_name=filename,
        mime="text/markdown"
    )


def get_user_input(prompt: str) -> str:
    """
    Get user input with a given prompt.
    """
    return st.text_input(prompt)


def show_success_message(message: str = "Operation completed successfully!"):
    """
    Display a success message.
    """
    st.success(message)


def show_error_message(message: str):
    """
    Display an error message.
    """
    st.error(message)


def show_warning_message(message: str):
    """
    Display a warning message.
    """
    st.warning(message)
