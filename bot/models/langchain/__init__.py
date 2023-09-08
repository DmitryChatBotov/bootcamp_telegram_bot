# todo: переписать на фабрику
from langchain.chat_models import ChatOpenAI

from .conversation_chain import CustomConversationChain

llm = ChatOpenAI(temperature=0, verbose=True)
