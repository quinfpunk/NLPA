import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model(model_name):
    torch.set_default_device("cuda")

    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    return model, tokenizer

def infer(model, tokenizer, prompt, max_length=200):
    tokenized = tokenizer(prompt, return_tensors='pt', return_attention_mask=False)
    output = model.generate(**tokenized, max_length=max_length)
    return tokenizer.batch_decode(outputs)[0]

if __name__ == "__main__":
    model, tokenizer = load_model("microsoft/phi-2")
    print(infer(model, tokenizer, "How are you"))
