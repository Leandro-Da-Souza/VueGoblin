import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_name, dtype=torch.float16)
model.to('cuda')

print(f"Model memory: {torch.cuda.memory_allocated() / 1024**2:.0f} MiB")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model.eval()

question = 'Hello how are you?'
messages = [{"role": "user", "content": question}]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    enable_thinking=False,
    return_tensors="pt"
)

with torch.inference_mode():
    inputs = inputs.to("cuda")
    
    output = model.generate(
        **inputs,
        max_new_tokens=16,
        do_sample=True,
        temperature=0.7,
        top_p=0.8,
        top_k=20
    )



print(f"Peak memory: {torch.cuda.max_memory_allocated() / 1024**2:.0f} MiB")