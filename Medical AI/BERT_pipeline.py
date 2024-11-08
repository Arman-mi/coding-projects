# from transformers import pipeline
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments, DistilBertTokenizerFast
import torch
from sklearn.model_selection import train_test_split
import pandas as pd

from transformers import DistilBertForSequenceClassification

# classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1", framework="pt")

# intent_labels = [
#     "Check for PPE precautions", "Ask about blood pressure", "Ask about heart rate", "Ask about respiratory rate",
#     "Ask about pulse", "Identify system", "Final Diagnosis", "Check scene safety",
#     "Check number of patients", "Request additional EMS", "Consider spine stabilization",
#     "Ask about chief complaint", "Check patient responsiveness"
# ]
# def classify_intent(question):
#     """Use BERT to classify the intent of a question."""
#     result = classifier(question, intent_labels)
#     return result['labels'][0]
data = pd.read_excel("Model_train.xlsx")

train_texts, val_texts, train_labels, val_labels = train_test_split(data['questions'], data['intent'], test_size=0.1)
label_to_id = {label: idx for idx, label in enumerate(data['intent'].unique())}
train_labels = train_labels.map(label_to_id).tolist()
val_labels = val_labels.map(label_to_id).tolist()

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True)
val_encodings = tokenizer(val_texts.tolist(), truncation=True, padding=True)



class IntentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)
    
train_dataset = IntentDataset(train_encodings, train_labels)
val_dataset = IntentDataset(val_encodings, val_labels)

num_intents = len(data['intent'].unique())  # Automatically detect number of unique intents
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=num_intents)

training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Fine-tune model
trainer.train()