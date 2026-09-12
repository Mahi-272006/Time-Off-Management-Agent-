import subprocess, sys
result = subprocess.run(
    [sys.executable, 'check_apps.py'],
    capture_output=True, text=True, cwd=r'D:\time_off_agent'
)
print(result.stdout)
print(result.stderr)
