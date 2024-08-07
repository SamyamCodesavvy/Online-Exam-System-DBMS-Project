import sqlite3
from utils import get_db_connection

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

def calculate_pass_rates_per_exam():
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT 
        exams.exam_name, 
        SUM(CASE WHEN results.score * 100.0 / (SELECT SUM(marks) FROM questions WHERE exam_id = exams.exam_id) >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(results.score) AS pass_rate
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    GROUP BY exams.exam_id
    ''')

    pass_rates = cursor.fetchall()
    connection.close()

    return pass_rates

def generate_detailed_student_report(search_by=None, search_value=None):
    connection = sqlite3.connect('online_exam.db')
    cursor = connection.cursor()

    query = '''
    SELECT users.username AS student_name, exams.exam_name, exams.subject, results.score
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    JOIN users ON enrollments.student_id = users.user_id
    '''
    
    if search_by and search_value:
        if search_by == "exam":
            query += " WHERE exams.exam_name = ?"
        elif search_by == "student":
            query += " WHERE users.username = ?"
        cursor.execute(query, (search_value,))
    else:
        cursor.execute(query)
    
    report = cursor.fetchall()
    connection.close()
    return report

def calculate_average_scores_per_exam():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = '''
    SELECT exams.exam_name, AVG(results.score) AS average_score
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    GROUP BY exams.exam_id
    '''
    
    cursor.execute(query)
    report = cursor.fetchall()
    
    connection.close()
    return report


def create_student_performance_history_view():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS student_performance_history AS
    SELECT students.username AS student_name, exams.exam_name, exams.subject, results.score
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    JOIN users AS students ON enrollments.student_id = students.user_id
    ''')
    
    connection.commit()
    connection.close()

def fetch_student_performance_history_view():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM student_performance_history")
    performance_history = cursor.fetchall()
    connection.close()

    return performance_history

def create_exam_result_statistics_view():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS exam_result_statistics AS
    SELECT exams.exam_name, AVG(results.score) AS average_score, 
    SUM(CASE WHEN results.score >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(results.score) AS pass_rate
    FROM results
    JOIN enrollments ON results.enrollment_id = enrollments.enrollment_id
    JOIN exams ON enrollments.exam_id = exams.exam_id
    GROUP BY exams.exam_id
    ''')
    
    connection.commit()
    connection.close()

def fetch_exam_result_statistics_view():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM exam_result_statistics")
    statistics = cursor.fetchall()
    connection.close()

    return statistics

def create_exam_statistics_update_trigger():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_result_insert
    AFTER INSERT ON results
    BEGIN
        UPDATE exam_result_statistics
        SET average_score = (
            SELECT AVG(score)
            FROM results
            WHERE results.exam_id = NEW.exam_id
        ),
        pass_rate = (
            SELECT SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
            FROM results
            WHERE results.exam_id = NEW.exam_id
        )
        WHERE exam_id = NEW.exam_id;
    END;
    ''')
    
    connection.commit()
    connection.close()

def setup_views_and_triggers():
    create_student_performance_history_view()
    create_exam_result_statistics_view()
    create_exam_statistics_update_trigger()

if __name__ == '__main__':
    setup_views_and_triggers()
    print("Reports setup complete with views and triggers.")
