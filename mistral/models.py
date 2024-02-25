from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import Trainer, TrainingArguments
import evaluate
import numpy as np

metric = evaluate.load('accuracy')

def compute_accuracy(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    acc = metric.compute(predictions=predictions, references=labels)
    return acc

def train_model(model, train_dataset, eval_dataset, cm=None):
    args = TrainingArguments(output_dir="test_trainer",
                             evaluation_strategy="epoch",
                             num_train_epochs = 3,
                             per_device_train_batch_size=batch_size,
                             save_strategy='epoch')

    trainer = Trainer(model=model,
                      args=args,
                      train_dataset=train_dataset,
                      eval_dataset=eval_dataset,
                      compute_metrics=compute_metrics if cm is None else cm)

    train_history = trainer.train()
    return train_history, model
