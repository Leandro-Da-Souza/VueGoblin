from peft import LoraConfig, get_peft_model
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
from pathlib import Path

model_name = "Qwen/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_name, dtype=torch.float16)

config = LoraConfig(
    r=4,
    lora_alpha=8,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, config)
model.print_trainable_parameters()

model.gradient_checkpointing_enable()
model.to('cuda')
model.train()

tokenizer = AutoTokenizer.from_pretrained(model_name)
examples = []

for path in sorted(Path('data/training').glob("*.json")):
    examples.extend(json.loads(path.read_text(encoding="utf-8")))

print(f"Loaded {len(examples)} examples")

optimizer = torch.optim.AdamW(
    (p for p in model.parameters() if p.requires_grad),
    lr=1e-4,
)

for step, example in enumerate(examples, start=1):
    messages = [
        {"role": "user", "content": example["question"]},
        {"role": "assistant", "content": example["answer"]}
    ]

    batch = tokenizer.apply_chat_template(
        messages,
        enable_thinking=False,
        return_tensors="pt"
    ).to("cuda")

    prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": example["question"]}],
        add_generation_prompt=True,
        enable_thinking=False,
        return_tensors="pt"
    ).to("cuda")

    prompt_length = prompt["input_ids"].shape[-1]
    assert torch.equal(
        batch["input_ids"][0, :prompt_length],
        prompt["input_ids"][0],
    ), example["id"]

    labels = batch["input_ids"].clone()
    labels[:, :prompt_length] = -100

    loss = model(**batch, labels=labels).loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    print(f"{step:02d}/{len(examples)} {example['id']} loss={loss.item():.3f}")

model.save_pretrained("outputs/vuegoblin-lora-v1")
print(f"Peak GPU memory: {torch.cuda.max_memory_allocated() / 1024**2:.0f} MiB")
print("Saved adapter to outputs/vuegoblin-lora-v1")
