import streamlit as st
import os

from router import route
from tools.file_tools import write_file, read_file, read_all_files
from tools.parser import extract_files_and_explanation
from tools.diff_tools import get_diff
from agents.explainer import explain_code

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


st.set_page_config(layout="wide")
st.title("CodeBuddy")


if "prompt" not in st.session_state:
    st.session_state.prompt = ""

if "pending_files" not in st.session_state:
    st.session_state.pending_files = []

if "applied_count" not in st.session_state:
    st.session_state.applied_count = 0

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None



left, center, right = st.columns([1.2, 2.2, 1.6])



def show_file_tree(root="workspace"):
    for path, dirs, files in os.walk(root):
        level = path.replace(root, "").count(os.sep)
        indent = " " * 2 * level

        st.write(f"{indent}📁 {os.path.basename(path)}")

        subindent = " " * 2 * (level + 1)
        for f in files:
            file_path = os.path.join(path, f)
            if st.button(f"{subindent}📄 {f}", key=file_path):
                st.session_state.selected_file = file_path


with left:
    st.subheader("📂 Directory")
    show_file_tree()



with right:
    st.subheader("AI Controls")

    mode = st.radio("Mode", ["Generate", "Modify", "Debug", "Explain"], label_visibility="hidden")

    user_input = st.text_area(
        "Prompt",
        value=st.session_state.prompt,
        key="prompt_box",
        height=200
    )

  

    if st.button("Run"):
        st.info("⏳ Working... please wait")

        try:
            result = route(mode, user_input)
        except Exception as e:
            st.error(f"Router crashed: {e}")
            st.stop()

        
        if not isinstance(result, dict):
            st.error("AI returned no usable response.")
            st.stop()

        response = result.get("code")
        explanation = result.get("explanation")

    
        if response:
            try:
                files, _ = extract_files_and_explanation(response)
                st.session_state.pending_files = files
                st.session_state.applied_count = 0
            except Exception as e:
                st.error(f"Failed to parse generated code: {e}")

        
        if explanation:
            st.write("### 🧠 Explanation")
            st.write(explanation)

        if not response and not explanation:
            st.warning("AI ran but returned empty output.")

        st.session_state.prompt = ""




with center:
    st.subheader("Viewer / Changes")

    
    if st.session_state.pending_files:
        st.success("Files ready to update")

        for filename, new_code in st.session_state.pending_files:
            try:
                old_code = read_file(filename)
            except:
                old_code = ""

            if old_code.strip() == "":
                st.write(f"### 📄 New file: `{filename}`")
                st.code(new_code)
            else:
                diff = get_diff(old_code, new_code)
                st.write(f"### 🔍 Changes in `{filename}`")
                st.code(diff)

            if st.button(f"Apply {filename}", key=f"apply_{filename}"):
                write_file(filename, new_code)
                st.success(f"✅ {filename} updated!")

                st.session_state.applied_count += 1

                if st.session_state.applied_count == len(st.session_state.pending_files):
                    files_content = read_all_files()
                    explanation = explain_code(
                        files_content,
                        "Explain what this project does after the latest changes."
                    )

                    st.write("### 🧠 What the AI did")
                    st.write(explanation)

                    st.session_state.pending_files = []
                    st.session_state.applied_count = 0

    
    elif st.session_state.selected_file:
        try:
            with open(st.session_state.selected_file, "r", encoding="utf-8") as f:
                st.code(f.read())
        except:
            st.write("Cannot preview this file.")

    else:
        st.info("Select a file from the left panel or run a prompt.")
