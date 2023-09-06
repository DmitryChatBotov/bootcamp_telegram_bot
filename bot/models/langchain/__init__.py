# todo: переписать на фабрику
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI

from .conversation_agent import ConversationAgent

llm = ChatOpenAI(temperature=0, verbose=True)
