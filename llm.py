import os
from dotenv import load_dotenv
import openai
from pokemon import get_all
import json
import subprocess
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel
import torch

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_key)
pokemon_list = get_all()


# def run_mistral(prompt: str) -> str:
#     result = subprocess.run(
#         ["ollama", "run", "mistral"], input=prompt.encode(), stdout=subprocess.PIPE
#     )
#     return result.stdout.decode()


def load_model():
    base_model = "mistralai/Mistral-7B-Instruct-v0.1"

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        load_in_4bit=True,  # bitsandbytes magic
        device_map="auto",  # puts model on your GPU
        torch_dtype=torch.float16,
    )

    # Optional: load LoRA adapter if you’ve fine-tuned it
    # model = PeftModel.from_pretrained(model, "path/to/lora")

    return tokenizer, model


tokenizer, model = load_model()


# def run_mistral(prompt: str) -> str:
#     inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs, max_new_tokens=256, do_sample=True, temperature=0.7
#         )
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)


# print(model)

# def llm_client(user_query: str, pokemon_list):
#     print("pokemon list.......", pokemon_list)
#     # send message to the LLM and return the response
#     pokemon_list_str = json.dumps(pokemon_list, indent=2)

#     # need to add to the prompt to use python for counting stuff

#     # system_prompt = (
#     #     "You are a Python assistant. You are given a user query about Pokémon and a list of Pokémon "
#     #     "dictionaries, each with 'name', 'url'\n\n"
#     #     # "You are a code assistant. Given a user query and a JSON list of names, generate a Python expression that answers the question precisely.\n"
#     #     "Write a Python function that filters that list according to the user's request.\n"
#     #     "Do not count manually — use len() or other appropriate functions. Only output code."
#     #     "Return only the function body. Assume 'pokemon_list' is the input.\n"
#     #     "After the function, inclue a comment block in this format:\n"
#     #     "# Arguments:\n"
#     #     "# arg1: value\n"
#     #     "# arg2: value\n"
#     #     "You are not limited to 2 arguments. But you must use this argument format for all additional arguments\n"
#     #     "Use actual values, not type annotations, in the `# Arguments:` section. If unsure, make your best guess based on the query."
#     # )
# system_prompt = (
#     "You are a Python assistant. You are given a user query about Pokémon and a list of Pokémon "
#     "dictionaries, each with 'name' and 'url'.\n\n"
#     "Write a Python function that filters or analyzes that list according to the user's request.\n"
#     "Do not count manually — use len() or other appropriate functions.\n"
#     "Only output code, no extra explanation.\n"
#     "Return only the function body. Assume 'pokemon_list' is always the input.\n\n"
#     "After the function, include a comment block in this format:\n"
#     "# Arguments:\n"
#     "# argname: value_to_pass\n\n"
#     "Use actual values based on the user's request.\n"
#     "Do NOT include data types, descriptions, or annotations.\n"
#     "Only include values like strings, numbers, booleans, or lists in proper Python syntax.\n"
#     "Do NOT include 'pokemon_list' in the arguments block — it is always passed automatically."
# )
#     user_message = f"""The user wants to know: "{user_query}"
#         Here is the pokemon data that you may use: {pokemon_list}
#         Respond with your answer only. Be brief"""

#     full_prompt = system_prompt + "\n\n" + user_message.strip()

#     # response = run_mistral(full_prompt)
#     response = run_mistral(full_prompt)
#     print(response)

#     return response


# def run_generated_code(code_str: str, pokemon_list: list[str]) -> int:
#     print("Input code:\n", code_str)

#     # Define a minimal set of safe built-ins
#     safe_globals = {
#         "__builtins__": {
#             "len": len,
#             "sum": sum,
#             "min": min,
#             "max": max,
#             "sorted": sorted,
#             "any": any,
#             "all": all,
#             "str": str,
#             "int": int,
#             "float": float,
#         }
#     }

#     # This will hold the defined function
#     local_vars = {}

#     try:
#         # Run the code to define the function
#         exec(code_str, safe_globals, local_vars)

#         # Grab the first function in local_vars
#         func = next(v for v in local_vars.values() if callable(v))

#         # Run the function with the provided list
#         result = func(pokemon_list)
#         # print("✅ Result:", result)
#         return result

#     except Exception as e:
#         print("❌ Error executing generated code:", e)
#         return None


# # def extract_code_block(text: str) -> str:
# #     # Find the first triple backtick block with Python code
# #     code_match = re.search(r"```python(.*?)```", text, re.DOTALL | re.IGNORECASE)
# #     if code_match:
# #         return code_match.group(1).strip()
# #     else:
# #         # fallback: try to strip everything before the first def
# #         fallback = text.split("def ", 1)
# #         if len(fallback) > 1:
# #             return "def " + fallback[1].strip()
# #         raise ValueError("No code block found in LLM output")


# def extract_code_block(text: str) -> str:
#     code_match = re.search(r"```python(.*?)```", text, re.DOTALL | re.IGNORECASE)
#     if code_match:
#         return code_match.group(1).strip()
#     else:
#         # fallback: grab from "def" onward
#         fallback = text.split("def ", 1)
#         if len(fallback) > 1:
#             return "def " + fallback[1].split("# Arguments:")[0].strip()
#         raise ValueError("No code block found in LLM output")


# # def clean_code(code_str: str) -> str:
# #     lines = code_str.strip().split("\n")
# #     cleaned_lines = []
# #     for line in lines:
# #         # Only keep lines that are part of the function (indented or `def`)
# #         if line.startswith("def") or line.startswith("    "):
# #             cleaned_lines.append(line)
# #         else:
# #             break  # stop at first non-function-related line
# #     return "\n".join(cleaned_lines)


# def clean_code(code_str: str) -> str:
#     lines = code_str.strip().splitlines()
#     cleaned_lines = []
#     for line in lines:
#         if line.startswith("def") or line.startswith("    "):
#             cleaned_lines.append(line)
#         elif line.strip() == "":
#             continue  # ignore blank lines
#         else:
#             break
#     return "\n".join(cleaned_lines)


# def extract_arguments(text: str) -> dict:
#     arg_section_match = re.search(r"# Arguments:(.*)", text, re.DOTALL | re.IGNORECASE)
#     if not arg_section_match:
#         return {}

#     args_raw = arg_section_match.group(1).strip()
#     arg_lines = args_raw.splitlines()
#     arg_dict = {}

#     for line in arg_lines:
#         match = re.match(r"#\s*(\w+):\s*(.+)", line)
#         if match:
#             key = match.group(1)
#             value = match.group(2).strip()

#             # Try to cast to appropriate type
#             if value.lower() == "true":
#                 value = True
#             elif value.lower() == "false":
#                 value = False
#             elif value.isdigit():
#                 value = int(value)
#             elif re.match(r"^-?\d+\.\d+$", value):
#                 value = float(value)
#             elif value.startswith('"') and value.endswith('"'):
#                 value = value[1:-1]
#             elif value.startswith("'") and value.endswith("'"):
#                 value = value[1:-1]

#             arg_dict[key] = value

#     return arg_dict


# # llm_result = llm_client("How many pokemon names are there", pokemon_list)

# llm_result = llm_client(
#     "How many pokemon names begin with the letter 'w'?", pokemon_list
# )


# print("llm_result \n", llm_result)

# code = extract_code_block(llm_result)
# print("extract_code_block result....", code)

# cleaned_code = clean_code(code)
# print("cleaned_code....", cleaned_code)

# args = extract_arguments(llm_result)
# print("args....", args)
