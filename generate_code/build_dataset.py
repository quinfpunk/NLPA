from datasets import Dataset
from generate_prompt import generate_prompt

def build_generated_captions(code_dataset, llm, hugging_faces=True):
    code_dataset["caption"] = []
    prompt_generator = generate_caption(code_dataset, f"Knowing the program language is {lang} generate a detailed caption for this program: \n{codes}")
    for i in code_dataset:
        prom = prompt_generator.next()
        answer = llm(prompt)
        code_dataset["caption"].append(answer)
    return code_dataset if not(hugging_faces) else Dataset.from_dict(code_dataset)

def build_generated_codes(code_dataset, llm, hugging_faces=True):
    code_dataset["generated_code"] = []
    prompt_generator = generate_prompt(code_dataset, f"Generate a program in {lang} from this caption:\n {caption}"
)
    for i in code_dataset:
        prom = prompt_generator.next()
        answer = llm(prompt)
        code_dataset["generated_code"].append(answer)
    return code_dataset if not(hugging_faces) else Dataset.from_dict(code_dataset)

def build_generated_dataset(code_dataset, llm, hugging_faces=True):
    code_dataset["generated_answer"] = []
    prompt_generator = generate_prompt(code_dataset, f"Knowing the code is in {lang}: \n{question}\ncontext:\n{code}")
    for i in code_dataset:
        prom = prompt_generator.next()
        answer = llm(prompt)
        code_dataset["generated_answer"].append(answer)
    return code_dataset if not(hugging_faces) else Dataset.from_dict(code_dataset)

