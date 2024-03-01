import pathlib
from string import Template

from constants import CAPTION_TEMPLATE, CODE_TEMPLATE


def _generic_build_prompt(
    data: dict[str, str],
    template: Template | None,
    default_template_path: pathlib.Path,
) -> str:
    if template is None:
        with open(default_template_path, "r", encoding="utf-8") as file:
            raw_template = file.read()
        template = Template(raw_template)

    return template.safe_substitute(**data)


def generate_caption(data: dict[str, str], template: Template | None = None) -> str:
    """
    Generate a caption for a code snippet.

    :param data: A dictionnary containing at least the keys 'code' and 'language'.
    :param template: A template accepting the placeholders 'code' and 'language'.
    """

    return _generic_build_prompt(data, template, CAPTION_TEMPLATE)


def generate_code_from_caption(
    data: dict[str, str],
    template: Template | None = None,
) -> str:
    """
    Generate code from a given description

    :param data: A dictionnary containing at least the keys 'caption', 'size' and 'language'.
    :param template: A template accepting the placeholders 'caption', 'size' and 'language'.
    """

    return _generic_build_prompt(data, template, CODE_TEMPLATE)
