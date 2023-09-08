from langchain.prompts import PromptTemplate

NLU_TEMPLATE = """
    Acs as assistant in beauty saloon that handles user input questions
    You need to classify questions by it's intent to 6 classes:
    - SQL - When user wants to know about beauty saloon masters or services, not bookings
    - Booking - When user asks to make or cancel his booking to beauty salon
    - Support - When user asks for human support 
    - Exit - When user wants to end the dialogue
    - Consultant - When user when a user wants to consult on beauty topics or asks general questions that are not related to other classes

    Here are some example:
    Question: Hello, it's Natalie. Can I have my nails done 26th of september at 10am
    Answer: Create

    Question: What services do you have?
    Answer: SQL

    Question: Can I cancel my booking that is tomorrow?
    Answer: Cancel

    Question: Okay, bye
    Answer: Exit

    Question: {input}
    Answer:
"""

nlu_prompt = PromptTemplate(template=NLU_TEMPLATE, input_variables=["input"])


SQL_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
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

sql_prompt = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=SQL_TEMPLATE
)


CONSULTANT_TEMPLATE = """
Act as a virtual assistant for a beauty saloon Krasota.Hamburg
Here are some topics you are good at:
- Beauty trends. Hairstyles, manicure, pedicure 
- Modern fashion
- Types of beauty services
Do not answer questions that are not relevant to those topics
You can perform small talk with user

Answer any other beauty salon-related queries or concerns user may have
If the topic of conversation is not related to the beauty sphere, answer without additional info: Let's change the topic of our conversation

Chat history, please remember it:
{history}
Question: {input}
Virtual assistant:
"""

consultant_prompt = PromptTemplate(
    input_variables=["input", "history"], template=CONSULTANT_TEMPLATE
)


NER_BOOKING_TEMPLATE = template = """
Extract relevant entity mentioned in the following message together with it's properties. 
The message is about booking an appointment to a beauty master for a service at specified date and time. 
So the entity is booking. 

Only extract the following properties:
action - Action with the booking. Possible values: Create, Cancel
master_name - Name of the master to whom user wants to go
beauty_service - Name of the beauty service
booking_date - Date of booking. Transform to YYYY-MM-DD format. Current date is {current_date}
booking_time - Time of booking. Transform to HH:MM format

Map master names with this list. If there is no master with such name, return null:
{masters_list}

Map service names with this list and return name from this list:
{service_list}
The information inside the description brackets is not part of the name

Output the result in the form of json with entity properties as keys. Make sure keys are enclosed in double quotes
If some properties are missing then place null in their values

User input: {input_text}
Result of retrieval:
"""

MASTERS_LIST = """
- Alice Johnson
- Bob Smith
- Charlie Brown
"""

SERVICE_LIST = """
- Haircut & Styling
- Basic Facial
- Manicure (or nails)
- Pedicure
- Hair Coloring
- Eyebrow Threading
- Deep Tissue Massage
"""

ner_prompt = PromptTemplate(
    template=NER_BOOKING_TEMPLATE,
    input_variables=["input_text", "current_date", "masters_list", "service_list"],
)
