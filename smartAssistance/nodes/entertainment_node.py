from ..state import State
from ..tools.entertainment_tools import open_youtube,open_songhub
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from ..llms.models import llm


tools = [open_youtube,open_songhub]
entertainment_support_llm = llm.bind_tools(tools= tools)

system_prompt = """
You are a entertainment supporting assistant.

Rules:
- Use the available tools to play music or open videos. 
- Use open_youtube for video, tutorial, or YouTube requests. 
- Use open_songhub for song/music requests.
"""

def entertainment_llm_node(state:State):
   
    messages = [SystemMessage(content=system_prompt)]+state["messages"]
    response = entertainment_support_llm.invoke(messages)
    return {"messages":[response]}

entertainment_tool_node = ToolNode(tools)    
    