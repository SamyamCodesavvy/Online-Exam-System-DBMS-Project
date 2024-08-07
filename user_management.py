import sqlite3
from hashlib import sha256
from utils import get_db_connection, hash_password

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def register_user(username, password, role):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        connection.execute('BEGIN')
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            connection.rollback()
            if existing_user[3] == role:
                return "Username already exists"
            else:
                return f"Username {username} already exists with a different role: {existing_user[3]}"

        hashed_password = hash_password(password)
        print(f"Registering user with username: {username}, hashed password: {hashed_password}, role: {role}")

        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, role))
        
        connection.commit()
        return "User registered successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        print(f"An error occurred while registering user {username}: {e}")
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

def authenticate_user(username, password, role):
    connection = get_db_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)
    print(f"Authenticating user with username: {username}, hashed password: {hashed_password}")

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    
    if user:
        stored_role = user[3]
        print(f"Stored role: {stored_role}, Provided role: {role}")
        if stored_role == role:
            print(f"Authentication successful for user: {username} with role: {role}")
            connection.close()
            return user
        else:
            print(f"Role mismatch for user: {username}. Expected: {stored_role}, Provided: {role}")
            connection.close()
            return None
    else:
        print(f"Authentication failed for user: {username}")
        connection.close()
        return None

def get_user_role(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    role = cursor.fetchone()[0]
    connection.close()

    return role

def update_user(user_id, username, password, role):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        connection.execute('BEGIN')

        hashed_password = hash_password(password)

        cursor.execute("UPDATE users SET username = ?, password = ?, role = ? WHERE user_id = ?",
                       (username, hashed_password, role, user_id))
        
        connection.commit()
        return "User information updated successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        print(f"An error occurred while updating user {user_id}: {e}")
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

def delete_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        connection.execute('BEGIN')

        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        
        connection.commit()
        return "User deleted successfully"
    
    except sqlite3.Error as e:
        connection.rollback()
        print(f"An error occurred while deleting user {user_id}: {e}")
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

def fetch_all_users():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()

    return users

def fetch_user_by_username(username):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()

    return user

def search_users_by_role(role):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE role = ?", (role,))
    users = cursor.fetchall()
    connection.close()

    return users

def role_based_access(user_id, required_role):
    user_role = get_user_role(user_id)
    return user_role == required_role

def create_user_role_view():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE VIEW IF NOT EXISTS user_roles AS
    SELECT user_id, username, role FROM users
    ''')
    
    connection.commit()
    connection.close()

def fetch_user_roles_view():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user_roles")
    user_roles = cursor.fetchall()
    connection.close()

    return user_roles

def create_user_registration_trigger():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS after_user_registration
    AFTER INSERT ON users
    BEGIN
        INSERT INTO enrollments (student_id, exam_id)
        VALUES (NEW.user_id, (SELECT exam_id FROM exams ORDER BY date LIMIT 1));
    END;
    ''')
    
    connection.commit()
    connection.close()

def setup_views_and_triggers():
    create_user_role_view()
    create_user_registration_trigger()

if __name__ == '__main__':
    setup_views_and_triggers()
    print("User management setup complete with views and triggers.")
