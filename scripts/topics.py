"""
topics.py
Topic modeling using LDA for clean review text.
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from config import PROCESSED_DATA, TOPIC_DATA

def run_topic_modeling(num_topics=5):
    input_file = f"{PROCESSED_DATA}/cleaned_reviews.csv"
    df = pd.read_csv(input_file)

    text_data = df["clean_content"].astype(str)

    vectorizer = CountVectorizer(
        max_features=3000,
        stop_words="english"
    )
    X = vectorizer.fit_transform(text_data)

    lda = LatentDirichletAllocation(
        n_components=num_topics,
        learning_method="batch",
        random_state=42
    )

    lda_matrix = lda.fit_transform(X)
    df["topic"] = lda_matrix.argmax(axis=1)

    df.to_csv(TOPIC_DATA, index=False)
    print(f"Topics extracted → {TOPIC_DATA}")


if __name__ == "__main__":
    run_topic_modeling()
    print("Topic modeling completed.")
