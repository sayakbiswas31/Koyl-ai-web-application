from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch
import os

MODEL_DIR = "data/model_weights"

def prepare_dataset(documents):
    # Filter out documents with empty or invalid abstracts
    valid_documents = [doc for doc in documents if doc.get("abstract") and isinstance(doc["abstract"], str) and len(doc["abstract"].strip()) > 0]
    
    # Generate texts and labels
    texts = [doc["abstract"] for doc in valid_documents]
    labels = [1 if "allergy" in doc["title"].lower() or "allergy" in doc["abstract"].lower() else 0 for doc in valid_documents]
    
    return texts, labels, valid_documents

def train_model(documents):
    if not documents:
        print("No documents to train on.")
        return None, None
    
    # Prepare dataset
    texts, labels, valid_documents = prepare_dataset(documents)
    
    if len(texts) < 2:
        print(f"Insufficient valid documents for training. Found {len(texts)} valid documents.")
        return None, None
    
    # Initialize tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)
    
    # Tokenize data
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors="pt")
    
    # Create dataset
    class PubMedDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels
        
        def __getitem__(self, idx):
            item = {key: val[idx].clone().detach() for key, val in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item
        
        def __len__(self):
            return len(self.labels)
    
    # Ensure consistent lengths
    if len(texts) != len(labels):
        print(f"Mismatch in texts ({len(texts)}) and labels ({len(labels)}).")
        return None, None
    
    # Split data
    train_idx, val_idx = train_test_split(
        list(range(len(texts))), test_size=0.2, random_state=42
    )
    
    train_encodings = {key: val[train_idx] for key, val in encodings.items()}
    val_encodings = {key: val[val_idx] for key, val in encodings.items()}
    train_labels = [labels[i] for i in train_idx]
    val_labels = [labels[i] for i in val_idx]
    
    train_dataset = PubMedDataset(train_encodings, train_labels)
    val_dataset = PubMedDataset(val_encodings, val_labels)
    
    # Training arguments
   
    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )
    
    # Train
    trainer.train()
    
    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)
    
    return model, tokenizer

def load_trained_model():
    if not os.path.exists(MODEL_DIR):
        return None, None
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_DIR)
    return model, tokenizer
