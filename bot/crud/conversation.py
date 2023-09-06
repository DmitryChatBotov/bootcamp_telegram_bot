import logging
from os import getenv

from common.cache import agent_cache
from models.langchain import ConversationAgent, llm


def chat_with_llm(user_id: int, text: str) -> str:
    if not agent_cache.get(user_id, None):
        agent_cache[user_id] = ConversationAgent(llm, getenv("SQLITE_FILE"))
    try:
        return agent_cache[user_id](text)
    except Exception as err:
        logging.info(err)
