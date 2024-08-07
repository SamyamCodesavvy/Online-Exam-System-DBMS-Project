import tkinter as tk
from tkinter import ttk, messagebox
from user_management import register_user, authenticate_user, fetch_all_users, delete_user, update_user
from exam_management import create_exam, update_exam, delete_exam, fetch_all_exams, fetch_exam_by_id, search_exams
from student_management import enroll_student, fetch_students_by_exam_id, track_student_performance
from question_bank import add_question, update_question, delete_question, fetch_all_questions, fetch_questions_by_exam_id
from reports import generate_performance_report, generate_detailed_student_report, calculate_average_scores_per_exam, calculate_pass_rates_per_exam

class OnlineExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Examination System")
        self.root.geometry("1000x700")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.create_login_page()

    def create_login_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        inner_frame = ttk.Frame(frame)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)

        tk.Label(inner_frame, text="Login", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(inner_frame, text="Username", font=("Helvetica", 14)).grid(row=1, column=0, pady=5, sticky="e")
        self.username_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Password", font=("Helvetica", 14)).grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(inner_frame, show='*', font=("Helvetica", 14))
        self.password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.role_var = tk.StringVar(value="student")
        tk.Radiobutton(inner_frame, text="Student", variable=self.role_var, value="student", font=("Helvetica", 12)).grid(row=3, column=0, pady=5, columnspan=2)
        tk.Radiobutton(inner_frame, text="Teacher", variable=self.role_var, value="teacher", font=("Helvetica", 12)).grid(row=4, column=0, pady=5, columnspan=2)
        tk.Radiobutton(inner_frame, text="Admin", variable=self.role_var, value="admin", font=("Helvetica", 12)).grid(row=5, column=0, pady=5, columnspan=2)

        tk.Button(inner_frame, text="Login", command=self.login, font=("Helvetica", 14), bg="#4CAF50", fg="white").grid(row=6, column=0, pady=20, columnspan=2)
        tk.Button(inner_frame, text="Register", command=self.create_register_page, font=("Helvetica", 14), bg="#2196F3", fg="white").grid(row=7, column=0, pady=5, columnspan=2)

    def create_register_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        inner_frame = ttk.Frame(frame)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)

        tk.Label(inner_frame, text="Register", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(inner_frame, text="Username", font=("Helvetica", 14)).grid(row=1, column=0, pady=5, sticky="e")
        self.reg_username_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.reg_username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Password", font=("Helvetica", 14)).grid(row=2, column=0, pady=5, sticky="e")
        self.reg_password_entry = tk.Entry(inner_frame, show='*', font=("Helvetica", 14))
        self.reg_password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.reg_role_var = tk.StringVar(value="student")
        tk.Radiobutton(inner_frame, text="Student", variable=self.reg_role_var, value="student", font=("Helvetica", 12)).grid(row=3, column=0, pady=5, columnspan=2)
        tk.Radiobutton(inner_frame, text="Teacher", variable=self.reg_role_var, value="teacher", font=("Helvetica", 12)).grid(row=4, column=0, pady=5, columnspan=2)
        tk.Radiobutton(inner_frame, text="Admin", variable=self.reg_role_var, value="admin", font=("Helvetica", 12)).grid(row=5, column=0, pady=5, columnspan=2)

        tk.Button(inner_frame, text="Register", command=self.register, font=("Helvetica", 14), bg="#4CAF50", fg="white").grid(row=6, column=0, pady=20, columnspan=2)
        tk.Button(inner_frame, text="Back to Login", command=self.create_login_page, font=("Helvetica", 14), bg="#f44336", fg="white").grid(row=7, column=0, pady=5, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        
        print(f"Trying to authenticate user: {username} with role: {role}")  # Debugging statement
        user = authenticate_user(username, password, role)
        print(f"Authenticated user: {user}")  # Debugging statement
        
        if user:
            if user[3] == role:
                self.user = user
                if role == "admin":
                    self.create_admin_page()
                elif role == "teacher":
                    self.create_teacher_page()
                elif role == "student":
                    self.create_student_page()
            else:
                messagebox.showerror("Error", "Incorrect role selected")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_var.get()
        
        result = register_user(username, password, role)
        messagebox.showinfo("Info", result)
        if result == "User registered successfully":
            self.create_login_page()

    def create_admin_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Admin Dashboard", font=("Helvetica", 24)).pack(pady=20)
        
        tk.Button(frame, text="Manage Users", command=self.create_manage_users_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(frame, text="Manage Exams", command=self.create_manage_exams_page, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Manage Questions", command=self.create_manage_questions_page, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Generate Reports", command=self.create_reports_page, font=("Helvetica", 14), bg="#9C27B0", fg="white").pack(pady=10)
        tk.Button(frame, text="Logout", command=self.create_login_page, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=20)

    def create_teacher_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Teacher Dashboard", font=("Helvetica", 24)).pack(pady=20)
        
        tk.Button(frame, text="Manage Exams", command=self.create_manage_exams_page, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Manage Questions", command=self.create_manage_questions_page, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Generate Reports", command=self.create_reports_page, font=("Helvetica", 14), bg="#9C27B0", fg="white").pack(pady=10)
        tk.Button(frame, text="Logout", command=self.create_login_page, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=20)

    def create_student_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Student Dashboard", font=("Helvetica", 24)).pack(pady=20)
        
        tk.Button(frame, text="Enroll in Exams", command=self.create_enroll_page, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="View Performance", command=self.create_performance_page, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Logout", command=self.create_login_page, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=20)

    def create_manage_users_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Manage Users", font=("Helvetica", 24)).pack(pady=20)
        
        self.user_listbox = tk.Listbox(frame, font=("Helvetica", 14), width=50, height=10)
        self.user_listbox.pack(pady=10)
        self.refresh_user_list()

        tk.Button(frame, text="Add User", command=self.create_register_page, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Delete User", command=self.delete_user, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=10)
        tk.Button(frame, text="Update User", command=self.update_user, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.create_admin_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def refresh_user_list(self):
        self.user_listbox.delete(0, tk.END)
        users = fetch_all_users()
        for user in users:
            self.user_listbox.insert(tk.END, f"{user[0]} - {user[1]} - {user[3]}")

    def delete_user(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if selected_user:
            user_id = selected_user.split(" - ")[0]
            result = delete_user(int(user_id))
            messagebox.showinfo("Info", result)
            self.refresh_user_list()

    def update_user(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if selected_user:
            user_id = selected_user.split(" - ")[0]
            self.clear_frame()

            frame = ttk.Frame(self.root)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

            inner_frame = ttk.Frame(frame)
            inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            inner_frame.columnconfigure(0, weight=1)
            inner_frame.columnconfigure(1, weight=1)

            tk.Label(inner_frame, text="Update User", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

            tk.Label(inner_frame, text="Username", font=("Helvetica", 14)).grid(row=1, column=0, pady=5, sticky="e")
            self.update_username_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Password", font=("Helvetica", 14)).grid(row=2, column=0, pady=5, sticky="e")
            self.update_password_entry = tk.Entry(inner_frame, show='*', font=("Helvetica", 14))
            self.update_password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

            self.update_role_var = tk.StringVar(value="student")
            tk.Radiobutton(inner_frame, text="Student", variable=self.update_role_var, value="student", font=("Helvetica", 12)).grid(row=3, column=0, pady=5, columnspan=2)
            tk.Radiobutton(inner_frame, text="Teacher", variable=self.update_role_var, value="teacher", font=("Helvetica", 12)).grid(row=4, column=0, pady=5, columnspan=2)
            tk.Radiobutton(inner_frame, text="Admin", variable=self.update_role_var, value="admin", font=("Helvetica", 12)).grid(row=5, column=0, pady=5, columnspan=2)

            tk.Button(inner_frame, text="Update", command=lambda: self.update_user_db(user_id), font=("Helvetica", 14), bg="#FF9800", fg="white").grid(row=6, column=0, pady=20, columnspan=2)
            tk.Button(inner_frame, text="Back", command=self.create_manage_users_page, font=("Helvetica", 14), bg="#2196F3", fg="white").grid(row=7, column=0, pady=5, columnspan=2)

    def update_user_db(self, user_id):
        username = self.update_username_entry.get()
        password = self.update_password_entry.get()
        role = self.update_role_var.get()
        
        result = update_user(int(user_id), username, password, role)
        messagebox.showinfo("Info", result)
        if result == "User information updated successfully":
            self.create_manage_users_page()

    def create_manage_exams_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Manage Exams", font=("Helvetica", 24)).pack(pady=20)

        self.exam_listbox = tk.Listbox(frame, font=("Helvetica", 14), width=50, height=10)
        self.exam_listbox.pack(pady=10)
        self.refresh_exam_list()

        tk.Button(frame, text="Add Exam", command=self.add_exam, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Delete Exam", command=self.delete_exam, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=10)
        tk.Button(frame, text="Update Exam", command=self.update_exam, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.create_admin_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def refresh_exam_list(self):
        self.exam_listbox.delete(0, tk.END)
        exams = fetch_all_exams()
        for exam in exams:
            self.exam_listbox.insert(tk.END, f"{exam[0]} - {exam[1]} - {exam[2]} - {exam[4]}")

    def add_exam(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        inner_frame = ttk.Frame(frame)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)

        tk.Label(inner_frame, text="Add Exam", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(inner_frame, text="Exam Name", font=("Helvetica", 14)).grid(row=1, column=0, pady=5, sticky="e")
        self.add_exam_name_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_exam_name_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Subject", font=("Helvetica", 14)).grid(row=2, column=0, pady=5, sticky="e")
        self.add_subject_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_subject_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Teacher ID", font=("Helvetica", 14)).grid(row=3, column=0, pady=5, sticky="e")
        self.add_teacher_id_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_teacher_id_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Date (YYYY-MM-DD)", font=("Helvetica", 14)).grid(row=4, column=0, pady=5, sticky="e")
        self.add_date_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_date_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        tk.Button(inner_frame, text="Add Exam", command=self.add_exam_db, font=("Helvetica", 14), bg="#4CAF50", fg="white").grid(row=5, column=0, pady=20, columnspan=2)
        tk.Button(inner_frame, text="Back", command=self.create_manage_exams_page, font=("Helvetica", 14), bg="#2196F3", fg="white").grid(row=6, column=0, pady=5, columnspan=2)

    def add_exam_db(self):
        exam_name = self.add_exam_name_entry.get()
        subject = self.add_subject_entry.get()
        teacher_id = self.add_teacher_id_entry.get()
        date = self.add_date_entry.get()

        result = create_exam(exam_name, subject, int(teacher_id), date)
        messagebox.showinfo("Info", result)
        if result == "Exam created successfully":
            self.create_manage_exams_page()

    def delete_exam(self):
        selected_exam = self.exam_listbox.get(tk.ACTIVE)
        if selected_exam:
            exam_id = selected_exam.split(" - ")[0]
            result = delete_exam(int(exam_id))
            messagebox.showinfo("Info", result)
            self.refresh_exam_list()

    def update_exam(self):
        selected_exam = self.exam_listbox.get(tk.ACTIVE)
        if selected_exam:
            exam_id = selected_exam.split(" - ")[0]
            self.clear_frame()

            frame = ttk.Frame(self.root)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

            inner_frame = ttk.Frame(frame)
            inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            inner_frame.columnconfigure(0, weight=1)
            inner_frame.columnconfigure(1, weight=1)

            tk.Label(inner_frame, text="Update Exam", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

            tk.Label(inner_frame, text="Exam Name", font=("Helvetica", 14)).grid(row=1, column=0, pady=5, sticky="e")
            self.update_exam_name_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_exam_name_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Subject", font=("Helvetica", 14)).grid(row=2, column=0, pady=5, sticky="e")
            self.update_subject_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_subject_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Teacher ID", font=("Helvetica", 14)).grid(row=3, column=0, pady=5, sticky="e")
            self.update_teacher_id_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_teacher_id_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Date (YYYY-MM-DD)", font=("Helvetica", 14)).grid(row=4, column=0, pady=5, sticky="e")
            self.update_date_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_date_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

            tk.Button(inner_frame, text="Update Exam", command=lambda: self.update_exam_db(exam_id), font=("Helvetica", 14), bg="#FF9800", fg="white").grid(row=5, column=0, pady=20, columnspan=2)
            tk.Button(inner_frame, text="Back", command=self.create_manage_exams_page, font=("Helvetica", 14), bg="#2196F3", fg="white").grid(row=6, column=0, pady=5, columnspan=2)

    def update_exam_db(self, exam_id):
        exam_name = self.update_exam_name_entry.get()
        subject = self.update_subject_entry.get()
        teacher_id = self.update_teacher_id_entry.get()
        date = self.update_date_entry.get()

        result = update_exam(int(exam_id), exam_name, subject, int(teacher_id), date)
        messagebox.showinfo("Info", result)
        if result == "Exam updated successfully":
            self.create_manage_exams_page()

    def create_manage_questions_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Manage Questions", font=("Helvetica", 24)).pack(pady=20)

        self.exam_var = tk.StringVar()
        exams = fetch_all_exams()
        self.exam_options = {f"{exam[1]} ({exam[0]})": exam[0] for exam in exams}
        self.exam_menu = ttk.Combobox(frame, textvariable=self.exam_var, values=list(self.exam_options.keys()), font=("Helvetica", 14))
        self.exam_menu.pack(pady=10)

        self.question_listbox = tk.Listbox(frame, font=("Helvetica", 14), width=50, height=10)
        self.question_listbox.pack(pady=10)

        tk.Button(frame, text="Load Questions", command=self.load_questions, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Add Question", command=self.add_question, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Delete Question", command=self.delete_question, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=10)
        tk.Button(frame, text="Update Question", command=self.update_question, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.back_to_dashboard, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def load_questions(self):
        self.question_listbox.delete(0, tk.END)
        exam_id = self.exam_options.get(self.exam_var.get())
        if exam_id:
            questions = fetch_questions_by_exam_id(exam_id)
            for question in questions:
                self.question_listbox.insert(tk.END, f"{question[0]} - {question[1]} - {question[2]} - {question[3]} - {question[4]} - {question[5]}")

    def add_question(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        inner_frame = ttk.Frame(frame)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)

        tk.Label(inner_frame, text="Add Question", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(inner_frame, text="Exam ID", font=("Helvetica", 14)).grid(row=1, column=0, pady=5, sticky="e")
        self.add_exam_id_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_exam_id_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Question Text", font=("Helvetica", 14)).grid(row=2, column=0, pady=5, sticky="e")
        self.add_question_text_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_question_text_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Difficulty Level (easy, medium, hard)", font=("Helvetica", 14)).grid(row=3, column=0, pady=5, sticky="e")
        self.add_difficulty_level_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_difficulty_level_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Correct Answer", font=("Helvetica", 14)).grid(row=4, column=0, pady=5, sticky="e")
        self.add_correct_answer_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_correct_answer_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        tk.Label(inner_frame, text="Marks", font=("Helvetica", 14)).grid(row=5, column=0, pady=5, sticky="e")
        self.add_marks_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
        self.add_marks_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        tk.Button(inner_frame, text="Add Question", command=self.add_question_db, font=("Helvetica", 14), bg="#4CAF50", fg="white").grid(row=6, column=0, pady=20, columnspan=2)
        tk.Button(inner_frame, text="Back", command=self.create_manage_questions_page, font=("Helvetica", 14), bg="#2196F3", fg="white").grid(row=7, column=0, pady=5, columnspan=2)

    def add_question_db(self):
        exam_id = self.add_exam_id_entry.get()
        question_text = self.add_question_text_entry.get()
        difficulty_level = self.add_difficulty_level_entry.get()
        correct_answer = self.add_correct_answer_entry.get()
        marks = self.add_marks_entry.get()

        result = add_question(int(exam_id), question_text, difficulty_level, correct_answer, int(marks))
        messagebox.showinfo("Info", result)
        if result == "Question added successfully":
            self.create_manage_questions_page()

    def delete_question(self):
        selected_question = self.question_listbox.get(tk.ACTIVE)
        if selected_question:
            question_id = selected_question.split(" - ")[0]
            result = delete_question(int(question_id))
            messagebox.showinfo("Info", result)
            self.load_questions()

    def update_question(self):
        selected_question = self.question_listbox.get(tk.ACTIVE)
        if selected_question:
            question_id = selected_question.split(" - ")[0]
            self.clear_frame()

            frame = ttk.Frame(self.root)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

            inner_frame = ttk.Frame(frame)
            inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            inner_frame.columnconfigure(0, weight=1)
            inner_frame.columnconfigure(1, weight=1)

            tk.Label(inner_frame, text="Update Question", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

            tk.Label(inner_frame, text="Exam ID", font=("Helvetica", 14)).grid(row=1, column=0, pady=5, sticky="e")
            self.update_exam_id_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_exam_id_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Question Text", font=("Helvetica", 14)).grid(row=2, column=0, pady=5, sticky="e")
            self.update_question_text_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_question_text_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Difficulty Level (easy, medium, hard)", font=("Helvetica", 14)).grid(row=3, column=0, pady=5, sticky="e")
            self.update_difficulty_level_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_difficulty_level_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Correct Answer", font=("Helvetica", 14)).grid(row=4, column=0, pady=5, sticky="e")
            self.update_correct_answer_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_correct_answer_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

            tk.Label(inner_frame, text="Marks", font=("Helvetica", 14)).grid(row=5, column=0, pady=5, sticky="e")
            self.update_marks_entry = tk.Entry(inner_frame, font=("Helvetica", 14))
            self.update_marks_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")

            tk.Button(inner_frame, text="Update Question", command=lambda: self.update_question_db(question_id), font=("Helvetica", 14), bg="#FF9800", fg="white").grid(row=6, column=0, pady=20, columnspan=2)
            tk.Button(inner_frame, text="Back", command=self.create_manage_questions_page, font=("Helvetica", 14), bg="#2196F3", fg="white").grid(row=7, column=0, pady=5, columnspan=2)

    def update_question_db(self, question_id):
        exam_id = self.update_exam_id_entry.get()
        question_text = self.update_question_text_entry.get()
        difficulty_level = self.update_difficulty_level_entry.get()
        correct_answer = self.update_correct_answer_entry.get()
        marks = self.update_marks_entry.get()

        result = update_question(int(question_id), int(exam_id), question_text, difficulty_level, correct_answer, int(marks))
        messagebox.showinfo("Info", result)
        if result == "Question updated successfully":
            self.create_manage_questions_page()

    def create_reports_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Generate Reports", font=("Helvetica", 24)).pack(pady=20)

        tk.Button(frame, text="Performance Report", command=self.generate_performance_report, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Detailed Student Report", command=self.generate_detailed_student_report, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Average Scores per Exam", command=self.calculate_average_scores_per_exam, font=("Helvetica", 14), bg="#9C27B0", fg="white").pack(pady=10)
        tk.Button(frame, text="Pass Rates per Exam", command=self.calculate_pass_rates_per_exam, font=("Helvetica", 14), bg="#3F51B5", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.back_to_dashboard, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def generate_performance_report(self):
        report = generate_performance_report()
        self.display_report(report, ["Exam Name", "Subject", "Average Score", "Pass Rate"])

    def generate_detailed_student_report(self):
        report = generate_detailed_student_report()
        self.display_report(report, ["Student Name", "Exam Name", "Subject", "Score"])

    def calculate_average_scores_per_exam(self):
        report = calculate_average_scores_per_exam()
        self.display_report(report, ["Exam Name", "Average Score"])

    def calculate_pass_rates_per_exam(self):
        report = calculate_pass_rates_per_exam()
        self.display_report(report, ["Exam Name", "Pass Rate"])

    def display_report(self, report, headers):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        table_frame = ttk.Frame(frame)
        table_frame.grid(row=0, column=0, padx=20, pady=20)
        
        for i, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Helvetica", 16, "bold")).grid(row=0, column=i, padx=10, pady=5)

        for row_idx, row in enumerate(report, start=1):
            for col_idx, value in enumerate(row):
                tk.Label(table_frame, text=value, font=("Helvetica", 14)).grid(row=row_idx, column=col_idx, padx=10, pady=5)
        
        tk.Button(frame, text="Back", command=self.back_to_dashboard, font=("Helvetica", 14), bg="#2196F3", fg="white").grid(row=1, column=0, pady=20)

    def create_enroll_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Enroll in Exams", font=("Helvetica", 24)).pack(pady=20)

        self.enroll_exam_listbox = tk.Listbox(frame, font=("Helvetica", 14), width=50, height=10)
        self.enroll_exam_listbox.pack(pady=10)
        self.refresh_exam_list()

        tk.Button(frame, text="Enroll", command=self.enroll_in_exam, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.create_student_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def enroll_in_exam(self):
        selected_exam = self.enroll_exam_listbox.get(tk.ACTIVE)
        if selected_exam:
            exam_id = selected_exam.split(" - ")[0]
            result = enroll_student(self.user[0], int(exam_id))
            messagebox.showinfo("Info", result)

    def create_performance_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Performance", font=("Helvetica", 24)).pack(pady=20)

        performance = track_student_performance(self.user[0])
        self.display_report(performance, ["Exam Name", "Subject", "Score"])

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def back_to_dashboard(self):
        if self.user[3] == "admin":
            self.create_admin_page()
        elif self.user[3] == "teacher":
            self.create_teacher_page()
        elif self.user[3] == "student":
            self.create_student_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineExamApp(root)
    root.mainloop()
