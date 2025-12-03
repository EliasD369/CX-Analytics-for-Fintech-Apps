# scripts/run_eda.py
import os
from eda_helpers import (
    load_cleaned_reviews,
    load_sentiment_results,
    merge_sentiment_and_cleaned,
    plot_reviews_per_app,
    plot_rating_distribution,
    plot_avg_rating_over_time,
    plot_sentiment_distribution,
    plot_wordcloud_from_text,
    top_n_words,
    plot_top_keywords_bar,
    save_plot
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    cleaned = load_cleaned_reviews()
    sentiment = load_sentiment_results()

    merged = merge_sentiment_and_cleaned(cleaned, sentiment)

    # 1 - reviews per app
    plot_reviews_per_app(cleaned, save_path=os.path.join(OUTPUT_DIR, "reviews_per_app.png"))

    # 2 - rating distribution
    plot_rating_distribution(cleaned, save_path=os.path.join(OUTPUT_DIR, "rating_distribution.png"))

    # 3 - avg rating over time
    plot_avg_rating_over_time(cleaned, save_path=os.path.join(OUTPUT_DIR, "avg_rating_over_time.png"))

    # 4 - sentiment distribution
    plot_sentiment_distribution(merged, save_path=os.path.join(OUTPUT_DIR, "sentiment_distribution.png"))

    # 5 - wordcloud for negative reviews
    negative = merged[merged['sentiment']=="negative"]
    if not negative.empty:
        plot_wordcloud_from_text(negative["clean_content"], save_path=os.path.join(OUTPUT_DIR, "wordcloud_negative.png"))

    # 6 - top keywords per app (negative)
    stopwords = set(["app","bank","payment","payments","service","mobile","update","please"])
    for app in cleaned['app'].unique():
        neg = merged[(merged['app']==app) & (merged['sentiment']=="negative")]
        pairs = top_n_words(neg['clean_content'], n=40, stopwords=stopwords)
        if pairs:
            plot_top_keywords_bar(pairs, title=f"Top negative keywords - {app}", save_path=os.path.join(OUTPUT_DIR, f"top_keywords_negative_{app}.png"))

    print("EDA run complete. Plots saved to:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
