from load_dataset import load_dataset

def generate_prompt(json_dataset, num_prompt : int):
    questions = json_dataset["question"]
    codes = json_dataset["code"]
    lang = json_dataset["lang"]
    prompt_list = []
    for i in range(num_prompt):
        prompt = f"Knowing the code is in {lang}: \n{questions[i]}\ncontext:\n{codes[i]}"
        prompt_list.append(prompt)
    return prompt_list

#json = load_dataset("python", "dev", 20)
#prompts = generate_prompt(json, 1)
#print(prompts[0])
