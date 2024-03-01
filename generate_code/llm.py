import os
import time

import google.generativeai as genai
import torch
from google.api_core.exceptions import GoogleAPIError
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils import debounce


def load_model(model_name: str) -> tuple:
    if torch.cuda.is_available():
        torch.set_default_device("cuda")
    elif torch.backends.mps.is_available():
        torch.set_default_device("mps")

    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype="auto", trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        padding_side="left",
    )
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})

    return model, tokenizer


def infer(model, tokenizer, prompt: list[str], max_length: int = 50) -> list[str]:
    tokenized = tokenizer(prompt, return_tensors="pt", padding=True)
    output = model.generate(
        **tokenized,
        max_new_tokens=max_length,
        pad_token_id=tokenizer.pad_token_id,
    )
    return tokenizer.batch_decode(output)


@debounce(timeout=60, max_calls=60, safety_net=True)
def gemini_infer(prompt: str):
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")
    retry_count = 0

    response: str | None = None
    while retry_count < 3:
        try:
            response = model.generate_content(prompt).text
        except (GoogleAPIError, ValueError):
            retry_count += 1
            time.sleep(0.1)
        else:
            break

    return response if response is not None else ""


if __name__ == "__main__":
    resp = gemini_infer("Hello, world!")
    print(resp.text)
