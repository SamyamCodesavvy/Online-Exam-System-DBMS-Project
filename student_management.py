import sqlite3
from utils import get_db_connection

# Function to enroll a student in an exam with transaction
def enroll_student(student_id, exam_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        # Check if the student is already enrolled in the exam
        cursor.execute("SELECT * FROM enrollments WHERE student_id = ? AND exam_id = ?", (student_id, exam_id))
        if cursor.fetchone():
            connection.rollback()
            return "Student already enrolled in this exam"

        # Enroll the student in the exam
        cursor.execute("INSERT INTO enrollments (student_id, exam_id) VALUES (?, ?)", (student_id, exam_id))
        
        # Commit transaction
        connection.commit()
        return "Student enrolled successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to track student performance and results
def track_student_performance(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
    SELECT 
        exams.exam_name, 
        exams.subject, 
        results.score, 
        (results.score * 100.0 / (SELECT SUM(marks) FROM questions WHERE exam_id = exams.exam_id)) AS percentage, 
        (SELECT MAX(score) FROM results WHERE enrollment_id IN (SELECT enrollment_id FROM enrollments WHERE exam_id = exams.exam_id)) AS highest_score
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    WHERE enrollments.student_id = ?
    GROUP BY exams.exam_name, exams.subject, results.score
    ''', (student_id,))
    
    performance = cursor.fetchall()
    connection.close()
    
    return performance

# Function to fetch all enrolled students for an exam
def fetch_students_by_exam_id(exam_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT users.user_id, users.username
    FROM enrollments
    JOIN users ON enrollments.student_id = users.user_id
    WHERE enrollments.exam_id = ?
    ''', (exam_id,))
    
    students = cursor.fetchall()
    connection.close()

    return students

# Function to store student answers
def store_student_answer(enrollment_id, question_id, answer):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    try:
        # Begin transaction
        connection.execute('BEGIN')

        cursor.execute("INSERT INTO submissions (enrollment_id, question_id, answer) VALUES (?, ?, ?)",
                       (enrollment_id, question_id, answer))
        
        # Commit transaction
        connection.commit()
        return "Answer submitted successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Function to create a view for student performance history
def create_student_performance_view():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS student_performance AS
    SELECT users.user_id, users.username, exams.exam_name, exams.subject, results.score
    FROM users
    JOIN enrollments ON users.user_id = enrollments.student_id
    JOIN results ON enrollments.enrollment_id = results.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    ''')
    
    connection.commit()
    connection.close()

# Function to fetch data from the student performance view
def fetch_student_performance_view(student_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM student_performance WHERE user_id = ?", (student_id,))
    performance = cursor.fetchall()
    connection.close()

    return performance

# Function to generate a report on student performance and exam results
def generate_performance_report():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT 
        exams.exam_name, 
        exams.subject, 
        AVG(results.score) AS average_score, 
        SUM(CASE WHEN results.score * 100.0 / (SELECT SUM(marks) FROM questions WHERE exam_id = exams.exam_id) >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(results.score) AS pass_rate
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    GROUP BY exams.exam_id
    ''')

    report = cursor.fetchall()
    connection.close()

    return report

# Function to calculate aggregate question difficulty statistics
def calculate_question_difficulty_statistics():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT difficulty_level, COUNT(*) AS question_count
    FROM questions
    GROUP BY difficulty_level
    ''')
    
    statistics = cursor.fetchall()
    connection.close()

    return statistics

# Function to create a trigger for notifying students of exam schedules
def create_exam_schedule_notification_trigger():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_exam_scheduling
    AFTER INSERT ON exams
    BEGIN
        INSERT INTO notifications (student_id, message)
        SELECT enrollments.student_id, 'You have an upcoming exam: ' || NEW.exam_name || ' on ' || NEW.date
        FROM enrollments
        WHERE enrollments.exam_id = NEW.exam_id;
    END;
    ''')
    
    connection.commit()
    connection.close()

# Function to create a notifications table (required for the trigger)
def create_notifications_table():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        message TEXT,
        FOREIGN KEY(student_id) REFERENCES users(user_id)
    )
    ''')
    
    connection.commit()
    connection.close()

# Initial setup for creating views and triggers
def setup_views_and_triggers():
    create_student_performance_view()
    create_notifications_table()
    create_exam_schedule_notification_trigger()

if __name__ == '__main__':
    # Initial setup for views and triggers
    setup_views_and_triggers()
    print("Student management setup complete with views and triggers.")
