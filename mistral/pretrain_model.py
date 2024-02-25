import sys
import datasets
from transformers import AutoModelForSequenceClassification,\
                         AutoModelForCausalLM,\
                         AutoTokenizer

from models import train_model
from data_preprocessing import tokenize_function

model_url = "microsoft/phi-2"
dataset = datasets.load_from_disk("./staqc_man_python_codegen_all_configs.hf")

tokenizer = AutoTokenizer.from_pretrained(model_url)
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

print("Preprocessing dataset")

train_dataset = dataset['train'].map(lambda x: tokenize_function(tokenizer, x))
eval_dataset = dataset['test'].map(lambda x: tokenize_function(tokenizer, x))

print(f"Pretraining '{model_url}' model")

model = AutoModelForCausalLM.from_pretrained(model_url)

train_model(model, train_dataset, eval_dataset)

