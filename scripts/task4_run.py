# scripts/task4_run.py
import sys
import os

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # folder containing task4_run.py
sys.path.append(PROJECT_ROOT)

import os
import pandas as pd
from scripts.config import PROCESSED_DATA
from scripts.eda_helpers import (
    merge_sentiment_and_cleaned,
    top_n_words,
    plot_reviews_per_app,
    plot_rating_distribution,
    plot_sentiment_distribution,
    plot_wordcloud_from_text,
    plot_top_keywords_bar,
    save_plot
)

# -----------------------------
# Step 1: Load Data
# -----------------------------
cleaned_path = os.path.join(PROCESSED_DATA, "cleaned_reviews.csv")
sentiment_path = os.path.join(PROCESSED_DATA, "sentiment_results.csv")

if not os.path.exists(cleaned_path) or not os.path.exists(sentiment_path):
    raise FileNotFoundError("Cleaned reviews or sentiment file missing!")

cleaned = pd.read_csv(cleaned_path)
sentiment = pd.read_csv(sentiment_path)

merged = merge_sentiment_and_cleaned(cleaned, sentiment)

# -----------------------------
# Step 2: Separate by sentiment
# -----------------------------
positive = merged[merged["sentiment"]=="positive"]
negative = merged[merged["sentiment"]=="negative"]

stopwords = set([
    "app","bank","payment","payments","service","mobile","update","please",
    "cbe","bankofabyssinia","boa","amole"
])

# -----------------------------
# Step 3: Insights - Drivers & Pain Points
# -----------------------------
insights = {}
for bank in merged['app'].unique():
    pos_words = top_n_words(positive[positive['app']==bank]['clean_content'], n=10, stopwords=stopwords)
    neg_words = top_n_words(negative[negative['app']==bank]['clean_content'], n=10, stopwords=stopwords)
    insights[bank] = {"drivers": pos_words, "pain_points": neg_words}

# -----------------------------
# Step 4: Visualization
# -----------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "task4_plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Sentiment distribution per bank
plot_sentiment_distribution(merged, save_path=os.path.join(OUTPUT_DIR, "sentiment_distribution.png"))

# 2. Rating distribution per bank
plot_rating_distribution(merged, save_path=os.path.join(OUTPUT_DIR, "rating_distribution.png"))

# 3. WordCloud & Top Keywords for Negative Reviews
for bank in merged['app'].unique():
    neg_reviews = negative[negative['app']==bank]
    if not neg_reviews.empty:
        # WordCloud
        plot_wordcloud_from_text(neg_reviews["clean_content"], save_path=os.path.join(OUTPUT_DIR, f"wordcloud_negative_{bank}.png"))
        # Top keywords bar chart
        pairs = top_n_words(neg_reviews['clean_content'], n=20, stopwords=stopwords)
        if pairs:
            plot_top_keywords_bar(
                pairs, 
                title=f"Top negative keywords - {bank}",
                save_path=os.path.join(OUTPUT_DIR, f"top_keywords_negative_{bank}.png")
            )

# -----------------------------
# Step 5: Generate Summary Table
# -----------------------------
summary = []
for bank, data in insights.items():
    driver_list = [w for w, c in data['drivers'][:3]]
    pain_list = [w for w, c in data['pain_points'][:3]]
    summary.append({
        "Bank": bank,
        "Top Drivers (Positive)": ", ".join(driver_list),
        "Top Pain Points (Negative)": ", ".join(pain_list)
    })

summary_df = pd.DataFrame(summary)
summary_path = os.path.join(PROCESSED_DATA, "task4_insights_summary.csv")
summary_df.to_csv(summary_path, index=False)

# -----------------------------
# Step 6: Print Summary for Report
# -----------------------------
print("\n--- Task 4 Insights Summary ---\n")
print(summary_df.to_string(index=False))
print(f"\nPlots saved in: {OUTPUT_DIR}")
print(f"Summary CSV saved in: {summary_path}")