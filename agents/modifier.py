from llm import ask_llm
from tools.file_tools import read_all_files

SYSTEM_PROMPT = """
You are a senior software engineer working inside an AI coding IDE.

You will be given existing project files along with their exact filenames.

Your job is to MODIFY those files according to the user's request.

You may ONLY modify files listed above.
Do NOT invent new file paths.
If the requested file path does not exist, choose the closest existing file.


STRICT RULES:
- You MUST ONLY output files using this exact format:

# filename: styles/style.css
<updated code here>

- Even if only one file is modified, you MUST include the "# filename:" line exactly like shown above.
- Do NOT create new files or new paths.
- Do NOT explain anything.
- Do NOT use markdown.

Your output will be parsed automatically. Any deviation from this format will break the system.

"""

def modify_code(user_prompt):
    files = read_all_files()

    prompt = SYSTEM_PROMPT + f"""

    Existing project files:
    {files}

    User request:
    {user_prompt}
    """
    return ask_llm(prompt)
