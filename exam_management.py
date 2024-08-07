import sqlite3

# Function to create a new exam with transaction
def create_exam(exam_name, subject, teacher_id, date):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Insert the new exam
        cursor.execute("INSERT INTO exams (exam_name, subject, teacher_id, date) VALUES (?, ?, ?, ?)",
                       (exam_name, subject, teacher_id, date))
        
        # Commit transaction
        connection.commit()
        return "Exam created successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to update exam details with transaction
def update_exam(exam_id, exam_name, subject, teacher_id, date):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Update the exam details
        cursor.execute("UPDATE exams SET exam_name = ?, subject = ?, teacher_id = ?, date = ? WHERE exam_id = ?",
                       (exam_name, subject, teacher_id, date, exam_id))
        
        # Commit transaction
        connection.commit()
        return "Exam updated successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to delete an exam with transaction
def delete_exam(exam_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Delete the exam
        cursor.execute("DELETE FROM exams WHERE exam_id = ?", (exam_id,))
        
        # Commit transaction
        connection.commit()
        return "Exam deleted successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to fetch all exams
def fetch_all_exams():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()
    connection.close()

    return exams

# Function to fetch exam by ID
def fetch_exam_by_id(exam_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM exams WHERE exam_id = ?", (exam_id,))
    exam = cursor.fetchone()
    connection.close()

    return exam

# Function to search exams by subject, date, or teacher
def search_exams(subject=None, date=None, teacher_id=None):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()
    
    query = "SELECT * FROM exams WHERE 1=1"
    params = []
    
    if subject:
        query += " AND subject = ?"
        params.append(subject)
    
    if date:
        query += " AND date = ?"
        params.append(date)
    
    if teacher_id:
        query += " AND teacher_id = ?"
        params.append(teacher_id)
    
    cursor.execute(query, params)
    exams = cursor.fetchall()
    connection.close()

    return exams

# Function to create a view for upcoming exams
def create_upcoming_exams_view():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS upcoming_exams AS
    SELECT * FROM exams
    WHERE date >= DATE('now')
    ORDER BY date ASC
    ''')
    
    connection.commit()
    connection.close()

# Function to fetch data from the upcoming exams view
def fetch_upcoming_exams_view():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM upcoming_exams")
    exams = cursor.fetchall()
    connection.close()

    return exams

# Function to create a question for an exam with transaction
def create_question(exam_id, question_text, difficulty_level, correct_answer):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Insert the new question
        cursor.execute("INSERT INTO questions (exam_id, question_text, difficulty_level, correct_answer) VALUES (?, ?, ?, ?)",
                       (exam_id, question_text, difficulty_level, correct_answer))
        
        # Commit transaction
        connection.commit()
        return "Question created successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to update a question with transaction
def update_question(question_id, question_text, difficulty_level, correct_answer):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Update the question
        cursor.execute("UPDATE questions SET question_text = ?, difficulty_level = ?, correct_answer = ? WHERE question_id = ?",
                       (question_text, difficulty_level, correct_answer, question_id))
        
        # Commit transaction
        connection.commit()
        return "Question updated successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to delete a question with transaction
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

# Function to fetch all questions for an exam
def fetch_questions_by_exam_id(exam_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions WHERE exam_id = ?", (exam_id,))
    questions = cursor.fetchall()
    connection.close()

    return questions

# Function to create a view for exam details
def create_exam_details_view():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS exam_details AS
    SELECT exams.exam_id, exams.exam_name, exams.subject, users.username AS teacher_name, exams.date
    FROM exams
    JOIN users ON exams.teacher_id = users.user_id
    ''')
    
    connection.commit()
    connection.close()

# Function to fetch data from the exam details view
def fetch_exam_details_view():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM exam_details")
    exams = cursor.fetchall()
    connection.close()

    return exams

# Function to create a trigger for automatic result update after exam creation
def create_result_update_trigger():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_exam_creation
    AFTER INSERT ON exams
    BEGIN
        INSERT INTO results (enrollment_id, score)
        SELECT enrollments.enrollment_id, 0
        FROM enrollments
        WHERE enrollments.exam_id = NEW.exam_id;
    END;
    ''')
    
    connection.commit()
    connection.close()

# Initial setup for creating views and triggers
def setup_views_and_triggers():
    create_upcoming_exams_view()
    create_exam_details_view()
    create_result_update_trigger()

if __name__ == '__main__':
    # Initial setup for views and triggers
    setup_views_and_triggers()
    print("Exam management setup complete with views and triggers.")
