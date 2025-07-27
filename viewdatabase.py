import sqlite3
import pandas as pd
from flask import Flask, render_template_string, request
from bs4 import BeautifulSoup
import html
import base64

app = Flask(__name__)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("assets/techqa_logo.png") 
stack_logo = get_base64_image("assets/stack.png")
reddit_logo = get_base64_image("assets/reddit.png")


TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>View Database - Tech QA Bot</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <!-- Font Awesome CDN -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            display: flex;
            min-height: 100vh;
        }
        .sidebar {
            position: sticky;
            top: 0;
            height: 100vh;
            width: 280px;
            background-color: #F0F0F0;
            padding: 30px 20px;
            color: white;
            flex-shrink: 0;
        }
        .sidebar h2 {
            font-size: 22px;
            margin-bottom: 30px;
            border-bottom: 1px solid #444;
            padding-bottom: 10px;
            color: black;
        }
        .sidebar a {
            color: black;
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
        }
        .content {
            flex-grow: 1;
            padding: 30px;
            background-color: #f4f4f4;
            overflow-x: auto;
            background-color: #fff;
        }
        .header {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }
        .header img {
            width: 160px;
            height: 160px;
            margin-right: 20px;
        }
        .header h1 {
            font-size: 50px;
            margin: 0;
        }
        h2 {
            font-size: 26px;
            margin-bottom: 20px;
        }
        form {
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        select {
            padding: 8px 12px;
            font-size: 14px;
            border-radius: 5px;
            border: 1px solid #ccc;
            background-color: white;
        }
        input[type="submit"] {
            padding: 8px 16px;
            font-size: 14px;
            border: none;
            border-radius: 5px;
            background-color: #007BFF;
            color: white;
            cursor: pointer;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            font-size: 14px;
            table-layout: auto;
            word-break: break-word;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            vertical-align: top;
            text-align: left;
        }
        th {
            background-color: #007BFF;
            color: white;
            white-space: nowrap;
        }
        td:nth-child(3) {
            max-width: 600px;
            width: 50%;
            white-space: normal;
        }
        td:last-child {
            white-space: nowrap;
            text-align: center;
            width: 70px;
        }
        a {
            color: #007BFF;
            text-decoration: none;
        }
                table tr:nth-child(even) {
            background-color: #e5e7eb;
        }
        table tr:nth-child(odd) {
            background-color: #f9fafb;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🧭 Navigation</h2>
        <a href="http://localhost:8501">⬅ Back to Chat Bot</a>
    </div>
    <div class="content">
        <div class="header">
            <img src="data:image/png;base64,{{ logo_base64 }}" alt="Logo">
            <h1>Tech QA Bot</h1>
        </div>
        <h2>📁 View Database</h2>
<form method="get" action="/database">
    <label for="source">Choose Source:</label>
    <select name="source" id="source">
        <option value="StackOverflow" {% if db_source == 'StackOverflow' %}selected{% endif %}>StackOverflow</option>
        <option value="Reddit" {% if db_source == 'Reddit' %}selected{% endif %}>Reddit</option>
    </select>
    <input type="submit" value="View">

    <label for="tag" style="margin-left: 20px;">
        <i class="fa-solid fa-filter" style="margin-right: 5px;"></i> Filter by Tag:
    </label>
    <select name="tag" id="tag">
        <option value="">-- All --</option>
        {% for tag in predefined_tags %}
            <option value="{{ tag }}" {% if tag == selected_tag %}selected{% endif %}>{{ tag }}</option>
        {% endfor %}
    </select>
    <input type="submit" value="Apply Filter"><br>
    <label for="search">
        <i class="fa-solid fa-magnifying-glass" style="margin-right: 5px;"></i> Search Question:
    </label>
    <input type="text" name="search" id="search" value="{{ search_query or '' }}" placeholder="e.g. pandas dataframe" style="padding: 6px; border-radius: 5px; width: 250px;">
    <input type="submit" value="Search">
</form>
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{{ platform_logo }}" alt="Platform Logo" style="width: 30px; height: 30px; margin-right: 10px;">
            <strong style="font-size: 36px;">{{ platform_label }}</strong>
        </div>
        {{ table | safe }}
    </div>
</body>
</html>
"""

def clean_answer(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = html.unescape(text)
    return text.replace("\n", "<br>").strip()

@app.route("/database")
def show_data():
    db_source = request.args.get("source", "StackOverflow")
    selected_tag = request.args.get("tag", "")
    search_query = request.args.get("search", "").strip()
    if db_source == "StackOverflow":
        db_path = "stackoverflow.db"
        question_table = "questions"
        answer_table = "answers"
        platform_logo = stack_logo
        platform_label = "Data from StackOverflow"
    else:
        db_path = "techqa.db"
        question_table = "questions_reddit"
        answer_table = "answers_reddit"
        platform_logo = reddit_logo
        platform_label = "Data from Reddit"

    # Define fixed tag list
    predefined_tags = [
        "python", "python,xml", "python,oop", "python,django", "python,python-itertools", "python,floating-point",
        "python,unicode", "python,string,sorting", "python,file", "python,variables,return", "python,syntax,namespaces,python-import", "python,html","python,graphics",
        "python,set","python,switch-statement","python,sql,database,random,sqlalchemy","opencv","computervision","datascience","MachineLearning"
    ]

    try:
        conn = sqlite3.connect(db_path)
        if selected_tag:
            query = f"""
                SELECT 
                    q.question_id AS Question_ID,
                    q.title AS Question,
                    a.body AS Answer,
                    a.score AS Score
                FROM 
                    {question_table} q
                JOIN 
                    {answer_table} a ON q.question_id = a.question_id
                WHERE q.tags LIKE ?
                ORDER BY q.question_id, a.score DESC;
            """
            df = pd.read_sql_query(query, conn, params=[f"%{selected_tag}%"])
        else:
            query = f"""
                SELECT 
                    q.question_id AS Question_ID,
                    q.title AS Question,
                    a.body AS Answer,
                    a.score AS Score
                FROM 
                    {question_table} q
                JOIN 
                    {answer_table} a ON q.question_id = a.question_id
                ORDER BY q.question_id, a.score DESC;
            """
            df = pd.read_sql_query(query, conn)
        conn.close()
        conn = sqlite3.connect(db_path)
        params = []
        conditions = []

        if selected_tag:
            conditions.append("q.tags LIKE ?")
            params.append(f"%{selected_tag}%")

        if search_query:
            conditions.append("q.title LIKE ?")
            params.append(f"%{search_query}%")

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        query = f"""
            SELECT 
                q.question_id AS Question_ID,
                q.title AS Question,
                a.body AS Answer,
                a.score AS Score
            FROM 
                {question_table} q
            JOIN 
                {answer_table} a ON q.question_id = a.question_id
            {where_clause}
            ORDER BY q.question_id, a.score DESC;
        """

        df = pd.read_sql_query(query, conn, params=params)

        # Links
        if db_source == "StackOverflow":
            df["Link"] = df["Question_ID"].apply(lambda qid: f'<a href="https://stackoverflow.com/q/{qid}" target="_blank">Link</a>')
        else:
            df["Link"] = df["Question_ID"].apply(lambda qid: f'<a href="https://www.reddit.com/comments/{qid}" target="_blank">Link</a>')

        df["Answer"] = df["Answer"].apply(clean_answer)
        html_table = df.to_html(escape=False, index=False)

    except Exception as e:
        html_table = f"<p style='color:red;'>❌ Error: {e}</p>"

    return render_template_string(
        TEMPLATE,
        table=html_table,
        db_source=db_source,
        logo_base64=logo_base64,
        platform_logo=platform_logo,
        platform_label=platform_label,
        predefined_tags=predefined_tags,
        selected_tag=selected_tag,
        search_query=search_query
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)