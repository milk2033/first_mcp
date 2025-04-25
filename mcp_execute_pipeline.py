import re
import ast
import traceback


def extract_function1(text):
    # Remove markdown backticks if present
    cleaned_text = "\n".join(
        line for line in text.splitlines() if not line.strip().startswith("```")
    )

    # Pattern to match complete function definitions including headers
    function_pattern = r"(def\s+\w+\s*\([^)]*\):(?:\r?\n|\Z)((?:[ \t]*.*?(?:\r?\n|\Z))+?))(?=#\s*Arguments:|\Z)"

    # Find all function definitions
    function_bodies = []
    for match in re.finditer(function_pattern, cleaned_text, re.MULTILINE | re.DOTALL):
        # Get full function (header + body)
        full_function = match.group(1).rstrip()
        lines = full_function.split("\n")

        if len(lines) > 1:
            # Get minimum indentation from function body
            indents = [
                len(line) - len(line.lstrip()) for line in lines[1:] if line.strip()
            ]
            if indents:
                min_indent = min(indents)
                body_lines = [
                    "    " + (line[min_indent:] if line.strip() else line.lstrip())
                    for line in lines[1:]
                ]
                full_function = lines[0] + "\n" + "\n".join(body_lines)

        function_bodies.append(full_function)

    return "\n\n".join(function_bodies)


def execute_code1(code_str: str, pokemon_list: list):
    """
    Executes a full function definition provided as a string.
    Assumes the function is named `analyze_pokemon_list(pokemon_list)`.
    """

    # Define a restricted set of safe built-ins
    safe_globals = {
        "__builtins__": {
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "sorted": sorted,
            "any": any,
            "all": all,
            "str": str,
            "int": int,
            "float": float,
            "range": range,
        }
    }
    local_vars = {}

    try:
        # Compile and execute the full function definition
        exec(code_str, safe_globals, local_vars)

        # Retrieve and call the function
        result = local_vars["analyze_pokemon_list"](pokemon_list)
        print("✅ Execution result:", result)
        return result

    except Exception as e:
        print("❌ Error while executing generated code:")
        traceback.print_exc()
        return None


def extract_function_body(text):
    """
    Extracts the analyze_pokemon_list function from a text.
    """
    # Find where the function definition starts
    start_index = text.find("def analyze_pokemon_list")
    if start_index == -1:
        return "Function not found"

    # Find the end of the function (before "# Arguments:")
    args_marker = text.find("# Arguments:", start_index)
    if args_marker == -1:
        # If no arguments marker, try to find the end some other way
        # This is a simplified approach and might need refinement
        end_index = text.find("\n\n", start_index)
        if end_index == -1:
            # If we can't find a clear end, return the rest of the text
            return text[start_index:]
    else:
        end_index = text.rfind("\n", start_index, args_marker)

    # Extract the function code
    function_code = text[start_index:end_index].strip()
    return function_code


def extract_arguments(text: str) -> dict:
    """
    Parses the # Arguments block and returns a dictionary of argument values.
    """
    print(text)
    arg_block_match = re.search(r"# Arguments:(.*)", text, re.DOTALL)
    if not arg_block_match:
        return {}

    args_raw = arg_block_match.group(1).strip()
    arg_lines = args_raw.splitlines()
    arg_dict = {}

    for line in arg_lines:
        match = re.match(r"#\s*(\w+):\s*(.+)", line)
        if match:
            key, val = match.group(1), match.group(2).strip()
            try:
                arg_dict[key] = ast.literal_eval(val)
            except Exception:
                arg_dict[key] = val  # fallback as raw string
    return arg_dict


def extract_arguments1(text):
    print(text)
    args = {}

    match = re.search(r"# Arguments:(.*)", text, re.DOTALL)
    if not match:
        return args  # no arguments block found

    block = match.group(1).strip()
    if block.lower().startswith("none"):
        return {}  # explicitly no arguments

    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("#"):
            continue
        line_content = line[1:].strip()  # Remove leading '#'
        if "=" not in line_content:
            continue  # skip malformed lines
        try:
            key, val = line_content.split("=", 1)
            key = key.strip()
            val = val.strip()
            args[key] = ast.literal_eval(val)
        except Exception:
            args[key] = val  # fallback as string

    return args


def execute_code(code_str: str, pokemon_list: list, args: dict):
    """
    Executes the extracted function body and returns the result.
    """
    safe_globals = {
        "__builtins__": {
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "sorted": sorted,
            "any": any,
            "all": all,
            "str": str,
            "int": int,
            "float": float,
        }
    }
    local_vars = {}

    function_code = "def analyze_pokemon_list(pokemon_list, **kwargs):\n"
    for line in code_str.splitlines():
        function_code += "    " + line + "\n"

    try:
        exec(function_code, safe_globals, local_vars)
        result = local_vars["analyze_pokemon_list"](pokemon_list, **args)
        return result
    except Exception as e:
        print("❌ Error during execution:")
        traceback.print_exc()
        return None


def run_pipeline(llm_output: str, pokemon_list: list):
    code = extract_function1(llm_output)
    print("////////CODE//////////")
    print(code)
    print("///////////////")
    execution = execute_code1(code, pokemon_list)
    print("//////EXECUTION///////")
    print(execution)
    print("///////////////")
    # print("🧠 Extracted Code:\n", code)
    # print("📦 Parsed Arguments:", args)

    # result = execute_code(code, pokemon_list, args)
    # print("✅ Execution Result:", result)
    # return result
    return "1"
