import sqlite3

DB_NAME = "stackoverflow.db"

# Initialize the database with tables
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY,
            title TEXT,
            body TEXT,
            tags TEXT,
            score INTEGER,
            creation_date INTEGER
        )
    """)

    # Create answers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            answer_id INTEGER PRIMARY KEY,
            question_id INTEGER,
            body TEXT,
            score INTEGER,
            is_accepted BOOLEAN,
            creation_date INTEGER,
            FOREIGN KEY (question_id) REFERENCES questions (question_id)
        )
    """)

    conn.commit()
    conn.close()

# Insert question into the database
def insert_question(question):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO questions (question_id, title, body, tags, score, creation_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        question.get("question_id"),
        question.get("title"),
        question.get("body"),
        ",".join(question.get("tags", [])),
        question.get("score", 0),
        question.get("creation_date")
    ))

    conn.commit()
    conn.close()

# Insert answer into the database
def insert_answer(answer):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO answers (answer_id, question_id, body, score, is_accepted, creation_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        answer.get("answer_id"),
        answer.get("question_id"),
        answer.get("body"),
        answer.get("score", 0),
        answer.get("is_accepted", False),
        answer.get("creation_date")
    ))

    conn.commit()
    conn.close()
