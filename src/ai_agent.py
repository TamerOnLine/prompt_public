from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from database import store_response
from utils import save_to_markdown
from tools import generate_reference_link
from config import DEFAULT_MODEL

class AIAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.llm = ChatOllama(model=model_name, temperature=0.1)

    def generate_response(self, topic, tool):
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are an AI assistant. Explain {tool} in relation to {topic}.")
        ])
        response = self.llm.invoke(prompt.format(topic=topic, tool=tool))
        return response.content.strip() if response else None

    def get_relevant_tools(self, topic):
        prompt = f"List relevant tools, books, or methods for {topic}."
        response = self.generate_response(topic, "relevant tools")
        return response.split("\n") if response else []

    def generate_and_store_response(self, topic, tool):
        response_text = self.generate_response(topic, tool)
        if response_text:
            reference_link = generate_reference_link(topic, tool)
            store_response(topic, tool, response_text, reference_link)
            save_to_markdown(topic, tool, response_text, reference_link)
            return response_text, reference_link
        return None, None

def initialize_ai_agent(model_name):
    return AIAgent(model_name)
