import datetime
import json

from langchain import LLMChain, SQLDatabase
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_experimental.sql import SQLDatabaseChain
from models.langchain.prompts import (DIALECT, MASTERS_LIST, SERVICE_LIST,
                                      TABLE_INFO, consultant_prompt,
                                      ner_prompt, nlu_prompt, sql_prompt,)


class CustomConversationChain:
    def __init__(self, llm, db_file):
        self._nlu_chain = LLMChain(prompt=nlu_prompt, llm=llm)

        db = SQLDatabase.from_uri(f"sqlite:///{db_file}")
        self._db_chain = SQLDatabaseChain.from_llm(
            llm, db, verbose=True, prompt=sql_prompt
        )

        self._ner_chain = LLMChain(prompt=ner_prompt, llm=llm)

        self._conversation_chain = ConversationChain(
            llm=llm, memory=ConversationBufferMemory(), prompt=consultant_prompt
        )

    def __call__(self, query: str):
        action = self._nlu_chain.run(query)

        match action:
            case "Booking":
                current_date = datetime.date.today().strftime("%Y-%m-%d")
                masters_list = MASTERS_LIST  # TODO: change to db query
                service_list = SERVICE_LIST  # TODO: change to db query

                result = json.loads(
                    self._ner_chain.run(
                        input_text=query,
                        current_date=current_date,
                        masters_list=masters_list,
                        service_list=service_list,
                    )
                )

            case "SQL":
                result = self._db_chain.run(
                    input=query, table_info=TABLE_INFO, dialect=DIALECT, query=query
                )

            case "Consultant":
                result = self._conversation_chain.run(query)

            case _:
                result = None

        return action, result
