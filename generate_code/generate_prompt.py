from load_dataset import load_dataset

# f"Knowing the program language is {lang} generate a detailed caption for this program: \n{codes}"
def generate_caption(json_dataset, prompt_template):
    codes = json_dataset["generated_code"]
    lang = json_dataset["language"]
    for code, lang in zip(codes, langs):
        # Write the code associated with this caption
        prompt = prompt_template.format(lang, code)
        yield prompt

# f"Generate a program in {lang} from this caption:\n {caption}"
def generate_code_from_caption(json_dataset, prompt_template):
    captions = json_dataset["caption"]
    langs = json_dataset["language"]
    for caption, lang in zip(captions, langs):
        # Write the code associated with this caption
        prompt = prompt_template.format(lang, caption)
        yield prompt

# f"Knowing the code is in {lang}: \n{question}\ncontext:\n{code}"
def generate_prompt(json_dataset, prompt_template):
    questions = json_dataset["question"]
    codes = json_dataset["generated_code"]
    langs = json_dataset["lang"]
    for question, code, lang in zip(questions, codes, langs):
        # Write the code associated with this caption
        prompt = prompt_template.format(lang, question, code)
        yield prompt

#res = generate_prompt({"code" : ["things"], "question" : ["rnvirn ?"], "lang": ["fr"]}, "Knowing the code is in {}: \n{}\ncontext:\n{}")
#for i in res:
#    print(i)
#res = generate_prompt({"caption" : ["rnvirn ?"], "lang": ["fr"]}, "Generate a program in {} from this caption:\n {}{}{}")
#for i in res:
#    print(i)
# json = load_dataset("python", "dev", 20)
# prompts = generate_prompt(json, 1)
# print(prompts[0])
