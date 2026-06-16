import os

import gradio as gr

visitor_count = 0


def env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def echo(message: str, history: list[dict[str, str]], request: gr.Request):
    """Reverse the input, tag it with a counter and session id, and update history."""
    global visitor_count
    if not message.strip():
        return history, history, ""

    visitor_count += 1
    session_id = (request.session_hash or "no-session")[:8]
    response = f"[{visitor_count}/{session_id}] {message[::-1]}"
    updated = [
        *history,
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]
    return updated, updated, ""


def clear_chat():
    return [], []


with gr.Blocks(title="Queue & State Demo") as demo:
    gr.Markdown("### Queue, global state, and per-session `gr.State`")

    chat_history = gr.State([])

    with gr.Row():
        inp = gr.Textbox(label="Your message", placeholder="Type and press Enter")
        btn = gr.Button("Send", variant="primary")
        clear = gr.Button("Clear")

    out = gr.Chatbot(label="History", height=360, buttons=["copy"])

    btn.click(
        echo,
        inputs=[inp, chat_history],
        outputs=[out, chat_history, inp],
        concurrency_limit=3,
    )
    inp.submit(
        echo,
        inputs=[inp, chat_history],
        outputs=[out, chat_history, inp],
        concurrency_limit=3,
    )
    clear.click(clear_chat, outputs=[out, chat_history], queue=False)

    demo.queue(max_size=20, default_concurrency_limit=3)


if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        share=env_flag("GRADIO_SHARE"),
        max_threads=20,
        theme=gr.themes.Soft(),
    )
