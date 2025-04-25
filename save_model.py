from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "mistralai/Mistral-7B-Instruct-v0.1"
target_dir = "/home/milk/models/mistral"

model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

model.save_pretrained(target_dir)
tokenizer.save_pretrained(target_dir)

print("✅ Model saved to", target_dir)
