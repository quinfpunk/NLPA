from datasets import Dataset

def build_generated_dataset(code_dataset, llm, hugging_faces=True):
    prompts = generate_prompt(code_dataset, len(code_dataset))
    code_dataset["generated_answer"] = []
    for p in prompts:
        answer = llm(p)
        code_dataset["generated_answer"].append(answer)
    return code_dataset if not(hugging_faces) else Dataset.from_dict(code_dataset)

