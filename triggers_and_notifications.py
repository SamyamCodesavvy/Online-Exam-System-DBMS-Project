import sqlite3

# Function to create the notifications table
def create_notifications_table():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

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

    connection.commit()
    connection.close()

# Function to fetch notifications for a user
def fetch_notifications(user_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT * FROM notifications 
    WHERE user_id = ? 
    ORDER BY timestamp DESC
    ''', (user_id,))
    
    notifications = cursor.fetchall()
    connection.close()

    return notifications

# Function to mark a notification as read
def mark_notification_as_read(notification_id):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    UPDATE notifications 
    SET is_read = 1 
    WHERE notification_id = ?
    ''', (notification_id,))
    
    connection.commit()
    connection.close()

# Function to create a trigger for notifying students of new exams
def create_new_exam_notification_trigger():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

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

    connection.commit()
    connection.close()

# Function to create a trigger for notifying students of exam results
def create_exam_result_notification_trigger():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

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

    connection.commit()
    connection.close()

# Function to create a trigger for notifying teachers of student enrollments
def create_student_enrollment_notification_trigger():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

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

    connection.commit()
    connection.close()

# Function to create a trigger for grading exams and updating results
def create_auto_grading_trigger():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_exam_submission
    AFTER INSERT ON submissions
    BEGIN
        -- Logic for automatic grading goes here
        -- This is a simplified example where we assume submissions table and correct answers are available
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

# Initial setup for creating triggers and notifications table
def setup_triggers_and_notifications():
    create_notifications_table()
    create_new_exam_notification_trigger()
    create_exam_result_notification_trigger()
    create_student_enrollment_notification_trigger()
    create_auto_grading_trigger()

if __name__ == '__main__':
    # Initial setup for triggers and notifications
    setup_triggers_and_notifications()
    print("Triggers and notifications setup complete.")
