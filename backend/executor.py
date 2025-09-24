import subprocess

def run_function_code(code: str) -> str:
    try:
        with open("temp.py", "w") as f:
            f.write(code)
        result = subprocess.run(["python", "temp.py"], capture_output=True, text=True, timeout=5)
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)
