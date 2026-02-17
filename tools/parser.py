import re

def extract_files_and_explanation(response: str):
    """
    Robust parser for LLM output.

    Works whether LLM returns:
    - Raw code after # filename
    - Markdown code blocks
    - Extra explanation text
    - Any programming language
    """

    files = []

    
    parts = re.split(r"# filename:\s*", response)

    
    explanation = parts[0].strip()

    for part in parts[1:]:
        lines = part.splitlines()

        
        filename = lines[0].replace("`", "").strip()

        
        content = "\n".join(lines[1:]).strip()

        
        content = re.sub(r"```[a-zA-Z]*", "", content)
        content = content.replace("```", "").strip()

        files.append((filename, content))

    return files, explanation
