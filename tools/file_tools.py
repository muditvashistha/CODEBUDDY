import os

WORKSPACE = "workspace"

def write_file(filename, content):
    
    filename = filename.replace("`", "").strip()

    path = os.path.join(WORKSPACE, filename)

    #  Create folders if they don't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_all_files():
    collected = []

    for root, _, files in os.walk(WORKSPACE):
        for file in files:
            full_path = os.path.join(root, file)

            
            relative_path = os.path.relpath(full_path, WORKSPACE).replace("\\", "/")

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                continue  

            collected.append(f"# filename: {relative_path}\n{content}")

    return "\n\n".join(collected)


def read_file(filename):
    path = os.path.join(WORKSPACE, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

