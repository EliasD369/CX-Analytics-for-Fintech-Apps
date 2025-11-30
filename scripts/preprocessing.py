import os
import pandas as pd
import re
from config import RAW_DATA, PROCESSED_DATA, APPS

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)          # remove links
    text = re.sub(r"[^a-z0-9\s]", " ", text)     # keep letters/numbers
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_reviews(app_name):
    file_path = os.path.join(RAW_DATA, f"{app_name}_reviews.csv")
    if not os.path.exists(file_path):
        print(f"⚠️ Missing file: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    df["app"] = app_name
    return df

def preprocess_app_reviews():
    all_data = []

    for app in APPS:
        df = load_reviews(app)
        if df is None:
            continue
        
        # Keep only important columns
        keep_cols = ["content", "score", "at", "app"]
        df = df[keep_cols]

        # Clean text
        df["clean_content"] = df["content"].apply(clean_text)

        # Drop empty rows
        df = df[df["clean_content"].str.len() > 0]

        all_data.append(df)

    # Merge all apps
    final_df = pd.concat(all_data, ignore_index=True)

    output_path = os.path.join(PROCESSED_DATA, "cleaned_reviews.csv")
    final_df.to_csv(output_path, index=False)

    print(f"Processed file saved → {output_path}")
    return final_df

def main():
    preprocess_app_reviews()

if __name__ == "__main__":
    main()