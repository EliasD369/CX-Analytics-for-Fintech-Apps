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

<<<<<<< task-4
└─ requirements.txt          # Python dependencies

Task Summary
Task 1: Scraping & Preprocessing

Scraped reviews for CBE, BOA, and Amole using scraper.py.

Cleaned and processed data using preprocessing.py:

Lowercased text

Removed links and non-alphanumeric characters

Dropped empty reviews

Added clean_content column

Initial EDA performed via preprocessing_EDA.ipynb.

Output:

data/processed/cleaned_reviews.csv

Review counts per app visualized

Rating distributions analyzed

Task 2: Sentiment Analysis

Performed sentiment scoring (positive/negative) for each review.

Merged sentiment results with cleaned reviews.

Prepared for Task 4 insights extraction.

Output:

data/processed/sentiment_results.csv

Merged dataset ready for insights generation

Task 3: PostgreSQL Storage

Designed relational database bank_reviews with two tables:

Banks Table

Column	Type	Description
bank_id	SERIAL PK	Unique ID for bank
bank_name	VARCHAR	Full bank name
app_name	VARCHAR	Mobile app name

Reviews Table

Column	Type	Description
review_id	SERIAL PK	Unique review ID
bank_id	INT FK	Linked bank ID
review_text	TEXT	Raw review text
rating	INT	Review rating (1–5)
review_date	DATE	Review posted date
sentiment_label	VARCHAR	Positive/Negative
sentiment_score	FLOAT	Sentiment confidence/score
source	VARCHAR	Data source (app store)

Data inserted into PostgreSQL using Python (psycopg2).

Verified data integrity with counts and averages.

SQL dump available via export_schema.sh.

Output:

400 reviews inserted successfully

Schema & data ready for analytics

Task 4: Insights & Recommendations

Generated insights from merged review & sentiment dataset.

Drivers (Positive) and Pain Points (Negative) identified per bank:

Bank	Top Drivers (Positive)	Top Pain Points (Negative)
CBE	good, the, and	the, and, not
BOA	good, the, and	the, and, this
Amole	the, and, good	the, and, not

Visualizations generated (saved to reports/task4_plots/):

Sentiment distribution by bank

Rating distributions

Negative reviews WordClouds

Top negative keywords per bank

Recommendations (based on keyword analysis & sentiment trends):

Improve app stability to reduce crashes

Enhance navigation and user experience

Add feature requests based on common negative keywords

How to Run

Install dependencies

pip install -r requirements.txt


Scrape reviews

python scripts/scraper.py


Preprocess reviews

python scripts/preprocessing.py


Run EDA & generate plots

python scripts/run_eda.py
=======
>>>>>>> main


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
