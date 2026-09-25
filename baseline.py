from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "Qwen/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model.eval()

question = "I have a large Vue 2 application using Vuex, mixins, filters, and the Options API. How would you approach migrating it incrementally to Vue 3, and which breaking changes should I watch for?"
messages = [{"role": "user", "content": question}]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    enable_thinking=False,
    return_tensors="pt"
)

print(f"Prompt length: {inputs['input_ids'].shape[-1]} tokens")

torch.manual_seed(19)

with torch.inference_mode():
    output = model.generate(
        **inputs,
        max_new_tokens=400,
        do_sample=True,
        temperature=0.7,
        top_p=0.8,
        top_k=20
    )

answer_ids = output[0][inputs['input_ids'].shape[-1]:]
print(tokenizer.decode(answer_ids, skip_special_tokens=True))