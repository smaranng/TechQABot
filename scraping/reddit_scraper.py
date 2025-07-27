import praw
import sqlite3
import time

# --- Initialize Reddit API ---
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="YOUR_USER_NAME"
)

# --- Connect to SQLite ---
conn = sqlite3.connect("techqa.db")
cur = conn.cursor()

# --- Create Tables ---
cur.execute('''
    CREATE TABLE IF NOT EXISTS questions_reddit (
        question_id TEXT PRIMARY KEY,
        title TEXT,
        body TEXT,
        tags TEXT,
        score INTEGER,
        creation_date INTEGER,
        source_url TEXT
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS answers_reddit (
        answer_id TEXT PRIMARY KEY,
        question_id TEXT,
        body TEXT,
        score INTEGER,
        creation_date INTEGER,
        FOREIGN KEY (question_id) REFERENCES questions_reddit (question_id)
    )
''')

conn.commit()

# --- List of Subreddits to Scrape ---
subreddits_to_scrape = [
    "Python",
    "learnpython",
    "datascience",
    "MachineLearning",
    "opencv",
    "learnprogramming",
    "computervision",
    "mlquestions"
]

# --- Scrape Reddit ---
for subreddit_name in subreddits_to_scrape:
    subreddit = reddit.subreddit(subreddit_name)
    print(f"📥 Scraping: r/{subreddit_name}")

    for submission in subreddit.top(limit=50):  # More coverage, from "top" posts
        if submission.stickied or submission.score < 3:
            continue

        submission.comments.replace_more(limit=0)

        top_comments = [
            c for c in submission.comments
            if len(c.body.strip()) > 50 and c.score >= 1
        ]

        if not top_comments:
            continue

        # Insert question
        qid = submission.id
        title = submission.title
        body = submission.selftext
        tags = subreddit_name
        score = submission.score
        created = int(submission.created_utc)
        url = f"https://www.reddit.com{submission.permalink}"

        cur.execute('''
            INSERT OR IGNORE INTO questions_reddit 
            (question_id, title, body, tags, score, creation_date, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (qid, title, body, tags, score, created, url))

        # Insert answers
        for comment in top_comments:
            aid = comment.id
            atext = comment.body.strip()
            ascore = comment.score
            acreated = int(comment.created_utc)

            cur.execute('''
                INSERT OR IGNORE INTO answers_reddit
                (answer_id, question_id, body, score, creation_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (aid, qid, atext, ascore, acreated))

        time.sleep(1)  # Respect rate limits

# --- Finalize ---
conn.commit()
conn.close()
print("✅ All subreddits scraped and saved to techqa.db")
