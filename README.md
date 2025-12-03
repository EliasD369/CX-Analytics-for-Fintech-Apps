# CX Analytics for Fintech Apps Project

## Project Overview

This project demonstrates end-to-end data engineering, analysis, and visualization of mobile banking app reviews in Ethiopia. The goal is to collect, preprocess, analyze, and store user reviews from Google Play for three banks: CBE, BOA, and Amole, providing actionable insights into user experience and sentiment.

## Project Scope

Data Sources: Google Play Store reviews for CBE, BOA, Amole.
Tasks Completed:

  1. **Task 1: Scraping and preprocessing of raw review data.
  2. Task 2: Exploratory Data Analysis (EDA) and sentiment labeling.
  3. Task 3: Storage of cleaned reviews in **PostgreSQL**.


## Folder Structure

CX_Analytics_for_Fintech_Apps/
│
├─ scripts/                 # Python scripts
│   ├─ scraper.py            # Scrapes reviews from Google Play
│   ├─ preprocessing.py      # Cleans and preprocesses reviews
│   ├─ config.py             # Project paths and app constants
│   ├─ eda_helpers.py        # Helper functions for EDA
│   └─ run_eda.py            # Runs EDA and generates plots
│
├─ data/
│   ├─ raw/                  # Raw scraped review CSVs
│   └─ processed/            # Cleaned review CSVs
│
├─ reports/
│   └─ plots/                # EDA visualizations
│
├─ .env                      # PostgreSQL credentials (local, not committed)
├─ export_schema.sh          # Script to export PostgreSQL DB schema and data
├─ README.md                 # Project documentation

## Task Details

### Task 1 – Data Collection & Preprocessing

Goal: Scrape reviews from Google Play and clean text for analysis.
Key Steps:

  * Scrape reviews using `scraper.py`.
  * Store raw reviews in `data/raw/`.
  * Clean text (remove links, punctuation, normalize whitespace) using `preprocessing.py`.
  * Save processed data to `data/processed/cleaned_reviews.csv`.
Tools Used: Python, `pandas`, `re`, `google-play-scraper`.

### Task 2 – Exploratory Data Analysis & Sentiment

Goal: Understand review distribution and sentiment trends.
Key Steps:

  Merge cleaned reviews with sentiment labels.
  Generate plots:

    * Reviews per app
    * Rating distribution
    * Average rating over time
    * Sentiment distribution
    * Wordclouds and top negative keywords
  Save plots in `reports/plots/`.
Tools Used: Python, `pandas`, `seaborn`, `matplotlib`, `wordcloud`.

### Task 3 – PostgreSQL Integration

Goal: Store processed reviews in a relational database for persistent storage.
Key Steps:

   Create PostgreSQL database `bank_reviews`.
   Define tables:

    * `banks(bank_id, bank_name, app_name)`
    * `reviews(review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)`
  * Insert cleaned reviews via Python using `psycopg2`.
  * Export DB schema using `export_schema.sh`.
Tools Used:** PostgreSQL, Python (`psycopg2`), `.env` for credentials.


## Key Metrics & Insights

Total Reviews Collected: >1,000
Cleaned & Preprocessed Reviews:** Saved in `data/processed/cleaned_reviews.csv`
EDA Outputs: Distribution of reviews, average ratings, sentiment trends visualized.
Database: Populated `reviews` and `banks` tables with cleaned review data.
Initial KPIs: Ready for further sentiment analysis and thematic extraction.
