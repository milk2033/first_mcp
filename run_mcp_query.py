import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from pokemon import get_all
import torch

# === Model setup ===
base_model_path = "/home/milk/models/mistral"
adapter_path = "./mcp-mistral-lora"

tokenizer = AutoTokenizer.from_pretrained(base_model_path, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16,
    local_files_only=True,
)
model = PeftModel.from_pretrained(model, adapter_path)


def run_mcp_query(user_query: str, data: list[dict], n_preview: int = 10):
    # Truncate for context length safety
    preview = data[:n_preview]
    preview_json = json.dumps(preview, indent=2)

    # Construct the prompt
    full_prompt = f"""You are a Python assistant. You are given a user query about Pokémon and a list of Pokémon dictionaries.
Each Pokémon has 'name' and 'url'. Here is a sample of the data:

{preview_json}

Write a Python function that analyzes the full list based on the user query:
"{user_query}"

Only output the function body. Assume the full list is passed in as 'pokemon_list'.

At the end, include this format:
# Arguments:
# any_argument: value
"""

    # Tokenize and generate
    inputs = tokenizer(
        full_prompt, return_tensors="pt", truncation=True, padding=True
    ).to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.7, top_p=0.9)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(response)

    print("✅ Final result:", response)
    # return result


user_input = "How many pokemon names are there"
pokemon_list = get_all()
print(pokemon_list)
