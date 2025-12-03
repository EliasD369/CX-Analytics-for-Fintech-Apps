# scripts/eda_helpers.py
import os
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

sns.set(style="whitegrid")

import sys
import os

# allow relative imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.config import PROCESSED_DATA

def load_cleaned_reviews(fname="cleaned_reviews.csv"):
    path = os.path.join(PROCESSED_DATA, fname)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path)

def load_sentiment_results(fname="sentiment_results.csv"):
    path = os.path.join(PROCESSED_DATA, fname)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path)

def merge_sentiment_and_cleaned(cleaned_df, sentiment_df, on_cols=None):
    # default merge by content and date if no review_id
    if on_cols is None:
        # prefer unique id if present
        if "review_id" in cleaned_df.columns and "review_id" in sentiment_df.columns:
            on_cols = ["review_id"]
        else:
            # fallback to content + date (not ideal but works)
            on_cols = ["clean_content", "at"] if "at" in cleaned_df.columns else ["clean_content"]
    merged = cleaned_df.merge(sentiment_df, how="left", left_on=on_cols, right_on=on_cols, suffixes=("", "_s"))
    return merged

def save_plot(fig, path, dpi=150):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, bbox_inches="tight", dpi=dpi)

def plot_reviews_per_app(df, save_path=None):
    fig, ax = plt.subplots(figsize=(7,4))
    order = df['app'].value_counts().index
    sns.countplot(data=df, x='app', order=order, ax=ax)
    ax.set_title("Number of Reviews per App")
    ax.set_xlabel("App")
    ax.set_ylabel("Review Count")
    if save_path:
        save_plot(fig, save_path)
    return fig

def plot_rating_distribution(df, save_path=None):
    fig, axes = plt.subplots(1,3, figsize=(14,4), sharey=True)
    apps = df['app'].unique()
    for i, app in enumerate(apps):
        sns.countplot(data=df[df['app']==app], x='score', ax=axes[i])
        axes[i].set_title(f"{app} - Rating Distribution")
        axes[i].set_xlabel("Rating")
        axes[i].set_ylabel("Count")
    plt.tight_layout()
    if save_path:
        save_plot(fig, save_path)
    return fig

def plot_avg_rating_over_time(df, time_col="at", save_path=None, freq="M"):
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    monthly = df.groupby([pd.Grouper(key=time_col, freq=freq), "app"])['score'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=monthly, x=time_col, y='score', hue='app', marker="o", ax=ax)
    ax.set_title("Average Rating Over Time (monthly)")
    ax.set_ylabel("Average Rating")
    if save_path:
        save_plot(fig, save_path)
    return fig

def plot_sentiment_distribution(df, sentiment_col="sentiment", save_path=None):
    fig, ax = plt.subplots(figsize=(7,4))
    sns.countplot(data=df, x=sentiment_col, hue='app', dodge=True, ax=ax)
    ax.set_title("Sentiment Distribution by App")
    ax.set_ylabel("Count")
    if save_path:
        save_plot(fig, save_path)
    return fig

def top_n_words(series, n=30, stopwords=None):
    stopwords = stopwords or set()
    counter = Counter()
    for text in series.dropna().astype(str):
        for w in text.split():
            w = w.strip()
            if len(w) > 2 and w not in stopwords:
                counter[w] += 1
    return counter.most_common(n)

def plot_wordcloud_from_text(series, save_path=None):
    text = " ".join(series.dropna().astype(str).tolist())
    wc = WordCloud(width=1200, height=600, background_color="white", collocations=False).generate(text)
    fig, ax = plt.subplots(figsize=(12,6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    if save_path:
        save_plot(fig, save_path)
    return fig

def plot_top_keywords_bar(counter_pairs, title="Top keywords", save_path=None, top_n=20):
    words, counts = zip(*counter_pairs[:top_n])
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=list(counts), y=list(words), ax=ax)
    ax.set_title(title)
    if save_path:
        save_plot(fig, save_path)
    return fig