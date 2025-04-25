from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
from pokemon import get_all

# Paths
base_model_path = "/home/milk/models/mistral"
adapter_path = "./mcp-mistral-lora"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_path, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token

# Load base Mistral + LoRA adapter
model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16,
    local_files_only=True,
)
model = PeftModel.from_pretrained(model, adapter_path)


# Inference function
def query(prompt: str) -> str:
    full_prompt = f"### User:\n{prompt}\n\n### Response:\n"
    inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs, max_new_tokens=256, do_sample=True, temperature=0.7, top_p=0.9
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Example usage
user_prompt = "How many Pokémon start with the letter 'w'?"
response = query(user_prompt)
print(response)
