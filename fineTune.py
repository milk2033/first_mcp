import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType

# OPTIONAL: enforce offline mode globally
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# 1. Load dataset (local)
dataset = load_dataset("json", data_files="./mcp_pokemon.jsonl", split="train")

# 2. Load model/tokenizer (local only)
model_path = "/home/milk/models/mistral"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token  # ensure padding is set

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    local_files_only=True,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16,
)

# 3. Prepare model for LoRA fine-tuning
model = prepare_model_for_kbit_training(model)
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    bias="none",
)
model = get_peft_model(model, peft_config)


# 4. Tokenize dataset
def tokenize(example):
    prompt = f"### User:\n{example['prompt']}\n\n### Response:\n{example['response']}"
    tokens = tokenizer(prompt, truncation=True, padding="max_length", max_length=512)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens


tokenized = dataset.map(tokenize)

# 5. Training configuration
training_args = TrainingArguments(
    output_dir="./mcp-mistral-lora",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=1,  # optional: keep only latest
    fp16=True,
    report_to="none",
)

# 6. Run training
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()

# 7. Save LoRA adapter and tokenizer
model.save_pretrained("./mcp-mistral-lora")
tokenizer.save_pretrained("./mcp-mistral-lora")

print("✅ Training complete. LoRA adapter saved to ./mcp-mistral-lora")
