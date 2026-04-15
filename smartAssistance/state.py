from typing import Annotated, Optional
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

    

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_request:str
    required_route:Optional[str]
    tool_result:Optional[dict[str,str]]
    