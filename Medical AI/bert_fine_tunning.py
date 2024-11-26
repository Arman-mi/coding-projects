from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments, DistilBertTokenizerFast
import torch
from sklearn.model_selection import train_test_split
import pandas as pd

# Load your dataset
data = pd.read_excel("Model_train.xlsx")

# Split into training and validation sets
train_texts, val_texts, train_labels, val_labels = train_test_split(data['questions'], data['intent'], test_size=0.1)

# Create a label-to-id mapping
label_to_id = {label: idx for idx, label in enumerate(data['intent'].unique())}
train_labels = train_labels.map(label_to_id).tolist()
val_labels = val_labels.map(label_to_id).tolist()

# Tokenize the text data
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True)
val_encodings = tokenizer(val_texts.tolist(), truncation=True, padding=True)

# Create a Dataset class
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

# Create datasets
train_dataset = IntentDataset(train_encodings, train_labels)
val_dataset = IntentDataset(val_encodings, val_labels)

# Load pre-trained DistilBERT model with the number of intents as output labels
num_intents = len(data['intent'].unique())
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=num_intents)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',            # Directory to save model and logs
    evaluation_strategy="epoch",      # Evaluate the model every epoch
    learning_rate=1e-5,               # Fine-tuning learning rate
    per_device_train_batch_size=10,   # Batch size for training
    per_device_eval_batch_size= 10,    # Batch size for evaluation
    num_train_epochs= 8,               # Number of epochs to train
    weight_decay=0.01,                # Weight decay for regularization
    logging_dir='./logs',             # Directory to save logs
    save_total_limit=1,               # Save only the most recent checkpoint
)

# Define the Trainer
trainer = Trainer(
    model=model,                         # The model to train
    args=training_args,                  # Training arguments
    train_dataset=train_dataset,         # Training data
    eval_dataset=val_dataset             # Validation data
)

# Fine-tune the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained("fine_tuned_distilbert")
tokenizer.save_pretrained("fine_tuned_distilbert")

print("Fine-tuning complete. Model and tokenizer saved to 'fine_tuned_distilbert'.")

test_results = trainer.evaluate(val_dataset)

print(f"Test Results: {test_results}")
