import os

import gradio as gr
import torch
from transformers import pipeline

MODEL = "unitary/toxic-bert"
MAX_CHARS = 1_024


def env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


device = 0 if torch.cuda.is_available() else -1
classifier = pipeline(
    task="text-classification",
    model=MODEL,
    tokenizer=MODEL,
    top_k=None,
    function_to_apply="sigmoid",
    device=device,
)


def classify(text: str) -> dict[str, float]:
    """Return a mapping: {label: probability}."""
    clean_text = text.strip()[:MAX_CHARS]
    if not clean_text:
        return {"empty input": 1.0}

    raw_scores = classifier(clean_text)
    if raw_scores and isinstance(raw_scores[0], list):
        raw_scores = raw_scores[0]

    scores = {
        item["label"].replace("_", " "): round(float(item["score"]), 3)
        for item in raw_scores
    }
    return scores


demo = gr.Interface(
    fn=classify,
    inputs=gr.Textbox(
        lines=3,
        label="Text",
        placeholder="Paste a short comment...",
        max_lines=6,
    ),
    outputs=gr.Label(num_top_classes=6, label="Toxicity scores"),
    title="Text Toxicity Classifier (BERT)",
    description="Multi-label output from unitary/toxic-bert.",
    examples=[
        "Thanks for the clear explanation.",
        "This comment is rude and unfair.",
    ],
    api_name="predict",
    concurrency_limit=1,
)

demo.queue(max_size=25, default_concurrency_limit=1)


if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        share=env_flag("GRADIO_SHARE"),
        theme=gr.themes.Soft(),
    )
