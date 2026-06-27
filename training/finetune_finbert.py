import os
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.utils.class_weight import compute_class_weight

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup
)

LABEL2ID = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}

ID2LABEL = {v: k for k, v in LABEL2ID.items()}


class Config:
    MODEL_NAME = "ProsusAI/finbert"
    MAX_LENGTH = 64
    BATCH_SIZE = 8
    EPOCHS = 5
    LR = 2e-5
    VAL_SIZE = 0.15
    CHECKPOINT_DIR = "./models/finbert_custom"
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class NewsDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=Config.MAX_LENGTH,
            return_tensors="pt"
        )

        item = {k: v.squeeze(0) for k, v in encoding.items()}
        item["labels"] = torch.tensor(self.labels[idx])

        return item


class Finetuner:
    def __init__(self):
        os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)

        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)

        print("Loading model...")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            Config.MODEL_NAME,
            num_labels=3,
            id2label=ID2LABEL,
            label2id=LABEL2ID
        ).to(Config.DEVICE)

        print("Model loaded successfully.")

    def prepare_data(self, csv_path):
        print("Loading dataset...")
        df = pd.read_csv(csv_path)

        print(f"Original rows: {len(df)}")

        # Use only 5000 rows for controlled training
        df = df.head(5000)

        print(f"Training rows selected: {len(df)}")

        print("Mapping labels...")
        df["label_id"] = df["label"].map(LABEL2ID)

        print("Splitting dataset...")
        train_df, val_df = train_test_split(
            df,
            test_size=Config.VAL_SIZE,
            stratify=df["label_id"],
            random_state=42
        )

        print(f"Train rows: {len(train_df)}")
        print(f"Validation rows: {len(val_df)}")

        print("Computing class weights...")
        class_weights = compute_class_weight(
            class_weight="balanced",
            classes=np.array([0, 1, 2]),
            y=train_df["label_id"]
        )

        self.loss_fn = nn.CrossEntropyLoss(
            weight=torch.tensor(class_weights, dtype=torch.float).to(Config.DEVICE)
        )

        print("Creating train loader...")
        self.train_loader = DataLoader(
            NewsDataset(
                train_df["headline"].tolist(),
                train_df["label_id"].tolist(),
                self.tokenizer
            ),
            batch_size=Config.BATCH_SIZE,
            shuffle=True
        )

        print("Creating validation loader...")
        self.val_loader = DataLoader(
            NewsDataset(
                val_df["headline"].tolist(),
                val_df["label_id"].tolist(),
                self.tokenizer
            ),
            batch_size=Config.BATCH_SIZE
        )

        print("Data preparation complete.")

    def train(self):
        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=Config.LR
        )

        total_steps = len(self.train_loader) * Config.EPOCHS

        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=0,
            num_training_steps=total_steps
        )

        best_f1 = 0

        print("Starting training...")

        for epoch in range(Config.EPOCHS):
            print(f"\n========== Epoch {epoch+1} ==========")

            self.model.train()
            total_loss = 0

            for i, batch in enumerate(self.train_loader):
                if i % 25 == 0:
                    print(f"Processing batch {i}/{len(self.train_loader)}")

                optimizer.zero_grad()

                batch = {k: v.to(Config.DEVICE) for k, v in batch.items()}
                labels = batch.pop("labels")

                outputs = self.model(**batch)
                loss = self.loss_fn(outputs.logits, labels)

                loss.backward()
                optimizer.step()
                scheduler.step()

                total_loss += loss.item()

            metrics = self.evaluate()

            print(f"\nEpoch {epoch+1} Results:")
            print(f"Train Loss: {total_loss / len(self.train_loader):.4f}")
            print(f"Val Accuracy: {metrics['accuracy']:.4f}")
            print(f"Val Precision: {metrics['precision']:.4f}")
            print(f"Val Recall: {metrics['recall']:.4f}")
            print(f"Val F1: {metrics['f1']:.4f}")

            if metrics["f1"] > best_f1:
                best_f1 = metrics["f1"]
                self.save_model()

    def evaluate(self):
        print("Running validation...")

        self.model.eval()

        preds = []
        labels_list = []

        with torch.no_grad():
            for batch in self.val_loader:
                batch = {k: v.to(Config.DEVICE) for k, v in batch.items()}
                labels = batch.pop("labels")

                outputs = self.model(**batch)
                predictions = torch.argmax(outputs.logits, dim=-1)

                preds.extend(predictions.cpu().numpy())
                labels_list.extend(labels.cpu().numpy())

        accuracy = accuracy_score(labels_list, preds)

        precision, recall, f1, _ = precision_recall_fscore_support(
            labels_list,
            preds,
            average="macro"
        )

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    def save_model(self):
        print("Saving best model...")

        self.model.save_pretrained(Config.CHECKPOINT_DIR)
        self.tokenizer.save_pretrained(Config.CHECKPOINT_DIR)

        with open(os.path.join(Config.CHECKPOINT_DIR, "label_map.json"), "w") as f:
            json.dump({
                "label2id": LABEL2ID,
                "id2label": ID2LABEL
            }, f)

        print("Saved best model successfully!")


if __name__ == "__main__":
    print(f"Using device: {Config.DEVICE}")

    trainer = Finetuner()
    trainer.prepare_data("data/news_dataset.csv")
    trainer.train()