# Dataset generation

## Basic principle

The dataset generation is made of two steps:

1. Generate detailed captions from human-written code.
2. From those captions, use a LM to generate code.

The final dataset thus contains both human and AI-generated code for similar
tasks, thus reducing potential bias.

The dataset used for the generation is code-parrot/github-code-clean, which
contains roughly 1TB of code from Github on permissive licenses, including 50GB
of Python.

For obvious reasons, we only use a limited subset of the Python dataset.

## How-to

The entry-point is the `main.py` file which contains two subcommands. You can
run `./main.py --help` for more information.

> [!NOTE]
> To use the Gemini API which is mandatory for captions generation, you need to
> set the environment variable `GOOGLE_API_KEY` to an appropiate value.

### Captions generation

``` sh
./main.py gen-captions
```

Options:
- `--output-path` (*optional*): the path in which to save the dataset.
- `--sample-size` (*optional*): the number of files to select from the shuffled dataset.

### Code generation

> [!WARNING]
> The code generation assumes that the captions have been generated beforehand

``` sh
./main.py gen-code
```

Options:
- `--captioned-path` (*optional*): the path from which to load the captioned dataset. 
- `--output-path` (*optional*): the path in which to save the dataset.
- `--model` (*optional*): name of the model from the hugging face hub. If omitted, use the Gemini API (recommended).
- `--sample-size`: the number of files to select from the captioned dataset.
