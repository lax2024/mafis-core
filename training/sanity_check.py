import pandas as pd

df = pd.read_csv("data/news_dataset.csv")

label_map = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

df["label_name"] = df["label"].map(label_map)

print("\nLabel distribution:")
print(df["label_name"].value_counts())

print("\nRandom samples:\n")

for label in ["positive", "neutral", "negative"]:
    print(f"\n===== {label.upper()} =====")

    samples = df[df["label_name"] == label].sample(10)

    for _, row in samples.iterrows():
        print(row["Title"])
        print(row["Description"])
        print("-" * 60)