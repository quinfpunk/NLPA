from pathlib import Path

_PROMPTS_DIR = Path("prompts")
CAPTION_TEMPLATE = _PROMPTS_DIR / "caption.txt"
CODE_TEMPLATE = _PROMPTS_DIR / "code.txt"

CAPTIONED_DS_PATH = Path("dataset/captions")
FINAL_DS_PATH = Path("dataset/final")

SAMPLE_SIZE = 10_000
MAX_CODE_LENGTH = 10_000
