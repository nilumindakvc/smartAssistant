from pathlib import Path
import os
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

recent_directories_path = os.getenv("RECENT_DIRECTORIES_PATH")



@tool
def append_to_text_file(file_path: str, content: str) -> dict:
    """this function capable of appending text data to
    existing text file in given path"""
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content + "\n")
        return {
            "success": True,
            "message": "Content appended successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }  
      #update state     

# @tool      
def read_text_file(file_path: str) -> dict:
    """this function can read data from text file
    in given path"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return {
            "success": True,
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
     #update state   
     

@tool     
def find_recently_opened_directory_paths()->list:
    """this function return path data related to recently opend files
    with some user given names for recent files"""
    
    path = recent_directories_path
    result = read_text_file(path)
    return result["content"] 
    #update state           
 

@tool    
def open_folder(path: str) -> dict:
    "this function can open a folder of a given path"
    try:
        if not Path(path).exists():
            return {
                "success": False,
                "error": "Path does not exist"
            }

        os.startfile(path)
        return {
            "success": True,
            "opened": path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    #update state here    