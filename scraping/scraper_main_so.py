from scraping.so_scraper import fetch_stackoverflow_questions, fetch_answers_for_questions
from utils.clean import clean_html
from database.db import init_db, insert_question, insert_answer


# Initialize the database and tables
init_db()

# Fetch questions
print("🔍 Fetching questions...")
questions = fetch_stackoverflow_questions(tag="python", pages=100, pagesize=100)

# Clean and insert questions
question_ids = []
for q in questions:
    q['title'] = clean_html(q['title'])
    q['body'] = clean_html(q['body'])
    insert_question(q)
    question_ids.append(q['question_id'])

print(f"✅ {len(questions)} questions fetched and stored.")

# Fetch answers for the collected question IDs
print(f"🔍 Fetching answers for {len(question_ids)} questions...")
answers = fetch_answers_for_questions(question_ids)

# Clean and insert answers
for a in answers:
    a['body'] = clean_html(a['body'])
    insert_answer(a)

print(f"✅ {len(answers)} answers fetched and stored in the database.")
