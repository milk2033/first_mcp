import json
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# === Load model and tokenizer ONCE ===
print("🔧 Loading Mistral model + LoRA adapter...")

base_model_path = "/home/milk/models/mistral"
adapter_path = "./mcp-mistral-lora"

tokenizer = AutoTokenizer.from_pretrained(base_model_path, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
    local_files_only=True,
)
model = PeftModel.from_pretrained(model, adapter_path)
model.eval()

# === Model Inference Server ===
app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        inputs = tokenizer(
            prompt, return_tensors="pt", truncation=True, padding=True
        ).to("cuda")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=128,
                temperature=0.7,
                top_p=0.9,
            )

        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5005)
