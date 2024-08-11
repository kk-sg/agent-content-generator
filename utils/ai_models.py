# ai_models.py
from typing import List, Dict, Any, Optional
from openai import OpenAI
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
import streamlit as st


class OpenAILanguageModel(LLM):
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    client: Any = None

    def __init__(self):
        super().__init__()
        self.client = OpenAI()

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stop=stop
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f'Error in OpenAI API call: {e}')
            return ''

    @property
    def _llm_type(self) -> str:
        return "custom_openai"
