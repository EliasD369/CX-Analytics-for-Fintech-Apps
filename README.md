CX Analytics for Fintech Apps  Project
Project Overview

This project focuses on analyzing mobile banking app reviews in Ethiopia to derive actionable insights for app improvement. It simulates a real-world data engineering and analytics workflow, including data scraping, preprocessing, sentiment analysis, storage in PostgreSQL, and insights visualization.

Banks Analyzed:

CBE

BOA

Amole

Tech Stack:

Python 3.10+

Pandas, NumPy, Seaborn, Matplotlib, WordCloud

PostgreSQL (psycopg2 or SQLAlchemy for data insertion)

Project Structure
CX_Analytics_for_Fintech_Apps/
│
├─ data/
│   ├─ raw/                  # Scraped raw reviews
│   └─ processed/            # Cleaned and processed data + CSV summaries
│
├─ scripts/
│   ├─ config.py             # Project configuration & folder paths
│   ├─ scraper.py            # Scrapes reviews from app stores
│   ├─ preprocessing.py      # Cleans and processes raw reviews
│   ├─ preprocessing_EDA.ipynb # Notebook for initial EDA
│   ├─ eda_helpers.py        # Helper functions for EDA & visualization
│   ├─ run_eda.py            # Run all EDA plots automatically
│   └─ task4_run.py          # Task 4: Insights & recommendations generation
│
├─ reports/
│   └─ task4_plots/          # Generated plots for Task 4 insights
│
├─ .env                      # PostgreSQL credentials (ignored in Git)
├─ export_schema.sh          # Shell script to export PostgreSQL schema/data
├─ README.md                 # Project documentation



Run Task 4 insights

python scripts/task4_run.py

Notes & Best Practices

Use .env for PostgreSQL credentials; never commit secrets.

Ensure data/raw and data/processed exist before running scripts.

Stopwords filtered to avoid common meaningless words.

Reports and plots are versioned via Git for reproducibility.

Git Branch Workflow

main → Stable code

task-1 → Scraping & preprocessing

task-2 → Sentiment analysis

task-3 → PostgreSQL storage

task-4 → Insights & recommendations

Pull Requests used to merge completed tasks into main.