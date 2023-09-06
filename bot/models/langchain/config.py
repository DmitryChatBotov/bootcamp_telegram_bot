from langchain import PromptTemplate

# TODO: прокидывать существующих мастеров и сервисы не так топорно

TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
User asks about beauty salon services and masters. Don't answer on any other questions
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run" Make sure you map services names with the existing in the database, same with masters
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Existing masters:
- Alice Johnson
- Bob Smith
- Charlie Brown

Existing services:
- Haircut & Styling
- Basic Facial
- Manicure (or nails)
- Pedicure
- Hair Coloring
- Eyebrow Threading
- Deep Tissue Massage

Only use the following tables:

{table_info}.

You dont answer questions about bookings. These are only tables that you have

Question: {input}"""

CUSTOM_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=TEMPLATE
)

TABLE_INFO = """
This is a basic schema for a beauty salon's database. 

Masters:
master_id: An integer that serves as the primary key for each master. It's auto-incremented.
name: A text field that stores the name of the master.
start_working_hour: A text field (in the format HH:MM) that indicates when the master starts their workday.
end_working_hour: A text field (in the format HH:MM) that indicates when the master ends their workday.

Services:
service_id: An integer that serves as the primary key for each service. It's auto-incremented.
name: A text field that describes the beauty service.
price: A real number that indicates the cost of the service in dollars.
duration_minutes: An integer that represents the duration of the service in minutes.
"""

DIALECT = "sqlite"
