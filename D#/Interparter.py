from colorama import Fore, Style

# Globalni rečnik za promenljive
variables = {}

# Dodela boja za funkcije
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
    if file:
        file.write(text + "\n")

def add_to_file(file, text):
    if file:
        file.write(text + "\n")
        print(f"Added to file: {text}")

def close_file(file):
    if file:
        file.close()

def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: {file_name} not found")
    except Exception as e:
        print(f"Error reading file: {e}")

def print_with_color(text, color="white"):
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
    print(f"\033[38;2;{rgb_tuple[0]};{rgb_tuple[1]};{rgb_tuple[2]}m{text}\033[0m")

def interpret(line):
    line = line.strip()

    if line.startswith("--"):
        return  # Ignoriši komentar
    
    elif "=" in line:
        parts = line.split("=")
        var_name = parts[0].strip()
        value = evaluate_expression(parts[1].strip())
        variables[var_name] = value
        print(f"{var_name} = {value}")
    
    elif line.startswith("function.d#.open.file("):
        file_name = line[len("function.d#.open.file("):-1].strip()
        file = open_file(file_name)
        if file:
            print(f"File {file_name} opened successfully.")
    
    elif line.startswith("function.d#.write("):
        text = line[len("function.d#.write("):-1].strip()
        write_to_file(file, text)
        print(f"Written to file: {text}")
    
    elif line.startswith("function.d#.add.to.file("):
        file_name = line[len("function.d#.add.to.file("):-1].strip()
        file = open_file(file_name)
        text = input("Enter text to add to the file: ")
        add_to_file(file, text)
    
    elif line.startswith("function.d#.read.file("):
        file_name = line[len("function.d#.read.file("):-1].strip()
        read_file(file_name)
    
    elif line.startswith("function.d#.close()"):
        close_file(file)
        print("File closed.")
    
    elif line.startswith("function.d#.print("):
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
    
    elif line.startswith("function.d#.if"):
        condition = line[len("function.d#.if("):-1].strip()
        if evaluate_expression(condition):
            print("Condition is True")
        else:
            print("Condition is False")
    
    elif line.startswith("function.d#.while"):
        condition = line[len("function.d#.while("):-1].strip()
        while evaluate_expression(condition):
            print("Looping...")
            break
    
    elif line.startswith("function.d#.save.code("):
        code_to_save = line[len("function.d#.save.code("):-1].strip()
        save_code_to_file("main.d#", code_to_save)
    
    elif line.startswith("function.d#.load.code("):
        file_name = line[len("function.d#.load.code("):-1].strip()
        load_code_from_file(file_name)
    
    else:
        print(f"Unknown command: {line}")

def evaluate_expression(expr):
    try:
        return eval(expr, {}, variables)
    except Exception as e:
        print(f"Error in expression: {e}")
        return None

def save_code_to_file(file_name, code):
    try:
        with open(file_name, "w") as file:
            file.write(code)
        print(f"Code saved successfully in {file_name}")
    except Exception as e:
        print(f"Error saving code: {e}")

def load_code_from_file(file_name):
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
    lines = code.split("\n")
    for line in lines:
        interpret(line)

def run_program():
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
