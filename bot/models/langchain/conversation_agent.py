# todo: тут нужна композиция
from pathlib import Path

from langchain import OpenAI, SQLDatabase, LLMChain
from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain


from models.langchain.config import CUSTOM_PROMPT
from models.langchain.tools.sql import SQLTool
from models.langchain.tools.booking_ner import NerBookingTool, NER_BOOKING_TEMPLATE


class ConversationAgent:
    def __init__(self, llm: OpenAI, db_file: str | Path):
        db: SQLDatabase = SQLDatabase.from_uri(f"sqlite:///{db_file}")
        db_chain: SQLDatabaseChain = SQLDatabaseChain.from_llm(
            llm, db, verbose=True, prompt=CUSTOM_PROMPT
        )

        prompt = PromptTemplate(template=NER_BOOKING_TEMPLATE, input_variables=[
            "input_text",
            "current_date",
            "masters_list",
            "service_list"
        ])
        ner_chain = LLMChain(prompt=prompt, llm=llm)

        tools: list[BaseTool] = [
            SQLTool(
                name="sql_tool",
                func=db_chain.run,
                description="Useful when user wants to know about beauty saloon masters or services, not bookings",
            ),
            NerBookingTool(
                name="ner_booking_tool",
                description="Useful when user asks to make or a cancel his booking to beauty salon."
                            "Also useful when user wants to check availability.",
                chain=ner_chain
            )
        ]
        self._agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True
        )

    def __call__(self, query: str):
        return self._agent({"input": query})
