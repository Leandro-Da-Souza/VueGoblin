# VueGoblin

VueGoblin is a learning experiment in **model specialization**: how much can a small language model improve on one narrow subject, Vue.js, when we fine-tune it on carefully written examples?

The current VueGoblin is [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) plus a small [LoRA](https://huggingface.co/docs/peft/en/conceptual_guides/lora) adapter. The original Qwen weights remain frozen; training changes the adapter. This project tests changes to the model itself. It does not use document retrieval or a hosted chatbot API.

This is an early experiment, **not a dependable Vue assistant**.

## What has been done

1. Saved answers from untouched Qwen3-0.6B to five Vue questions as a baseline.
2. Wrote 25 question-and-answer training examples: five each for Vue fundamentals, API styles, shared state, asynchronous requests, and Vue 2 to 3 migration.
3. Trained a LoRA adapter for one pass over those examples, scoring answer tokens while masking question tokens from the loss.
4. Asked the same five evaluation questions with the saved adapter and reviewed the answers against Vue ecosystem documentation.

The training data lives in [`data/training/`](data/training/); the five main questions are in [`questions.txt`](questions.txt). The untouched and adapted model answers, with separate human reviews, are in [`evaluations/`](evaluations/). Model answers in those files are intended to be preserved as generated.

## First result

| Topic                          | VueGoblin v1 observation                                                                                                                 |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Vue fundamentals               | Shorter and fewer factual errors than the baseline, but it did not explain dependency tracking and described DOM updates as “real-time.” |
| Options API vs Composition API | Confused `<script setup>` macros with Options API and misused “functional component.”                                                    |
| Shared state                   | Recommended Pinia for widely shared state, but wrongly claimed Pinia should be a single root store.                                      |
| Async search                   | Did not make an asynchronous request or prevent stale results despite a related training example.                                        |
| Vue 2 to 3 migration           | Incorrectly advised removing Vuex, mixins, Options API, and Vue Router as migration steps.                                               |

**Interpretation:** one answer became cleaner; the other four still contain substantial errors. Five hand-reviewed questions and 25 training examples do not establish general Vue ability. This run shows that the training pipeline works and gives us concrete failures to investigate.

The first run used LoRA rank 4 on `q_proj` and `v_proj`, with 573,440 trainable parameters (about 0.096% of the combined parameter count). The saved adapter is in [`outputs/vuegoblin-lora-v1/`](outputs/vuegoblin-lora-v1/) and needs the Qwen base model to run. Training used a batch of one example, gradient checkpointing, FP16 model weights, AdamW at `1e-4`, and one pass over the files in sorted filename order. The training script does not set a random seed, so a fresh run need not reproduce this exact adapter.

On the development laptop (NVIDIA T500, 2 GiB VRAM), the longest example was 129 tokens and the run reported 1,392 MiB peak _PyTorch-allocated_ GPU memory. A CUDA allocator warning occurred, but all 25 updates completed and the adapter was saved. This figure is not a guarantee that longer examples will fit.

## Run it locally

Use a Python virtual environment. This project was developed on Fedora 44 with Python 3.14 and a CUDA-enabled PyTorch build; package versions are not yet pinned. Install a PyTorch build appropriate for your hardware using the [official installation guide](https://pytorch.org/get-started/locally/), then install Transformers and PEFT:

```sh
python3 -m venv .venv
# In fish: source .venv/bin/activate.fish
# In bash/zsh: source .venv/bin/activate
python -m pip install transformers peft
```

Run these commands from the repository root:

```sh
python inspect_data.py  # Print token counts for the 25 examples
python baseline.py      # Untouched Qwen answer
python evaluate.py      # Qwen with the saved VueGoblin adapter
```

`baseline.py` and `evaluate.py` currently each contain a **hardcoded question** (the migration question in the committed scripts). Edit that line to run another question from `questions.txt`. Both scripts use thinking off, seed 19, sampling with temperature 0.7 / top-p 0.8 / top-k 20, and a maximum of 400 new tokens. Keep the same question and settings for a comparison; the reviews were written manually, not by an automated scorer. The saved evaluations record the outputs from the first experiment.

To train a new adapter:

```sh
python train.py
```

`train.py` assumes an NVIDIA CUDA GPU, loads the Qwen model, and writes to `outputs/vuegoblin-lora-v1/`. Running it again **replaces that local output path**; copy or rename the existing adapter first if you want to keep this run. The model weights download on first use. `gpu_probe.py` and `train_probe.py` document the smaller hardware checks used before the full run.

## Next experiments

- Record model version, package versions, generated token counts, and stopping reasons for repeatable comparisons.
- Add held-out questions, including Vue tasks and a few outside Vue, to measure gains and retained capabilities.
- Expand and improve training examples based on observed errors; keep evaluation answers out of training.
- Test longer examples within the hardware limit. Raw Vue documentation has **not** been fed into the model in this version.
- Compare additional training runs against the same untouched Qwen baseline, and explore retrieval separately later.
