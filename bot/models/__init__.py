from langchain.chat_models import ChatOpenAI

from .langchain_agents import CustomConversationChain
from .whisper import WhisperWrapper

whisper_model = WhisperWrapper()
llm = ChatOpenAI(temperature=0, verbose=True)
