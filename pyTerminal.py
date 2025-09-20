import os
import subprocess
import psutil
import shlex
import readline  # For command history & auto-completion

# ----- Enable History & Tab Completion -----
readline.parse_and_bind("tab: complete")

# Command history list
history_list = []

# ----- Command Handlers -----
def ls():
    return "\n".join(os.listdir())

def cd(path):
    try:
        os.chdir(path)
        return f"Changed directory to {os.getcwd()}"
    except FileNotFoundError:
        return f"Error: Directory '{path}' not found"
    except Exception as e:
        return str(e)

def pwd():
    return os.getcwd()

def mkdir(folder):
    try:
        os.makedirs(folder, exist_ok=True)
        return f"Folder '{folder}' created."
    except Exception as e:
        return str(e)

def rm(path):
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
        return f"Removed {path}"
    except FileNotFoundError:
        return f"Error: File/Directory '{path}' not found"
    except Exception as e:
        return str(e)

def cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def memory_usage():
    mem = psutil.virtual_memory()
    return f"Memory: {mem.percent}% used"

def processes():
    return "\n".join(
        [p.info["name"] for p in psutil.process_iter(["name"]) if p.info["name"]]
    )

def help_cmd():
    return """
Available commands:
  ls                  - List files
  cd <dir>            - Change directory
  pwd                 - Show current directory
  mkdir <folder>      - Create folder
  rm <file/folder>    - Remove file/folder
  cpu                 - Show CPU usage
  mem                 - Show memory usage
  ps                  - Show running processes
  history             - Show command history
  ai <natural query>  - Execute natural language command
  help                - Show this help
  exit                - Quit terminal
"""

# ----- AI/NLP Simple Interpreter -----
def ai_interpreter(query):
    query = query.lower()
    if "create folder" in query or "make folder" in query:
        words = query.split()
        if "called" in words:
            folder = words[words.index("called") + 1]
            return f"mkdir {folder}"
    if "move" in query and "into" in query:
        parts = query.split()
        if "move" in parts and "into" in parts:
            file = parts[parts.index("move") + 1]
            folder = parts[parts.index("into") + 1]
            return f"mv {file} {folder}"
    return query  # fallback to original

# ----- Command Dispatcher -----
def execute_command(command_line):
    if not command_line.strip():
        return ""

    # Save command to history
    history_list.append(command_line)

    # AI mode
    if command_line.startswith("ai "):
        command_line = ai_interpreter(command_line[3:])

    args = shlex.split(command_line)
    cmd = args[0]

    try:
        if cmd == "ls":
            return ls()
        elif cmd == "cd" and len(args) > 1:
            return cd(args[1])
        elif cmd == "pwd":
            return pwd()
        elif cmd == "mkdir" and len(args) > 1:
            return mkdir(args[1])
        elif cmd == "rm" and len(args) > 1:
            return rm(args[1])
        elif cmd == "cpu":
            return cpu_usage()
        elif cmd == "mem":
            return memory_usage()
        elif cmd == "ps":
            return processes()
        elif cmd == "help":
            return help_cmd()
        elif cmd == "history":
            return "\n".join(history_list)
        elif cmd == "exit":
            print("Exiting terminal...")
            exit(0)
        else:
            # Try running as system command
            result = subprocess.run(args, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

# ----- Main Loop -----
def terminal():
    print("Welcome to Advanced Python Terminal! Type 'help' for commands.")
    while True:
        try:
            command_line = input(f"{os.getcwd()}$ ")
            output = execute_command(command_line)
            if output:
                print(output)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit terminal.")

if __name__ == "__main__":
    terminal()

