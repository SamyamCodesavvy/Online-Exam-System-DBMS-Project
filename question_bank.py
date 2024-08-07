import sqlite3

# Function to add a question to the question bank with transaction
def add_question(exam_id, question_text, difficulty_level, correct_answer, marks):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Insert the new question
        cursor.execute("INSERT INTO questions (exam_id, question_text, difficulty_level, correct_answer, marks) VALUES (?, ?, ?, ?, ?)",
                       (exam_id, question_text, difficulty_level, correct_answer, marks))
        
        # Commit transaction
        connection.commit()
        return "Question added successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to update a question in the question bank with transaction
def update_question(question_id, exam_id, question_text, difficulty_level, correct_answer, marks):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Update the question
        cursor.execute("UPDATE questions SET exam_id = ?, question_text = ?, difficulty_level = ?, correct_answer = ?, marks = ? WHERE question_id = ?",
                       (exam_id, question_text, difficulty_level, correct_answer, marks, question_id))
        
        # Commit transaction
        connection.commit()
        return "Question updated successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to delete a question from the question bank with transaction
def delete_question(question_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Delete the question
        cursor.execute("DELETE FROM questions WHERE question_id = ?", (question_id,))
        
        # Commit transaction
        connection.commit()
        return "Question deleted successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to fetch all questions
def fetch_all_questions():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    connection.close()

    return questions

# Function to fetch questions by exam ID
def fetch_questions_by_exam_id(exam_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions WHERE exam_id = ?", (exam_id,))
    questions = cursor.fetchall()
    connection.close()

    return questions

# Function to search questions by various criteria
def search_questions(exam_id=None, difficulty_level=None):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    query = "SELECT * FROM questions WHERE 1=1"
    params = []
    
    if exam_id:
        query += " AND exam_id = ?"
        params.append(exam_id)
    
    if difficulty_level:
        query += " AND difficulty_level = ?"
        params.append(difficulty_level)
    
    cursor.execute(query, params)
    questions = cursor.fetchall()
    connection.close()

    return questions

# Function to create a view for question bank
def create_question_bank_view():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS question_bank AS
    SELECT questions.question_id, exams.exam_name, questions.question_text, questions.difficulty_level, questions.correct_answer, questions.marks
    FROM questions
    JOIN exams ON questions.exam_id = exams.exam_id
    ''')
    
    connection.commit()
    connection.close()

# Function to fetch data from the question bank view
def fetch_question_bank_view():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM question_bank")
    question_bank = cursor.fetchall()
    connection.close()

    return question_bank

# Function to randomize questions for an exam
def randomize_questions(exam_id, limit=10):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT * FROM questions 
    WHERE exam_id = ? 
    ORDER BY RANDOM() 
    LIMIT ?
    ''', (exam_id, limit))
    
    randomized_questions = cursor.fetchall()
    connection.close()

    return randomized_questions

# Function to create a trigger for logging question updates
def create_question_update_log_trigger():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_question_update
    AFTER UPDATE ON questions
    BEGIN
        INSERT INTO question_logs (question_id, old_question_text, new_question_text, change_time)
        VALUES (OLD.question_id, OLD.question_text, NEW.question_text, DATETIME('now'));
    END;
    ''')
    
    connection.commit()
    connection.close()

# Function to create a question_logs table (required for the trigger)
def create_question_logs_table():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS question_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        old_question_text TEXT,
        new_question_text TEXT,
        change_time TEXT,
        FOREIGN KEY(question_id) REFERENCES questions(question_id)
    )
    ''')
    
    connection.commit()
    connection.close()

# Initial setup for creating views and triggers
def setup_views_and_triggers():
    create_question_bank_view()
    create_question_logs_table()
    create_question_update_log_trigger()

if __name__ == '__main__':
    # Initial setup for views and triggers
    setup_views_and_triggers()
    print("Question bank management setup complete with views and triggers.")
