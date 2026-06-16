import os

import gradio as gr


def env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def greet(name: str) -> str:
    clean_name = name.strip() or "there"
    return f"Hello, {clean_name}! Your Gradio demo is running."


demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="Name", placeholder="Ada"),
    outputs=gr.Textbox(label="Greeting"),
    title="Gradio Hello Demo",
    description="Enter your name to receive a greeting.",
    examples=["Ada", "Harbour.Space"],
    api_name="greet",
)


if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        share=env_flag("GRADIO_SHARE"),
    )
