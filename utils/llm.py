import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

def get_model(model: str = "gpt-4o", tools: list = None, temperature: float = 0) -> ChatOpenAI:
    # TODO: load API key and base url from environment variables
    os.environ["OPENAI_API_KEY"] = "any"
    model = ChatOpenAI(model=model, base_url="http://call.mystockpilot.com:13999", temperature=temperature)
    if tools and len(tools) > 0:
        model = model.bind_tools(tools)
    return model
