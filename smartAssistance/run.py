from .graph import built_graph
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage



# request = "what are the recent updates of Antrophic ai company, how about the feedbacks for their new mythos model?"

# messages=built_graph.invoke({"user_request":request,
#                              "messages":[HumanMessage(content=request)]
#                              },
                            
#                              config={"configurable": {"thread_id": "conv_1"}}
#                             )

# for m in messages["messages"]:
#     m.pretty_print()

#-----------------------------------------------------------

# messages =built_graph.invoke(
#     Command(resume={"approve":"yes"}),
#     config={"configurable": {"thread_id": "conv_1"}}
# )

# for m in messages["messages"]:
#     m.pretty_print()

THREAD_ID = "conv_1"
config={"configurable": {"thread_id": THREAD_ID}}



def stream_output(graph_input):
    
    interrupted = None
    
    for chunk in built_graph.stream(
        graph_input,
        stream_mode="updates",
        config=config
        ):
        
        for node_update in chunk.values():
            if isinstance(node_update, dict) and "messages" in node_update:
                last_message = node_update["messages"][-1]

                # if the AI message contains tool calls
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        print(f"toolcall: {tool_call['name']}")

                # normal AI text response
                elif isinstance(last_message, AIMessage) and last_message.content:
                    print(last_message.content)
        
        if "__interrupt__" in chunk:
            interrupted = chunk["__interrupt__"]
            break
    return interrupted



print("hello , i am your pc assistance 😊,lets go!")

while True:
    
    user_query = input("what you are looking for?").strip()

    if user_query.lower() in {"exit", "quit"}:
        break
    
    interrupt_state = stream_output(
        {"user_request":user_query,
        "messages":[HumanMessage(content=user_query)]
        }
    )
    
    while interrupt_state:
        decision = input("Approve action? (yes/no): ").strip().lower()

        resume_value = "yes" if decision == "yes" else "reject"
        interrupt_state = stream_output(Command(resume={"approve":resume_value}))
        
        
    