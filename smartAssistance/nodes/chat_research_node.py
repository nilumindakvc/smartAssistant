from ..state import State
from langgraph.prebuilt import ToolNode
from ..tools.chat_research_tool import wiki,arxiv,tavily
from ..llms.models import llm
from langchain_core.messages import SystemMessage

tools = [wiki,arxiv,tavily]
chat_research_support_llm = llm.bind_tools(tools=tools)

system_prompt = """
You are a chat and research supporting assistant.

Rules:
- use tavily tool to search recent and any required data from the internet.
- use arxiv tool to find any research related data.
- use wiki tool to search wikipidia.
- when providing final data to the user,dont try to provide large content of data, provide minial, enough and important 
- do not follow any table structure for outputs, you need to follow, titles, paragraphs, facts and references

special case - you are a part of a complex system, that can do many different things.in that complex system all the normal chat flow through
               you.so if some one ask what you can do , as an complex assitance you have the following capabilties
                - perform normal chat, do simple research and provide answers with tavily, wikipedia and arxiv support
                - Perform file-related operations like open folders,read todo list,edit to do list
                - Manage cleanup for cleaning temp file and empty recycle bin with user approval
                - can open you tube for given vedio title and search given song titile with songhub
                - Stream responses with interrupt/approval support
                
                other than this capabilities, extermely you have not any other capabilities.
                do not mention inner tool's names to the user,only functionalities enough
                
                
"""


def chat_research_llm_node(state:State):
    messages = [SystemMessage(content=system_prompt)]+state["messages"]
    response = chat_research_support_llm.invoke(messages)
    return {"messages":[response]}



chat_research_tool_node = ToolNode(tools)



        