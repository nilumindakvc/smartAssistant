from ..state import State
from ..tools.cleaning_tools import empty_recycle_bin,delete_temp_files
from ..llms.models import llm
from langchain_core.messages import SystemMessage
from langgraph.types import interrupt
from langchain_core.messages import ToolMessage


tools = [empty_recycle_bin,delete_temp_files]
clean_support_llm = llm.bind_tools(tools=tools)

system_prompt = """
You are a system cleaning supporting assistant.

Rules:
- Use the tool empty_recycle_bin to empty the recycle bin.
- Use the tool delete_temp_files to delete files in the temp folder
"""

def clean_manager_llm_node(state:State):
    messages = [SystemMessage(content=system_prompt)]+state["messages"]
    response = clean_support_llm.invoke(messages)
    return {"messages":[response]}
       


def clean_manager_approval_node(state:State):
    last_msg = state["messages"][-1]
    
    if not getattr(last_msg,"tool_calls",None):
        return {}
    
    tool_call = last_msg.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call.get("args",{})
    
    decision = interrupt({
        "type":"approval_request",
        "tool_name":tool_name,
        "tool_args":tool_args,
        "message":f"Approve execution of {tool_name}?"
    })
    
    if decision.get("approve") != "yes":
        return{
            "message":[
                ToolMessage(
                    content=f"Execution of tool '{tool_name}' was rejected by user.",
                    tool_call_id = tool_call["id"]
                )
            ]
        }
        
    if tool_name == "empty_recycle_bin":
        result = empty_recycle_bin()
    elif tool_name == "delete_temp_files":
        result = delete_temp_files()
    else:
        result = {"error":f"Unknown tool: {tool_name}"}
    
    return{
        "messages":[
            ToolMessage(
                content= str(result),
                 tool_call_id=tool_call["id"]
            )
        ]
    }