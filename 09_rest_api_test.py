import asyncio
import os

from gradio_client import Client

URL = os.getenv("GRADIO_URL", "http://127.0.0.1:7860")
API_NAME = os.getenv("GRADIO_API_NAME", "/predict")
SYNC_TEXT = os.getenv("GRADIO_SYNC_TEXT", "This comment is rude and unfair.")
ASYNC_TEXT = os.getenv("GRADIO_ASYNC_TEXT", "Thanks for the clear explanation.")


def build_client() -> Client:
    return Client(URL)


async def run_async(client: Client) -> None:
    job = client.submit(ASYNC_TEXT, api_name=API_NAME)
    result = await asyncio.to_thread(job.result)
    print("Async response:", result)


if __name__ == "__main__":
    client = build_client()

    print(f"Connected to: {URL}")
    print(client.view_api())

    response = client.predict(SYNC_TEXT, api_name=API_NAME)
    print("Sync response:", response)

    asyncio.run(run_async(client))
