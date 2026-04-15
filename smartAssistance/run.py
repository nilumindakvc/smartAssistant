from .graph import built_graph
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class _Fallback:
        RESET_ALL = ""
        GREEN = ""
        CYAN = ""
        YELLOW = ""
    Fore = _Fallback()
    Style = _Fallback()


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
    
    user_query = input(f"\n{Fore.GREEN}what you are looking for? {Style.RESET_ALL}").strip()

    if user_query:
        print(f"{Fore.CYAN}You asked:{Style.RESET_ALL} {user_query}")

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
        
        
    