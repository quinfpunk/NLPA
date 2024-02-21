from load_dataset import load_dataset

def generate_caption(json_dataset, num_prompt : int, prompt_template: fstring):
    codes = json_dataset["code"]
    lang = json_dataset["language"]
    # Write the code associated with this caption
    prompt = f"Knowing the program language is {lang} generate a detailed caption for this program: \n{codes}"
    return prompt

def generate_code_from_caption(json_dataset, num_prompt : int, prompt_template: fstring):
    caption = json_dataset["caption"]
    codes = json_dataset["code"]
    lang = json_dataset["language"]
    # Write the code associated with this caption
    prompt = f"Generate a program in {lang} from this caption:\n {caption}"
    return prompt

def generate_prompt(json_dataset, num_prompt : int, prompt_template: fstring):
    questions = json_dataset["question"]
    codes = json_dataset["code"]
    lang = json_dataset["lang"]
    prompt_list = []
    for i in range(num_prompt):
        # Write the code associated with this caption
        prompt = f"Knowing the code is in {lang}: \n{questions[i]}\ncontext:\n{codes[i]}"
        prompt_list.append(prompt)
    return prompt_list
#json = load_dataset("python", "dev", 20)
#prompts = generate_prompt(json, 1)
#print(prompts[0])
