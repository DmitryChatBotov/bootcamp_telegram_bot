# todo: тут нужна композиция
from pathlib import Path

from langchain import OpenAI, SQLDatabase
from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool
from langchain_experimental.sql import SQLDatabaseChain

from models.langchain.config import CUSTOM_PROMPT
from models.langchain.tools.sql import SQLTool


class ConversationAgent:
    def __init__(self, llm: OpenAI, db_file: str | Path):
        db: SQLDatabase = SQLDatabase.from_uri(f"sqlite:///{db_file}")
        db_chain: SQLDatabaseChain = SQLDatabaseChain.from_llm(
            llm, db, verbose=True, prompt=CUSTOM_PROMPT
        )
        tools: list[BaseTool] = [
            SQLTool(
                name="sql_tool",
                func=db_chain.run,
                description="tool for extracting beauty saloon info",
            )
        ]
        self._agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )

    def __call__(self, query: str):
        return self._agent.run(query)
