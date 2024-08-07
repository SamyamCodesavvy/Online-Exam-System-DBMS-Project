import tkinter as tk
from tkinter import ttk, messagebox
from utils import get_db_connection, setup_views_and_triggers
from user_management import register_user, authenticate_user, fetch_all_users, delete_user, update_user
from exam_management import create_exam, update_exam, delete_exam, fetch_all_exams, fetch_exam_by_id, search_exams
from student_management import enroll_student, fetch_students_by_exam_id, track_student_performance, store_student_answer
from question_bank import add_question, update_question, delete_question, fetch_all_questions, fetch_questions_by_exam_id
from reports import generate_performance_report, generate_detailed_student_report, calculate_average_scores_per_exam, calculate_pass_rates_per_exam

class OnlineExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Examination System by Samyam Giri and Sandip Acharya")
        self.root.geometry("1480x820")
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
        
        user = authenticate_user(username, password, role)
        
        if user:
            if user[3] == role:
                self.user = user
                self.user_role = role
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
        
        columns = ('ID', 'Username', 'Role')
        self.user_tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.user_tree.heading('ID', text='ID')
        self.user_tree.heading('Username', text='Username')
        self.user_tree.heading('Role', text='Role')
        self.user_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.style_treeview(self.user_tree)
        self.refresh_user_list()

        tk.Button(frame, text="Add User", command=self.create_register_page, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Delete User", command=self.delete_user, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=10)
        tk.Button(frame, text="Update User", command=self.update_user, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.go_back, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def refresh_user_list(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        users = fetch_all_users()
        for user in users:
            self.user_tree.insert('', tk.END, values=(user[0], user[1], user[3]))

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if selected_item:
            user_id = self.user_tree.item(selected_item[0], 'values')[0]
            result = delete_user(int(user_id))
            messagebox.showinfo("Info", result)
            self.refresh_user_list()

    def update_user(self):
        selected_item = self.user_tree.selection()
        if selected_item:
            user_id = self.user_tree.item(selected_item[0], 'values')[0]
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

        columns = ('ID', 'Name', 'Subject', 'Date')
        self.exam_tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.exam_tree.heading('ID', text='ID')
        self.exam_tree.heading('Name', text='Name')
        self.exam_tree.heading('Subject', text='Subject')
        self.exam_tree.heading('Date', text='Date')
        self.exam_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.style_treeview(self.exam_tree)
        self.refresh_exam_list()

        tk.Button(frame, text="Add Exam", command=self.add_exam, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Delete Exam", command=self.delete_exam, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=10)
        tk.Button(frame, text="Update Exam", command=self.update_exam, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.go_back, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def refresh_exam_list(self):
        for row in self.exam_tree.get_children():
            self.exam_tree.delete(row)
        exams = fetch_all_exams()
        for exam in exams:
            self.exam_tree.insert('', tk.END, values=(exam[0], exam[1], exam[2], exam[4]))

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
        selected_item = self.exam_tree.selection()
        if selected_item:
            exam_id = self.exam_tree.item(selected_item[0], 'values')[0]
            result = delete_exam(int(exam_id))
            messagebox.showinfo("Info", result)
            self.refresh_exam_list()

    def update_exam(self):
        selected_item = self.exam_tree.selection()
        if selected_item:
            exam_id = self.exam_tree.item(selected_item[0], 'values')[0]
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

        columns = ('ID', 'Exam ID', 'Question Text', 'Difficulty Level', 'Correct Answer', 'Marks')
        self.question_tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.question_tree.heading('ID', text='ID')
        self.question_tree.heading('Exam ID', text='Exam ID')
        self.question_tree.heading('Question Text', text='Question Text')
        self.question_tree.heading('Difficulty Level', text='Difficulty Level')
        self.question_tree.heading('Correct Answer', text='Correct Answer')
        self.question_tree.heading('Marks', text='Marks')
        self.question_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.style_treeview(self.question_tree)

        tk.Button(frame, text="Load Questions", command=self.load_questions, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Add Question", command=self.add_question, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Delete Question", command=self.delete_question, font=("Helvetica", 14), bg="#f44336", fg="white").pack(pady=10)
        tk.Button(frame, text="Update Question", command=self.update_question, font=("Helvetica", 14), bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.go_back, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def load_questions(self):
        self.question_tree.delete(*self.question_tree.get_children())
        exam_id = self.exam_options.get(self.exam_var.get())
        if exam_id:
            questions = fetch_questions_by_exam_id(exam_id)
            for question in questions:
                self.question_tree.insert('', tk.END, values=(question[0], question[1], question[2], question[3], question[4], question[5]))

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
        selected_item = self.question_tree.selection()
        if selected_item:
            question_id = self.question_tree.item(selected_item[0], 'values')[0]
            result = delete_question(int(question_id))
            messagebox.showinfo("Info", result)
            self.load_questions()

    def update_question(self):
        selected_item = self.question_tree.selection()
        if selected_item:
            question_id = self.question_tree.item(selected_item[0], 'values')[0]
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
        tk.Button(frame, text="Back", command=self.go_back, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def generate_performance_report(self):
        report = generate_performance_report()
        self.display_report(report, ["Exam Name", "Subject", "Average Score", "Pass Rate"], "Performance Report")

    def generate_detailed_student_report(self):
        self.clear_frame()
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Detailed Student Report", font=("Helvetica", 24)).pack(pady=20)

        search_frame = ttk.Frame(frame)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search By:", font=("Helvetica", 14)).pack(side=tk.LEFT, padx=5)
        self.search_by_var = tk.StringVar(value="exam")
        self.search_by_menu = ttk.Combobox(search_frame, textvariable=self.search_by_var, values=["exam", "student"], font=("Helvetica", 14))
        self.search_by_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(search_frame, text="Search Value:", font=("Helvetica", 14)).pack(side=tk.LEFT, padx=5)
        self.search_value_entry = tk.Entry(search_frame, font=("Helvetica", 14))
        self.search_value_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Search", command=self.display_detailed_student_report, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Back", command=self.create_reports_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def display_detailed_student_report(self):
        search_by = self.search_by_var.get()
        search_value = self.search_value_entry.get()
        report = generate_detailed_student_report(search_by, search_value)
        self.display_report(report, ["Student Name", "Exam Name", "Subject", "Score"], "Detailed Student Report")

    def calculate_average_scores_per_exam(self):
        report = calculate_average_scores_per_exam()
        self.display_report(report, ["Exam Name", "Average Score"], "Average Scores per Exam")

    def calculate_pass_rates_per_exam(self):
        report = calculate_pass_rates_per_exam()
        self.display_report(report, ["Exam Name", "Pass Rate"], "Pass Rates per Exam")

    def display_report(self, report, columns, title):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text=title, font=("Helvetica", 24)).pack(pady=20)

        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.style_treeview(tree)

        for row in report:
            tree.insert('', tk.END, values=row)

        tk.Button(frame, text="Back", command=self.create_reports_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)

    def create_enroll_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Enroll in Exams", font=("Helvetica", 24)).pack(pady=20)

        columns = ('ID', 'Exam Name', 'Subject', 'Date')
        self.enroll_tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.enroll_tree.heading('ID', text='ID')
        self.enroll_tree.heading('Exam Name', text='Exam Name')
        self.enroll_tree.heading('Subject', text='Subject')
        self.enroll_tree.heading('Date', text='Date')
        self.enroll_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.style_treeview(self.enroll_tree)
        self.refresh_enroll_list()

        tk.Button(frame, text="Enroll", command=self.enroll_in_exam, font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.create_student_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)



    def refresh_enroll_list(self):
        for row in self.enroll_tree.get_children():
            self.enroll_tree.delete(row)
        exams = fetch_all_exams()
        for exam in exams:
            self.enroll_tree.insert('', tk.END, values=(exam[0], exam[1], exam[2], exam[4]))

    def enroll_in_exam(self):
        selected_item = self.enroll_tree.selection()
        if selected_item:
            exam_id = self.enroll_tree.item(selected_item[0], 'values')[0]
            student_id = self.user[0]
            
            # Check if already enrolled
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM enrollments WHERE student_id = ? AND exam_id = ?", (student_id, exam_id))
            enrollment = cursor.fetchone()
            connection.close()

            if enrollment:
                messagebox.showinfo("Info", "Already enrolled in this exam")
            else:
                result = enroll_student(student_id, int(exam_id))
                messagebox.showinfo("Info", result)
                if result == "Student enrolled successfully":
                    self.start_exam(int(exam_id))

        # Check if already enrolled
            cursor.execute("SELECT * FROM enrollments WHERE student_id = ? AND exam_id = ?", (student_id, exam_id))
            enrollment = cursor.fetchone()

            if enrollment:
                messagebox.showinfo("Info", "Already enrolled in this exam")
            else:
                cursor.execute("INSERT INTO enrollments (student_id, exam_id) VALUES (?, ?)", (student_id, exam_id))
                connection.commit()
                messagebox.showinfo("Info", "Enrolled successfully")

        connection.close()
    
    def start_exam(self, exam_id):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Exam", font=("Helvetica", 24)).pack(pady=20)

        self.exam_questions = fetch_questions_by_exam_id(exam_id)
        self.student_answers = {}

        for index, question in enumerate(self.exam_questions):
            question_frame = ttk.Frame(frame)
            question_frame.pack(pady=10, fill=tk.BOTH, expand=True)

            tk.Label(question_frame, text=f"Q{index + 1}: {question[2]}", font=("Helvetica", 14)).pack(anchor='w')
            self.student_answers[question[0]] = tk.StringVar()
            tk.Entry(question_frame, textvariable=self.student_answers[question[0]], font=("Helvetica", 14)).pack(anchor='w', fill=tk.X, expand=True)

        tk.Button(frame, text="Submit Exam", command=lambda: self.submit_exam(exam_id), font=("Helvetica", 14), bg="#4CAF50", fg="white").pack(pady=20)
        tk.Button(frame, text="Back", command=self.create_student_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)


    def submit_exam(self, exam_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        for question_id, answer in self.student_answers.items():
            cursor.execute(
                "INSERT INTO submissions (enrollment_id, question_id, answer) VALUES ((SELECT enrollment_id FROM enrollments WHERE student_id = ? AND exam_id = ?), ?, ?)",
                (self.user[0], exam_id, question_id, answer.get())
            )
        connection.commit()

        # Calculate and update score
        cursor.execute(
            "SELECT SUM(q.marks) FROM questions q JOIN submissions s ON q.question_id = s.question_id WHERE s.enrollment_id = (SELECT enrollment_id FROM enrollments WHERE student_id = ? AND exam_id = ?) AND q.correct_answer = s.answer",
            (self.user[0], exam_id)
        )
        score = cursor.fetchone()[0] or 0
        cursor.execute(
            "UPDATE results SET score = ? WHERE enrollment_id = (SELECT enrollment_id FROM enrollments WHERE student_id = ? AND exam_id = ?)",
            (score, self.user[0], exam_id)
        )
        connection.commit()
        connection.close()

        messagebox.showinfo("Info", "Exam submitted successfully")
        self.create_student_page()

    # Calculate score
        cursor.execute('''
        INSERT INTO results (enrollment_id, score)
        SELECT e.enrollment_id, SUM(CASE WHEN q.correct_answer = s.answer THEN q.marks ELSE 0 END) as score
        FROM submissions s
        JOIN enrollments e ON e.student_id = s.student_id AND e.exam_id = s.exam_id
        JOIN questions q ON q.question_id = s.question_id
        WHERE s.student_id = ? AND s.exam_id = ?
        GROUP BY e.enrollment_id
        ''', (self.user[0], exam_id))

        connection.commit()
        connection.close()

        messagebox.showinfo("Info", "Exam submitted successfully")
        self.create_student_page()
        

    def create_performance_page(self):
        self.clear_frame()

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="View Performance", font=("Helvetica", 24)).pack(pady=20)

        columns = ('Exam Name', 'Subject', 'Score', 'Percentage', 'Highest Score')
        self.performance_tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.performance_tree.heading('Exam Name', text='Exam Name')
        self.performance_tree.heading('Subject', text='Subject')
        self.performance_tree.heading('Score', text='Score')
        self.performance_tree.heading('Percentage', text='Percentage')
        self.performance_tree.heading('Highest Score', text='Highest Score')
        self.performance_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.style_treeview(self.performance_tree)
        self.refresh_performance_list()

        tk.Button(frame, text="Back", command=self.create_student_page, font=("Helvetica", 14), bg="#2196F3", fg="white").pack(pady=20)




    def refresh_performance_list(self):
        for row in self.performance_tree.get_children():
            self.performance_tree.delete(row)

        student_id = self.user[0]
        connection = get_db_connection()
        cursor = connection.cursor()
    
        cursor.execute("""
                SELECT DISTINCT e.exam_name, e.subject, r.score, 
                (r.score * 100.0 / (SELECT SUM(marks) FROM questions WHERE exam_id = e.exam_id)) AS percentage,
                (SELECT MAX(score) FROM results WHERE enrollment_id IN (SELECT enrollment_id FROM enrollments WHERE exam_id = e.exam_id)) AS highest_score
                FROM results r
                JOIN enrollments en ON r.enrollment_id = en.enrollment_id
                JOIN exams e ON en.exam_id = e.exam_id
                WHERE en.student_id = ?
        """, (student_id,))
        performance = cursor.fetchall()
        connection.close()

        for record in performance:
            self.performance_tree.insert('', tk.END, values=(record[0], record[1], record[2], round(record[3], 2), record[4]))


    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.user_role == "admin":
            self.create_admin_page()
        elif self.user_role == "teacher":
            self.create_teacher_page()
        elif self.user_role == "student":
            self.create_student_page()

    def style_treeview(self, tree):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 14))
        style.configure("Treeview", font=("Helvetica", 12))

if __name__ == "__main__":
    setup_views_and_triggers()
    root = tk.Tk()
    app = OnlineExamApp(root)
    root.mainloop()
