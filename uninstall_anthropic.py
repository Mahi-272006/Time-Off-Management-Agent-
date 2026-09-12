import subprocess
result = subprocess.run(
    ['D:/time_off_agent/venv/Scripts/pip', 'uninstall', '-y', 'anthropic', 'langchain-anthropic'],
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr)
