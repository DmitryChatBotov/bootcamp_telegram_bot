# todo: переписать на фабрику
from langchain import OpenAI

from .conversation_agent import ConversationAgent

llm = OpenAI(temperature=0, verbose=True)
