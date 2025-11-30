import os
import pandas as pd
from google_play_scraper import Sort, reviews

APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Amole": "com.dashen.dashensuperapp",
}

# Build correct save path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)
def scrape_reviews(app_name, app_id, count=400):
    print(f"\nScraping reviews for {app_name}...")

    result, _ = reviews(
        app_id,
        lang="en",
        country="et",
        sort=Sort.NEWEST,
        count=count,
    )

    df = pd.DataFrame(result)
    file_path = os.path.join(DATA_DIR, f"{app_name}_reviews.csv")
    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f"Saved → {file_path}")

def main():
    for app_name, app_id in APPS.items():
        scrape_reviews(app_name, app_id)

if __name__ == "__main__":
    main()
