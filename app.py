import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
import openai

###################################
# 1) Database Initialization
###################################
DB_PATH = 'keywords.db'

def init_db():
    """Initialize the database and create the keywords table if it doesn’t exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL UNIQUE,
            business_problem TEXT NOT NULL,
            industry TEXT,
            context TEXT,
            solution TEXT
        )
    ''')
    conn.commit()
    conn.close()

###################################
# 2) Flask App Setup
###################################
app = Flask(__name__)

# Set your OpenAI API key from environment or fallback
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Initialize DB on startup
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
    return conn

# Predefined schema/prompt template for ChatGPT

PROMPT_TEMPLATE = """
You are an expert interviewer evaluating a set of corporate case-study inputs. 
Here is the data provided:

- Keyword: {keyword}
- Business Problem: {business_problem}
- Industry: {industry}
- Context: {context}
- Proposed Solution: {solution}

Task:
1. Summarize the main points of the data.
2. Point out any potential pitfalls or concerns.
3. Suggest one or two follow-up questions to gauge deeper insights.
4. Create a case study combining those keywords
5. Provide a top consultant-level solution to this case study

Answer concisely in bullet points.
"""

###################################
# 3) Routes
###################################

@app.route('/')
def index():
    """Renders main page and lists all entries in the keywords table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM keywords')
    keywords_list = cursor.fetchall()
    conn.close()
    return render_template('index.html', keywords=keywords_list)

@app.route('/add', methods=['POST'])
def add_keyword():
    """Adds a new keyword/business_problem record to the database."""
    keyword = request.form.get('keyword')
    business_problem = request.form.get('business_problem')
    industry = request.form.get('industry', '')
    context = request.form.get('context', '')
    solution = request.form.get('solution', '')

    if keyword and business_problem:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO keywords (keyword, business_problem, industry, context, solution)
                   VALUES (?, ?, ?, ?, ?)''',
                (keyword, business_problem, industry, context, solution)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # Keyword already exists or constraint is violated
            pass
        conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:keyword_id>', methods=['POST'])
def edit_keyword(keyword_id):
    """Updates an existing record in the keywords table."""
    new_keyword = request.form.get('keyword')
    new_business_problem = request.form.get('business_problem')
    new_industry = request.form.get('industry', '')
    new_context = request.form.get('context', '')
    new_solution = request.form.get('solution', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE keywords
        SET keyword = ?, business_problem = ?, industry = ?, context = ?, solution = ?
        WHERE id = ?
    ''',
    (new_keyword, new_business_problem, new_industry, new_context, new_solution, keyword_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:keyword_id>', methods=['GET'])
def delete_keyword(keyword_id):
    """Deletes a record from the keywords table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM keywords WHERE id = ?', (keyword_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/runChatGPTPipeline', methods=['GET'])
def run_chatgpt_pipeline():
    """
    1. Fetch all rows from 'keywords' table.
    2. For each row, build a prompt and call ChatGPT.
    3. Return the responses as JSON.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keywords")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        prompt = PROMPT_TEMPLATE.format(
            keyword=row['keyword'],
            business_problem=row['business_problem'],
            industry=row['industry'],
            context=row['context'],
            solution=row['solution']
        )
        
        response_text = call_chatgpt(prompt)

        result_item = {
            "id": row['id'],
            "keyword": row['keyword'],
            "business_problem": row['business_problem'],
            "industry": row['industry'],
            "context": row['context'],
            "solution": row['solution'],
            "chatgpt_response": response_text.strip()
        }
        results.append(result_item)

    return jsonify(results)

###################################
# 4) Helper Function to Call ChatGPT
###################################
def call_chatgpt(prompt_text):
    """Sends the prompt to OpenAI and returns the model's response text."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert interviewer evaluating a set of corporate case-study inputs."
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return f"Error: {str(e)}"

###################################
# 5) Main Entry Point
###################################
if __name__ == '__main__':
    app.run(debug=True)
