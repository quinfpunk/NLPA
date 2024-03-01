from preprocessing import Preprocessing
import re
from black import format_str, Mode


class PreprocessPython(Preprocessing):
    def remove_imports_from_own_files(self, text: str) -> str:
        # Pass, more specific for other languages
        return text

    def remove_comments(self, text: str) -> str:
        # Remove single line comments
        text = re.sub(r"(?m)^\s*#.*\n?", "", text)
        # Remove ending comments
        text = re.sub(r"\s*#.*", "", text)
        # Remove docstrings and multiline comments
        text = re.sub(r'(?s)(""".*?"""|\'\'\'.*?\'\'\').*\n', "", text)

        return text

    def remove_imports(self, text: str) -> str:
        # Remove import statements
        text = re.sub(r"import.*\n", "", text)
        text = re.sub(r"from.*\n", "", text)

        # Remove first line if it is empty
        text = re.sub(r"^\s*$\n", "", text)

        return text

    def reformat_code(self, text: str) -> str:
        try:
            return format_str(text, mode=Mode())
        except:
            return text

    def remove_print_statements(self, text: str) -> str:
        # Remove print statements
        return re.sub(r"print.*\n", "", text)
