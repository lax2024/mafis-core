import pandas as pd
import re


def clean_text(text):
    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\.{2,}", ".", text)

    text = text.replace('"', "")
    text = text.replace("'", "")

    text = text.strip()

    return text


# Load RAW dataset
df = pd.read_csv("data/raw_news.csv")

# Combine Title + Description
df["headline"] = (
    df["Title"].fillna("") + ". " + df["Description"].fillna("")
)

# Map numeric labels to text
label_map = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

df["label"] = df["label"].map(label_map)

# Clean text
df["headline"] = df["headline"].apply(clean_text)

# Keep only needed columns
df = df[["headline", "label"]]

# Remove duplicates + nulls
df = df.drop_duplicates()
df = df.dropna()

# Save processed dataset
df.to_csv("data/news_dataset.csv", index=False)

print("Dataset prepared successfully!")
print(df.head())
print("\nLabel counts:")
print(df["label"].value_counts())