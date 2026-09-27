from pathlib import Path
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
files = Path("data/training").glob("*.json")
counts = []

for file_path in files:
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            messages = [
                { 
                    "role": "user", 
                    "content": item["question"] 
                },
                {
                    "role": "assistant",
                    "content": item["answer"]
                }
            ]
            token_ids = tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                enable_thinking=False
            )
            count = len(token_ids["input_ids"])
            counts.append((item["id"], count))
            print(item["id"], count)

print("Longest:", max(counts, key=lambda entry: entry[1]))