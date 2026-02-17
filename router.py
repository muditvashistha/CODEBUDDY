from agents.generator import generate_code
from agents.debugger import debug_code
from agents.explainer import explain_code
from agents.modifier import modify_code

from tools.file_tools import read_all_files
from tools.run_tools import run_python_file
from tools.web_fetch import fetch_clean_html

import re


def route(mode, user_input):
    print("ROUTE CALLED:", mode)

    mode = mode.strip()

    
    if mode == "Generate":
        print("ENTERED GENERATE")

        if not user_input.strip():
            return {"code": None, "explanation": "Please enter a prompt."}

        url_match = re.search(r"https?://\S+", user_input)

        
        if url_match:
            url = url_match.group(0)
            html = fetch_clean_html(url)

            user_input = f"""
Create a project inspired by the structure and layout of this website.

Website HTML:
{html}

User request:
{user_input}
"""

        
        code_response = generate_code(user_input)
        return {"code": code_response, "explanation": None}

    
    if mode == "Modify":
        print("ENTERED MODIFY")

        if not user_input.strip():
            return {"code": None, "explanation": "Please enter a prompt."}

        code_response = modify_code(user_input)
        return {"code": code_response, "explanation": None}

    
    if mode == "Debug":
        print("ENTERED DEBUG")

        
        if "```" in user_input or len(user_input.strip().splitlines()) > 5:
            fixed_code = debug_code(user_input, "")
            return {"code": fixed_code, "explanation": None}

        
        code = read_all_files()
        error = run_python_file()
        fixed_code = debug_code(code, error)
        return {"code": fixed_code, "explanation": None}

    
    if mode == "Explain":
        print("ENTERED EXPLAIN")

        code = read_all_files()
        explanation = explain_code(code, user_input)
        return {"code": None, "explanation": explanation}

    
    return {"code": None, "explanation": "No response generated."}
