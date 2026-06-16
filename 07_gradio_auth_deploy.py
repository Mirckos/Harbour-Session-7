import os

import gradio as gr
from dotenv import load_dotenv


load_dotenv()


def env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def reverse(text: str) -> str:
    """Return the input string reversed."""
    return text[::-1]


demo = gr.Interface(
    fn=reverse,
    inputs=gr.Textbox(label="Text", placeholder="Try a private demo"),
    outputs=gr.Textbox(label="Reversed"),
    title="Password-Protected Reverse",
    description="Credentials come from DEMO_USER and DEMO_PASSWORD.",
    api_name="reverse",
)


if __name__ == "__main__":
    username = os.getenv("DEMO_USER", "admin")
    password = os.getenv("DEMO_PASSWORD", "demo-password-change-me")

    demo.launch(
        auth=(username, password),
        inbrowser=True,
        share=env_flag("GRADIO_SHARE"),
        theme=gr.themes.Soft(),
    )
