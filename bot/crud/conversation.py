import logging
from os import getenv

from common.cache import user_agent_dict
from models.langchain import ConversationAgent, llm


def chat_with_llm(user_id, text):
    if not user_agent_dict.get(user_id, None):
        user_agent_dict[user_id] = ConversationAgent(llm, getenv("SQLITE_FILE"))
    try:
        answer = user_agent_dict[user_id](text)
        return answer
    except Exception as err:
        logging.error(err)
        return str(err)
