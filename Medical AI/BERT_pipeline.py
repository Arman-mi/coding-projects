from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# Load the fine-tuned model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained("fine_tuned_distilbert")
tokenizer = DistilBertTokenizer.from_pretrained("fine_tuned_distilbert")

# Reverse the label-to-id mapping for inference
# Ensure the label_to_id dictionary from the training script is available
label_to_id = {
    "Check for PPE precautions": 0,
    "Ask about blood pressure": 1,
    "Ask about heart rate": 2,
    "Ask about respiratory rate": 3,
    "Ask about pulse": 4,
    "Identify system": 5,
    "Final Diagnosis": 6,
    "Check scene safety": 7,
    "Check number of patients": 8,
    "Request additional EMS": 9,
    "Consider spine stabilization": 10,
    "Ask about chief complaint": 11,
    "Check patient responsiveness": 12,
}
id_to_label = {v: k for k, v in label_to_id.items()}

def classify_intent(question):
    """Classify the intent of the given question using the fine-tuned model."""
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits).item()
    return id_to_label[predicted_class]
