from transformers import AutoModelForCausalLM, AutoTokenizer 

def load_model():
    model = AutoModelForCausalLM\
            .from_pretrained("gpt2")

    tokenizer = AutoTokenizer\
            .from_pretrained("gpt2")

    return model, tokenizer

def infer(model, tokenizer, prompt):
    tokenized = tokenizer(prompt, return_tensors='pt')
    output = model(**tokenized)
    return tokenizer.decode(model.generate(**tokenized)[0])

if __name__ == "__main__":
    model, tokenizer = load_model()
    print(infer(model, tokenizer, "How are you"))
