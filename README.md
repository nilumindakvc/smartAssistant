# Smart Assistance Agent

## Overview

This is a simple agentic assistant built with LangGraph and LangChain. It can process user queries, decide which workflow to follow, invoke tools, and stream back concise responses. The agent is designed to help with entertainment, file operations, system cleanup, and chat research tasks.

## What it can do

- perform normal chat, do simple research and provide answers with tavily,   wikipedia and arxiv support
- Perform file-related operations like open folders,read todo list,edit to do list
- Manage cleanup for cleaning temp file and empty recycle bin with user approval
- can open you tube for given vedio title and search given song titile with songhub
- Stream responses with interrupt/approval support

## Technologies used

- `langgraph` for graph-based agent workflows
- `langchain` / `langchain_core` for LLM message handling
- `selenium`, `wikipedia`, `arxiv`, and other helper libraries for tool functionality
- Groque api for llm support

## Setup

1. Open a terminal in `langraph Basics\smartAssistance`
2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:

   ```powershell
   .\.venv\Scripts\Activate
   ```

4. Install dependencies from `assist_requirements.txt`:

   ```powershell
   pip install -r assist_requirements.txt
   ```

## Configure recent file and todo list paths

The assistant expects a simple text file that stores the paths for your recently opened file list and your todo list file.

1. Create a file, for example:

   ```text
   path\to\your\file\smart_assistant_paths.txt
   ```

2. Add the file paths in it, for example:

   ```text
   pictures = path\to\your\picturs\folder
   todos    = path\to\todo_list.txt
   ```

3. Set an environment variables in .env file (below api keys can get for free for small scale usages)

   GROQ_API_KEY="your_api_key"

   TAVILY_API_KEY = "your_tavily_api_key"

   #includes paths of regularly opened folders with their good names in that path
   RECENT_DIRECTORIES_PATH = "path/to/recently/opened/file's/paths/file"

## Running the application

Run the agent from the `langraph Basics` folder:

```powershell
cd "\langraph Basics"
python -m smartAssistance.run
```

Then start interacting with the assistant through the console prompts.
