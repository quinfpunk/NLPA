def tokenize_function(tokenizer, examples):
    return tokenizer(examples["text"], padding="longest", truncation=True)
