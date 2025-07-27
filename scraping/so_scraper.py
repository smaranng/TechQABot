import requests
import time
from utils.clean import clean_html
from database.db import insert_question, insert_answer


API_KEY = "YOUR_API_KEY"

# Fetch questions from Stack Overflow
def fetch_stackoverflow_questions(tag="python", pages=100, pagesize=100):
    all_questions = []
    for page in range(1, pages + 1):
        print(f"📄 Fetching questions page {page}...")
        url = (
            f"https://api.stackexchange.com/2.3/questions?"
            f"order=desc&sort=votes&tagged={tag}&site=stackoverflow"
            f"&filter=withbody&page={page}&pagesize={pagesize}&key={API_KEY}"
        )
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Failed to fetch questions: {response.status_code}")
            break
        data = response.json()
        if "items" not in data:
            break
        for item in data["items"]:
            item["title"] = clean_html(item["title"])
            item["body"] = clean_html(item["body"])
            insert_question(item)
        all_questions.extend(data["items"])
        time.sleep(1.5)  # Respect rate limits
    return all_questions


# Fetch answers for given list of question IDs
def fetch_answers_for_questions(question_ids):
    all_answers = []
    batch_size = 100
    print(f"🔍 Fetching answers for {len(question_ids)} questions...")
    for i in range(0, len(question_ids), batch_size):
        ids = ";".join(map(str, question_ids[i:i + batch_size]))
        url = (
            f"https://api.stackexchange.com/2.3/questions/{ids}/answers?"
            f"order=desc&sort=votes&site=stackoverflow&filter=withbody"
            f"&pagesize=100&page=1&key={API_KEY}"
        )
        print(f"📡 Requesting: {url}")
        response = requests.get(url)
        print(f"🔢 Status: {response.status_code}")

        if response.status_code == 429:
            print("❌ Rate limit hit. Sleeping for 10 seconds...")
            time.sleep(10)
            continue

        try:
            data = response.json()
        except Exception as e:
            print("❌ Failed to parse JSON:", e)
            continue

        if "items" not in data:
            continue

        for ans in data["items"]:
            ans["body"] = clean_html(ans["body"])
            insert_answer(ans)
        all_answers.extend(data["items"])
        time.sleep(1.5)
    print(f"✅ {len(all_answers)} answers fetched.")
    return all_answers
