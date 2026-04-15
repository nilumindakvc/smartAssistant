import winshell
import tempfile
import shutil
from pathlib import Path
from langchain_core.tools import tool



def empty_recycle_bin():
    """This function meant to be used 
    clear all the content inside the recycle bin"""
    try:   
        winshell.recycle_bin().empty(confirm=False,
            show_progress=True, sound=True)

        return {
            "success": True,
            "message": "Recycle Bin emptied successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Could not empty Recycle Bin: {str(e)}"
        }
  


def delete_temp_files() -> dict:
    """this function can effeciently handle
    deletion process of content inside temp folder
    C drive"""
    temp_path = Path(tempfile.gettempdir())

    deleted = []
    failed = []

    for item in temp_path.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
            deleted.append(str(item))
        except Exception as e:
            failed.append({
                "path": str(item),
                "error": str(e)
            })

    return {
        "success": True,
        "temp_path": str(temp_path),
        "deleted_count": len(deleted),
        "failed_count": len(failed)    
    }
    