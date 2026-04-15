from ..state import State
from ..tools.entertainment_tools import open_youtube,open_songhub
from ..llms.models import llm


tools = [open_youtube,open_songhub]
entertainment_support_llm = llm.bind_tools(tools= tools)

# class youtube_request(BaseModel):
#     vedio_title:str=Field(description="this should be title for the vedio search")

def entertainment_node(state:State):
    user_text = state["user_request"]
    
    response = entertainment_support_llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "You are an entertainment assistant. "
                    "Use the available tools to play music or open videos. "
                    "Use open_songhub for song/music requests. "
                    "Use open_youtube for video, tutorial, or YouTube requests."
                ),
            },
            {
                "role": "user",
                "content": user_text,
            },
        ]
    )
    
    # If no tool was called
    if not response.tool_calls:
        return {
            "tool_result": {
                "success": False,
                "error": "No entertainment tool was selected by the LLM."
            }
            
        }
        
    # Take the first tool call
    tool_call = response.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    tool_map = {
        "open_youtube": open_youtube,
        "open_songhub": open_songhub,
    }
    
    # Execute the selected tool
    result = tool_map[tool_name].invoke(tool_args)

    return {
        "tool_result": result,
        "selected_tool": tool_name
    }

