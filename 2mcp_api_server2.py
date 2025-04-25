import json
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from pokemon import get_all
import torch

app = Flask(__name__)

# === Globals ===
model = None
tokenizer = None
pokemon_list = get_all()


def load_model():
    global model, tokenizer
    if model is None or tokenizer is None:
        print("🔧 Lazy-loading model and tokenizer...")
        base_model_path = "/home/milk/models/mistral"
        adapter_path = "./mcp-mistral-lora"

        tokenizer = AutoTokenizer.from_pretrained(
            base_model_path, local_files_only=True
        )
        tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_4bit=True,
            local_files_only=True,
        )
        model = PeftModel.from_pretrained(model, adapter_path)
        model.eval()


model_loaded = False


@app.route("/query", methods=["POST"])
def handle_query():
    global model_loaded
    if not model_loaded:
        print("loading model..")
        load_model()
        model_loaded = True
    # load_model()  # ensure model is loaded (but only once)
    # data = request.get_json()
    # user_query = data.get("query", "How many Pokémon names are there?")

    # preview = pokemon_list[:10]
    # preview_json = json.dumps(preview, indent=2)
    return jsonify({"response": "response2"})


#     prompt = f"""You are a Python assistant. You are given a user query about Pokémon and a list of Pokémon dictionaries.
# Each Pokémon has 'name' and 'url'. Here is a sample of the data:

# {preview_json}

# Write a Python function that analyzes the full list based on the user query:
# "{user_query}"

# Only output the function body. Assume the full list is passed in as 'pokemon_list'.

# At the end, include this format:
# # Arguments:
# # any_argument: value
# """

#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(
#         "cuda"
#     )
#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs, max_new_tokens=256, temperature=0.7, top_p=0.9
#         )

#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return jsonify({"response": response})


if __name__ == "__main__":
    app.run(port=8000, debug=True, use_reloader=True)
