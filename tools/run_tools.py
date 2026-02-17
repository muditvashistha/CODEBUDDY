import subprocess

def run_python_file(filename="main.py"):
    result = subprocess.run(
        ["python", f"workspace/{filename}"],
        capture_output=True,
        text=True
    )
    return result.stderr
