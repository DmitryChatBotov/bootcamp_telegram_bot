from typing import Optional

from langchain import PromptTemplate
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.tools import BaseTool
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain

TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
User asks about availability of making a booking, you must answer its questions using information about already boked time slots and masters working time
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}.

Here are some examples how you should think:
Question: Can I have a haircut on 11th of september at 17:00?
Thoughts: User want to check wether he can book a free slot for haircut to any master at 17:00. You should check if there any master available at 17:00 (he doesnt have any other bookings at that time)

Question: {input}"""

CUSTOM_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=TEMPLATE
)

db = SQLDatabase.from_uri("sqlite:///BeautySalon.db")
llm = OpenAI(temperature=0, verbose=True)

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=CUSTOM_PROMPT)

TABLE_INFO = """
This is a basic schema for a beauty salon's database. 

Masters:
id: An integer that serves as the primary key for each master. It's auto-incremented.
name: A text field that stores the name of the master.
start_working_hour: A text field (in the format HH:MM) that indicates when the master starts their workday.
end_working_hour: A text field (in the format HH:MM) that indicates when the master ends their workday.

Services:
id: An integer that serves as the primary key for each service. It's auto-incremented.
name: A text field that describes the beauty service.
price: A real number that indicates the cost of the service.
duration_minutes: An integer that represents the duration of the service in minutes.

Clients:
id: An integer that serves as the primary key for each client. It's auto-incremented.
name: A text field that stores the name of the client.
phone: A text field that stores the client's phone number.

Bookings. Each booking have the master, client and service. If master is busy with the booking he cannot service another clients:
booking_id: An integer that serves as the primary key for each booking. It's auto-incremented.
client_id: A foreign key that references the client_id in the Clients table.
master_id: A foreign key that references the master_id in the Masters table.
service_id: A foreign key that references the service_id in the Services table.
date: A text field that stores the date of the booking.
start_time: A text field (in the format HH:MM) that indicates the start time of the booking.
end_time: A text field (in the format HH:MM) that indicates the end time of the booking. This is calculated based on the start_time and the duration of the service.
price: A real number that indicates the price of the booked service.
"""

dialect = "sqlite"


class SQLTool(BaseTool):
    name = "sql_tool"
    description = "Useful for when you need to answer questions about booking, reservations, appointment using SQL queries"

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return db_chain.run(query)

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


tools = [SQLTool()]
