import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data folders
RAW_DATA = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA = os.path.join(BASE_DIR, "data", "processed")

# Create folders if missing
os.makedirs(RAW_DATA, exist_ok=True)
os.makedirs(PROCESSED_DATA, exist_ok=True)

# Cleaned CSV from preprocessing.py
CLEANED_DATA = PROCESSED_DATA  # cleaned_reviews.csv lives here

# App names (must match scraper)
APPS = ["CBE", "BOA", "Amole"]

# Sentiment & Topic output files
SENTIMENT_DATA = os.path.join(PROCESSED_DATA, "sentiment_results.csv")
TOPIC_DATA = os.path.join(PROCESSED_DATA, "topic_results.csv")