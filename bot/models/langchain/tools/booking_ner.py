import datetime
import json
from typing import Optional

from langchain import LLMChain
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool

class NerBookingTool(BaseTool):
    name: str
    description: str
    chain: LLMChain

    def __init__(self, name, description, chain, **kwargs):
        super(NerBookingTool, self).__init__(
            name=name, description=description, chain=chain, **kwargs
        )

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        masters_list = MASTERS_LIST  # TODO: change to db query
        service_list = SERVICE_LIST  # TODO: change to db query
        result = self.chain.run({
            "input_text": query,
            "current_date": current_date,
            "masters_list": masters_list,
            "service_list": service_list
        })

        return json.loads(result)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


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