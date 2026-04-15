
from pydantic import BaseModel
from typing import Literal,Optional
from .llms.models import llm
from .state import State

class RouteDecision(BaseModel):
    route: Literal[
        "entertainment",
        "file_ops",
        "system_cleanup",
        "chat_research"
    ]
    confidence: float
    reason: Optional[str] = None

route_support_llm = llm.with_structured_output(RouteDecision)

# starting router node decision

def route_deciding_node(state:State):
    result = route_support_llm.invoke(
        f"""
    Classify the user's request into one route only.

    Routes:
    - entertainment
    - file_ops
    - system_cleanup
    - chat_research

    User request:
    {state["user_request"]}
    """)
    return{"required_route":result.route}


def route_selector(state: State):
    return state["required_route"]