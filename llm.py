import subprocess

def ask_llm(prompt: str) -> str:
    print("\n====== PROMPT SENT TO LLM ======\n")
    print(prompt)

    result = subprocess.run(
        ["ollama", "run", "qwen2.5-coder"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8", errors="ignore")

    print("\n====== RAW LLM OUTPUT ======\n")
    print(output)

    return output
