#!/usr/bin/env python3

import pathlib
from functools import partial
from typing import Optional

import click
from datasets import Dataset, IterableDataset, load_dataset

from build_dataset import build_generated_captions, build_generated_codes
from constants import *
from llm import gemini_infer, infer, load_model
from postprocess import cleanup


def _lazy_to_eager_dataset(dataset: IterableDataset) -> Dataset:
    def generate():
        yield from dataset

    return Dataset.from_generator(generate)


@click.group()
def cli():
    ...


@cli.command()
@click.option("--output-path", default="dataset/captions", type=pathlib.Path)
@click.option("--sample-size", default=SAMPLE_SIZE, type=int)
def gen_captions(output_path: pathlib.Path, sample_size: int):
    """Generate captions for code snippets using the Gemini API"""

    streamed = load_dataset(
        "codeparrot/github-code-clean",
        streaming=True,
        trust_remote_code=True,
        split="train",
    )

    # Lazy, in-memory filtering and shuffling to prevent unoptimized disk accesses
    sample = (
        streamed.filter(lambda row: row["language"] == "Python")
        .shuffle(seed=42)
        .take(sample_size)
    )

    captioned = build_generated_captions(sample, gemini_infer)

    dataset = _lazy_to_eager_dataset(captioned)
    dataset.save_to_disk(output_path)


@cli.command()
@click.option("--captioned-path", default=CAPTIONED_DS_PATH, type=pathlib.Path)
@click.option("--output-path", default=FINAL_DS_PATH, type=pathlib.Path)
@click.option("--model", default=None)
@click.option("--sample-size", default=SAMPLE_SIZE, type=int)
def gen_code(
    captioned_path: pathlib.Path,
    output_path: pathlib.Path,
    model: str | None,
    sample_size: int,
):
    """Generate code based on captions"""

    # This time, we can use an eager dataset that will efficiently perform memory mapping
    captioned = Dataset.load_from_disk(captioned_path)
    captioned = (
        captioned.select_columns(["code", "size", "caption", "language"])
        .select(range(sample_size))  # Gen on the whole dataset might be expensive
        .filter(lambda row: bool(row["caption"]))  # Remove rows with no caption
    )

    inference_function = gemini_infer
    batch_size = None  # Gemini does not support batched generation requests yet

    if model is not None:
        model, tokenizer = load_model(model)
        inference_function = partial(
            infer,
            model=model,
            tokenizer=tokenizer,
            max_length=MAX_CODE_LENGTH,
        )
        batch_size = 1  # Actually depends on the model
        # FIXME: Add this as a cli option

    generated = build_generated_codes(
        captioned,
        inference_function,
        batch_size=batch_size,
    )
    generated.save_to_disk(output_path)


@cli.command()
@click.option("--input-path", default=FINAL_DS_PATH)
@click.option("--output-path", default=CLEANED_DS_PATH)
def post_process(input_path: pathlib.Path, output_path: pathlib.Path):
    """Apply post-processing to the final dataset"""

    dataset = Dataset.load_from_disk(input_path)
    cleaned = cleanup(dataset)

    cleaned.to_parquet(output_path)


if __name__ == "__main__":
    cli()
