from langgraph.graph import StateGraph,START,END
from .state import State
from .nodes import entertainment_node,file_ops_tool_node,file_ops_llm_node,clean_manager_llm_node,clean_manager_approval_node,chat_research_llm_node,chat_research_tool_node
from .route import route_deciding_node,route_selector
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver


memory = MemorySaver()
builder = StateGraph(State)

# registering nodes for the graph
builder.add_node("routing_node",route_deciding_node)
builder.add_node("entertainment_node",entertainment_node)
builder.add_node("file_ops_llm_node",file_ops_llm_node)
builder.add_node("file_ops_tool_node",file_ops_tool_node)
builder.add_node("clean_manager_llm_node",clean_manager_llm_node)
builder.add_node("clean_manager_approval_node",clean_manager_approval_node)
builder.add_node("chat_research_llm_node",chat_research_llm_node)
builder.add_node("chat_research_tool_node",chat_research_tool_node)

# creating edges
builder.add_edge(START,"routing_node")


builder.add_conditional_edges(
    "routing_node",
    route_selector,
    {
        "entertainment": "entertainment_node",
        "file_ops": "file_ops_llm_node",
        "system_cleanup": "clean_manager_llm_node",
        "chat_research": "chat_research_llm_node"
        
    }
)

builder.add_edge("entertainment_node",END)

builder.add_conditional_edges(
    "file_ops_llm_node",
    tools_condition,
    {
        "tools":"file_ops_tool_node",
        "__end__":END
    }
)
builder.add_edge("file_ops_tool_node","file_ops_llm_node")

builder.add_conditional_edges(
    "clean_manager_llm_node",
    tools_condition,
    {
        "tools":"clean_manager_approval_node",
        "__end__": END
    }
    )
builder.add_edge("clean_manager_approval_node","clean_manager_llm_node")

builder.add_conditional_edges(
    "chat_research_llm_node",
    tools_condition,
    {
        "tools":"chat_research_tool_node",
        "__end__": END
    }
    )
builder.add_edge("chat_research_tool_node","chat_research_llm_node")

built_graph = builder.compile(checkpointer=memory)