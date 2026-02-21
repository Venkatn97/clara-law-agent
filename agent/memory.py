from typing import TypedDict, Annotated
import operator
from langchain_core.messages import BaseMessage

class CallerInfo(TypedDict, total=False):
    name:str
    phone:str
    email:str
    case_type:str
    urgency: str
    consultantion_booked: bool 
    lead_captured: bool 
    preferred_time: str 

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage],operator.add]
    session:str 
    caller_info: CallerInfo 
    tools_called: Annotated[list[str], operator.add]

def create_initial_state(session_id:str)-> AgentState: 
    from datetime import datetime 
    return {
        "messages":[],
        "session_id": session_id,
        "caller_info":{
            "consultation_booked":False,
            "lead_captured": False,
            "urgency": "normal"

        },
        "call_start_time":datetime.now().isoformat(),
        "tools_called":[] 

    }