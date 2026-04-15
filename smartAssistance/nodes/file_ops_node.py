from ..state import State
from ..tools.file_ops_tools import open_folder,find_recently_opened_directory_paths,read_text_file,append_to_text_file
from ..llms.models import llm
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode

tools = [open_folder,find_recently_opened_directory_paths,read_text_file,append_to_text_file]
file_ops_support_llm = llm.bind_tools(tools=tools)

system_prompt = """
You are a file operation supporting assistant.

Rules:
- Use find_recently_opened_directory_paths to find file paths for user requested destinations.
- To open a directory, use open_folder with a path found from find_recently_opened_directory_paths.
- To find the user's ToDo list, first find the path using find_recently_opened_directory_paths, then read it using read_text_file.
- When the user asks to add ToDos, first read the ToDo file, inspect the writing format, then append the new ToDo using append_to_text_file.
"""


def file_ops_llm_node(state:State):
   
    messages = [SystemMessage(content=system_prompt)]+state["messages"]
    response = file_ops_support_llm.invoke(messages)
    return {"messages":[response]}

file_ops_tool_node = ToolNode(tools)    
    
    
    
    
