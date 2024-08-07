import sqlite3
from hashlib import sha256

def get_db_connection():
    return sqlite3.connect('online_exam.db')

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin'))
    )
    ''')

    # Create Exams table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exams (
        exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_name TEXT NOT NULL,
        subject TEXT NOT NULL,
        teacher_id INTEGER,
        date TEXT NOT NULL,
        FOREIGN KEY(teacher_id) REFERENCES users(user_id)
    )
    ''')

    # Create Questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER,
        question_text TEXT NOT NULL,
        difficulty_level TEXT NOT NULL CHECK(difficulty_level IN ('easy', 'medium', 'hard')),
        correct_answer TEXT NOT NULL,
        marks INTEGER NOT NULL,
        FOREIGN KEY(exam_id) REFERENCES exams(exam_id)
    )
    ''')

    # Create Enrollments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        exam_id INTEGER,
        FOREIGN KEY(student_id) REFERENCES users(user_id),
        FOREIGN KEY(exam_id) REFERENCES exams(exam_id)
    )
    ''')

    # Create Results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrollment_id INTEGER,
        score INTEGER,
        FOREIGN KEY(enrollment_id) REFERENCES enrollments(enrollment_id)
    )
    ''')

    # Create Notifications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_read INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    # Create Submissions table (updated)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        exam_id INTEGER,
        question_id INTEGER,
        answer TEXT,
        FOREIGN KEY(student_id) REFERENCES users(user_id),
        FOREIGN KEY(exam_id) REFERENCES exams(exam_id),
        FOREIGN KEY(question_id) REFERENCES questions(question_id)
    )
    ''')

    # Create Question Logs table
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

    # Check if the 'marks' column exists, if not, add it
    cursor.execute("PRAGMA table_info(questions)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'marks' not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN marks INTEGER")

    connection.commit()
    connection.close()

def insert_sample_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', ?, 'admin')", (hash_password('adminpass'),))
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('teacher1', ?, 'teacher')", (hash_password('teacherpass'),))
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('student1', ?, 'student')", (hash_password('studentpass'),))
    
    cursor.execute("INSERT INTO exams (exam_name, subject, teacher_id, date) VALUES ('Math Exam', 'Math', 2, '2023-10-01')")
    cursor.execute("INSERT INTO exams (exam_name, subject, teacher_id, date) VALUES ('Science Exam', 'Science', 2, '2023-11-01')")
    
    cursor.execute("INSERT INTO questions (exam_id, question_text, difficulty_level, correct_answer, marks) VALUES (1, 'What is 2+2?', 'easy', '4', 1)")
    cursor.execute("INSERT INTO questions (exam_id, question_text, difficulty_level, correct_answer, marks) VALUES (1, 'What is 3+5?', 'easy', '8', 1)")
    cursor.execute("INSERT INTO questions (exam_id, question_text, difficulty_level, correct_answer, marks) VALUES (2, 'What is H2O?', 'medium', 'Water', 2)")
    
    cursor.execute("INSERT INTO enrollments (student_id, exam_id) VALUES (3, 1)")
    cursor.execute("INSERT INTO enrollments (student_id, exam_id) VALUES (3, 2)")
    
    cursor.execute("INSERT INTO results (enrollment_id, score) VALUES (1, 100)")
    cursor.execute("INSERT INTO results (enrollment_id, score) VALUES (2, 90)")
    
    connection.commit()
    connection.close()

def setup_views_and_triggers():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS user_roles AS
    SELECT user_id, username, role FROM users
    ''')

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS upcoming_exams AS
    SELECT * FROM exams
    WHERE date >= DATE('now')
    ORDER BY date ASC
    ''')

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS exam_details AS
    SELECT exams.exam_id, exams.exam_name, exams.subject, users.username AS teacher_name, exams.date
    FROM exams
    JOIN users ON exams.teacher_id = users.user_id
    ''')

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS student_performance_history AS
    SELECT students.username AS student_name, exams.exam_name, exams.subject, results.score
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    JOIN users AS students ON enrollments.student_id = students.user_id
    ''')

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS exam_result_statistics AS
    SELECT exams.exam_name, AVG(results.score) AS average_score, 
    SUM(CASE WHEN results.score >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(results.score) AS pass_rate
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    GROUP BY exams.exam_id
    ''')

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS question_bank AS
    SELECT questions.question_id, exams.exam_name, questions.question_text, questions.difficulty_level, questions.correct_answer, questions.marks
    FROM questions
    JOIN exams ON questions.exam_id = exams.exam_id
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_user_registration
    AFTER INSERT ON users
    BEGIN
        INSERT INTO enrollments (student_id, exam_id)
        VALUES (NEW.user_id, (SELECT exam_id FROM exams ORDER BY date LIMIT 1));
    END;
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_question_update
    AFTER UPDATE ON questions
    BEGIN
        INSERT INTO question_logs (question_id, old_question_text, new_question_text, change_time)
        VALUES (OLD.question_id, OLD.question_text, NEW.question_text, DATETIME('now'));
    END;
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_new_exam
    AFTER INSERT ON exams
    BEGIN
        INSERT INTO notifications (user_id, message)
        SELECT enrollments.student_id, 'A new exam "' || NEW.exam_name || '" has been scheduled on ' || NEW.date || '.'
        FROM enrollments
        WHERE enrollments.exam_id = NEW.exam_id;
    END;
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_exam_result
    AFTER INSERT ON results
    BEGIN
        INSERT INTO notifications (user_id, message)
        SELECT enrollments.student_id, 'Your result for the exam "' || exams.exam_name || '" has been published. Your score is ' || NEW.score || '.'
        FROM enrollments
        JOIN exams ON enrollments.exam_id = exams.exam_id
        WHERE enrollments.enrollment_id = NEW.enrollment_id;
    END;
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_student_enrollment
    AFTER INSERT ON enrollments
    BEGIN
        INSERT INTO notifications (user_id, message)
        SELECT exams.teacher_id, 'A new student has enrolled in your exam "' || exams.exam_name || '".'
        FROM exams
        WHERE exams.exam_id = NEW.exam_id;
    END;
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_exam_submission
    AFTER INSERT ON submissions
    BEGIN
        INSERT INTO results (enrollment_id, score)
        SELECT NEW.enrollment_id, 
        SUM(CASE WHEN submissions.answer = questions.correct_answer THEN 1 ELSE 0 END) * 100.0 / COUNT(questions.question_id) AS score
        FROM submissions
        JOIN questions ON submissions.question_id = questions.question_id
        WHERE submissions.enrollment_id = NEW.enrollment_id;
    END;
    ''')

    connection.commit()
    connection.close()

def initial_setup():
    create_tables()
    insert_sample_data()
    setup_views_and_triggers()

if __name__ == '__main__':
    initial_setup()
    print("Database setup complete with tables, sample data, views, and triggers.")
