from typing import Callable

import pandas as pd
from datasets import Dataset, IterableDataset

from generate_prompt import generate_caption, generate_code_from_caption
from llm import infer, load_model


def build_generated_captions(
    code_dataset: IterableDataset,
    infer: Callable[[str], str],
) -> IterableDataset:
    """
    Add a column 'caption' to a dataset containing at least columns 'code' and 'language'.
    """

    def add_caption(data: dict[str, str]) -> dict[str, str]:
        prompt = generate_caption(data)
        caption = infer(prompt=prompt)
        data["caption"] = caption

        return data

    captioned = code_dataset.map(add_caption)

    return captioned


def build_generated_codes(
    captioned_dataset: Dataset,
    infer: Callable[[str], str],
    batch_size: int | None = None,
) -> Dataset:
    """
    Add a column 'generated_code' to a dataset containing at least columns 'caption', 'size' and 'language'.
    """

    def add_generated_code(
        data: dict[str, str | list[str]]
    ) -> dict[str, str | list[str]]:
        if batch_size is None:
            prompt = generate_code_from_caption(data)
        else:
            mapped = {key: data[key] for key in ("caption", "size", "language")}
            flattened = pd.DataFrame(mapped).to_dict(orient="records")
            prompt = [generate_code_from_caption(item) for item in flattened]

        code = infer(prompt=prompt)
        data["generated_code"] = code

        return data

    generated = captioned_dataset.map(
        add_generated_code,
        load_from_cache_file=True,
        batched=batch_size is not None,
        batch_size=batch_size,
    )

    return generated
