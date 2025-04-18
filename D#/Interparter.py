#D# programing language v.0.1 
#Made by Daki0903
#Thank you for downloading
from colorama import Fore, Style

# Global dictionary for variables
variables = {}

# Define function colors mapping for easier reference
function_colors = {
    "print": Fore.CYAN,
    "open.file": Fore.GREEN,
    "write": Fore.YELLOW,
    "close": Fore.MAGENTA,
    "read.file": Fore.RED,
    "add.to.file": Fore.BLUE,
    "if": Fore.YELLOW,
    "while": Fore.GREEN,
}

def open_file(file_name):
    """Opens a file for writing."""
    if not file_name.endswith(".txt"):
        print("Error: File must be a .txt file")
        return None
    try:
        file = open(file_name, "w+")
        return file
    except Exception as e:
        print(f"Error opening file: {e}")
        return None

def write_to_file(file, text):
    """Writes text to a file."""
    if file:
        file.write(text + "\n")
        print(f"Written to file: {text}")
    else:
        print("Error: File is not open.")

def add_to_file(file, text):
    """Adds text to a file."""
    if file:
        file.write(text + "\n")
        print(f"Added to file: {text}")
    else:
        print("Error: File is not open.")

def close_file(file):
    """Closes a file."""
    if file:
        file.close()
        print("File closed.")
    else:
        print("Error: File is not open.")

def read_file(file_name):
    """Reads the content of a file."""
    try:
        with open(file_name, "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: {file_name} not found")
    except Exception as e:
        print(f"Error reading file: {e}")

def print_with_color(text, color="white"):
    """Prints text in a specified color."""
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
    }

    color_code = color_map.get(color.lower(), Fore.WHITE)
    print(color_code + text + Style.RESET_ALL)

def print_rgb_color(text, rgb_tuple):
    """Prints text in RGB color."""
    print(f"\033[38;2;{rgb_tuple[0]};{rgb_tuple[1]};{rgb_tuple[2]}m{text}\033[0m")

def interpret(line):
    """Interprets and executes a line of code."""
    line = line.strip()

    if line.startswith("--"):
        return  # Ignore comments

    elif "=" in line:
        parts = line.split("=")
        var_name = parts[0].strip()
        value = evaluate_expression(parts[1].strip())
        variables[var_name] = value
        print(f"{var_name} = {value}")
    
    elif line.startswith("function.d#.open.file("):
        handle_file_operation(line, "open")
    
    elif line.startswith("function.d#.write("):
        handle_file_operation(line, "write")
    
    elif line.startswith("function.d#.add.to.file("):
        handle_file_operation(line, "add")
    
    elif line.startswith("function.d#.read.file("):
        handle_file_operation(line, "read")
    
    elif line.startswith("function.d#.close()"):
        handle_file_operation(line, "close")
    
    elif line.startswith("function.d#.print("):
        handle_print_operation(line)
    
    elif line.startswith("function.d#.if"):
        handle_condition(line, "if")
    
    elif line.startswith("function.d#.while"):
        handle_condition(line, "while")
    
    elif line.startswith("function.d#.save.code("):
        code_to_save = line[len("function.d#.save.code("):-1].strip()
        save_code_to_file("main.d#", code_to_save)
    
    elif line.startswith("function.d#.load.code("):
        file_name = line[len("function.d#.load.code("):-1].strip()
        load_code_from_file(file_name)
    
    else:
        print(f"Unknown command: {line}")

def handle_file_operation(line, operation_type):
    """Handles file operations like open, write, add, read, close."""
    file_name = extract_file_name(line)
    if operation_type == "open":
        file = open_file(file_name)
        if file:
            print(f"File {file_name} opened successfully.")
    elif operation_type == "write":
        text = extract_text(line)
        write_to_file(file, text)
    elif operation_type == "add":
        text = input("Enter text to add to the file: ")
        add_to_file(file, text)
    elif operation_type == "read":
        read_file(file_name)
    elif operation_type == "close":
        close_file(file)

def handle_print_operation(line):
    """Handles print operations, including colored and RGB text."""
    parts = line[len("function.d#.print("):-1].split(")(")
    text = parts[0].strip().strip('"')
    color = parts[1].strip() if len(parts) > 1 else "white"

    if color.startswith("(") and color.endswith(")"):
        try:
            rgb_values = eval(color)
            print_rgb_color(text, rgb_values)
        except:
            print("Error: Invalid RGB color format.")
    else:
        print_with_color(text, color)

def handle_condition(line, condition_type):
    """Handles if and while conditions."""
    condition = line[len(f"function.d#{condition_type}("):-1].strip()
    if evaluate_expression(condition):
        print(f"Condition is True for {condition_type}")
    else:
        print(f"Condition is False for {condition_type}")

def extract_file_name(line):
    """Extracts file name from the line."""
    return line[len("function.d#.open.file("):-1].strip()

def extract_text(line):
    """Extracts text from the line."""
    return line[len("function.d#.write("):-1].strip()

def evaluate_expression(expr):
    """Evaluates expressions."""
    try:
        return eval(expr, {}, variables)
    except Exception as e:
        print(f"Error in expression: {e}")
        return None

def save_code_to_file(file_name, code):
    """Saves code to a file."""
    try:
        with open(file_name, "w") as file:
            file.write(code)
        print(f"Code saved successfully in {file_name}")
    except Exception as e:
        print(f"Error saving code: {e}")

def load_code_from_file(file_name):
    """Loads code from a file."""
    try:
        with open(file_name, "r") as file:
            code = file.read()
            print(f"Code from {file_name} loaded successfully:")
            print(code)
            run_code_from_string(code)
    except FileNotFoundError:
        print(f"Error: {file_name} not found")
    except Exception as e:
        print(f"Error reading file: {e}")

def run_code_from_string(code):
    """Runs code from a string."""
    lines = code.split("\n")
    for line in lines:
        interpret(line)

def run_program():
    """Main program loop."""
    print("🟢 Welcome to D# language! (type 'exit' to quit)")
    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() == "exit":
                break
            interpret(line)
        except Exception as e:
            print(f"Error: {e}")

run_program()


