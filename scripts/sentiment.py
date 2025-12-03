import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from config import PROCESSED_DATA, SENTIMENT_DATA, APPS

nltk.download("vader_lexicon")

def run_sentiment():
    input_file = f"{PROCESSED_DATA}/cleaned_reviews.csv"
    df = pd.read_csv(input_file)

    sia = SentimentIntensityAnalyzer()
    df["compound"] = df["clean_content"].apply(lambda x: sia.polarity_scores(str(x))["compound"])

    df["sentiment"] = df["compound"].apply(
        lambda x: "positive" if x > 0.05 else ("negative" if x < -0.05 else "neutral")
    )

    df.to_csv(SENTIMENT_DATA, index=False)
    print(f"Sentiment completed → {SENTIMENT_DATA}")


if __name__ == "__main__":
    run_sentiment()