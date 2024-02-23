from abc import ABC, abstractmethod
from enum import Enum
from datasets import Dataset, DatasetDict, load_from_disk


class Configuration(Enum):
    # We keep the code unchanged
    C1 = 1
    # Remove import from own files
    C2 = 2
    # C2 + remove all comments
    C3 = 3
    # C3 + remove all import statements
    C4 = 4
    # C4 + use a reformatter to change the code style
    C5 = 5
    # C5 + remove all print statements
    C6 = 6


class Preprocessing(ABC):
    def __init__(self, dataset: DatasetDict):
        # Dataset should be at form:
        # Dataset({
        #   features: ['question_id', 'question', 'text', 'label'],
        #   num_rows: 3694
        # })
        self.dataset = dataset

        # Check features
        if "question_id" not in self.dataset["train"].features:
            raise ValueError("Feature question_id not found in dataset")
        if "label" not in self.dataset["train"].features:
            raise ValueError("Feature label not found in dataset")
        if "text" not in self.dataset["train"].features:
            raise ValueError("Feature question not found in dataset")

        # Sort to always have pair
        self.dataset["train"] = self.dataset["train"].sort(["question_id", "label"])
        self.dataset["test"] = self.dataset["test"].sort(["question_id", "label"])

    @abstractmethod
    def remove_imports_from_own_files(self, text: str) -> str:
        pass

    @abstractmethod
    def remove_comments(self, text: str) -> str:
        pass

    @abstractmethod
    def remove_imports(self, text: str) -> str:
        pass

    @abstractmethod
    def reformat_code(self, text: str) -> str:
        pass

    @abstractmethod
    def remove_print_statements(self, text: str) -> str:
        pass

    def get_configuration(self, configuration: Configuration) -> list[callable]:
        ret = []
        if configuration.value >= Configuration.C2.value:
            ret.append(self.remove_imports_from_own_files)
        if configuration.value >= Configuration.C3.value:
            ret.append(self.remove_comments)
        if configuration.value >= Configuration.C4.value:
            ret.append(self.remove_imports)
        if configuration.value >= Configuration.C5.value:
            ret.append(self.reformat_code)
        if configuration.value >= Configuration.C6.value:
            ret.append(self.remove_print_statements)
        return ret

    def preprocess(self, configuration: Configuration) -> Dataset:
        functions = self.get_configuration(configuration)
        print(functions)
        for f in functions:
            self.dataset["train"] = self.dataset["train"].map(
                lambda x: {"text": f(x)}, input_columns="text"
            )
            self.dataset["test"] = self.dataset["test"].map(
                lambda x: {"text": f(x)}, input_columns="text"
            )

        return self.dataset


if __name__ == "__main__":
    from datasets import load_from_disk
    import random
    from python.preprocess_python import PreprocessPython

    dataset = load_from_disk("tests/staqc_man_python_codegen.hf")

    print(dataset)
    preprocess = PreprocessPython(dataset)
    l = len(preprocess.dataset["train"])
    i = random.randint(0, l - 2)
    i = i + 1 if i % 2 == 0 else i

    def pretty_print(dataset: Dataset, i: int = 22):
        # Print question, then text and label
        print(dataset["question"][i])
        print("AI:" if dataset["label"][i] == 1 else "Human:")
        print(dataset["text"][i])
        print("AI:" if dataset["label"][i + 1] == 1 else "Human:")
        print(dataset["text"][i + 1])
        print()

    pretty_print(preprocess.dataset["train"])
    print("-" * 80)
    # Test C2
    dataset = preprocess.preprocess(Configuration.C6)
    # Print first 5 examples
    pretty_print(dataset["train"])
