from tkinter import *
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import re
from datetime import datetime
import pyttsx3 
import threading 
from time import strftime
from ttkbootstrap.widgets import DateEntry


class Student:
    def __init__(self, root):
        self.root = root

        self.root.state('zoomed') 
        self.root.title("Face Recognition System - Student Management")
        style = ttk.Style("vapor")  

        # Initialize TTS engine in background to avoid delays
        self.engine = None
        threading.Thread(target=self._init_tts_engine, daemon=True).start()

        # Variables
        self.var_dep = StringVar()
        self.var_group = StringVar()
        self.var_year = StringVar()
        self.var_sem = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_course = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_proctor = StringVar()
        self.var_radio1 = StringVar()
        self.var_search_by = StringVar()
        self.var_search_text = StringVar()

        # Create main container with gradient-like effect
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=BOTH, expand=YES)

        # Header Frame with modern design
        header_frame = ttk.Frame(main_container, bootstyle="primary")
        header_frame.pack(fill=X, pady=(0, 10))

        # Title with icon-like effect
        title_frame = ttk.Frame(header_frame, bootstyle="primary")
        title_frame.pack(fill=X, pady=15)

        title_label = ttk.Label(
            title_frame,
            text="🎓 STUDENT MANAGEMENT SYSTEM",
            font=("Segoe UI", 32, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(side=LEFT, padx=20)

        # Time display in header
        self.time_frame = ttk.Frame(header_frame, bootstyle="primary")
        self.time_frame.pack(side=RIGHT, padx=20, pady=15)

        ttk.Label(
            self.time_frame,
            text="🕐",
            font=("Segoe UI", 20),
            bootstyle="inverse-primary"
        ).pack(side=LEFT, padx=(0, 10))

        self.time_lbl = ttk.Label(
            self.time_frame,
            font=("Segoe UI", 16, "bold"),
            bootstyle="inverse-primary"
        )
        self.time_lbl.pack(side=LEFT)
        self.update_time()

        # Main content frame with modern card design
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=(0, 20))

        # Left Panel - Student Details (Modern Card)
        left_panel = ttk.Labelframe(
            content_frame,
            text="📝 Student Details",
            bootstyle="info",
            padding=15
        )
        left_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Current Course Section
        course_frame = ttk.Labelframe(
            left_panel,
            text="📚 Current Course Information",
            bootstyle="primary",
            padding=15
        )
        course_frame.pack(fill=X, pady=(0, 15))

        # Course fields in grid
        course_grid = ttk.Frame(course_frame)
        course_grid.pack(fill=X)

        # Department
        ttk.Label(course_grid, text="Department:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky=W, padx=5, pady=8
        )
        dept_combo = ttk.Combobox(
            course_grid,
            textvariable=self.var_dep,
            values=["Select Department", "CSE", "ECE", "ENTC", "MECH", "EE", "CIVIL", "BScITM", "MCA", "MBA", "BArch"],
            state="readonly",
            font=("Segoe UI", 10),
            bootstyle="primary",
            width=22
        )
        dept_combo.current(0)
        dept_combo.grid(row=0, column=1, padx=5, pady=8, sticky=W)

        # Group
        ttk.Label(course_grid, text="Group:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=2, sticky=W, padx=5, pady=8
        )
        group_combo = ttk.Combobox(
            course_grid,
            textvariable=self.var_group,
            values=["Select Group", "1", "2", "3", "4"],
            state="readonly",
            font=("Segoe UI", 10),
            bootstyle="primary",
            width=22
        )
        group_combo.current(0)
        group_combo.grid(row=0, column=3, padx=5, pady=8, sticky=W)

        # Year
        ttk.Label(course_grid, text="Year:", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky=W, padx=5, pady=8
        )
        year_combo = ttk.Combobox(
            course_grid,
            textvariable=self.var_year,
            values=["Select Year", "First Year", "Second Year", "Third Year", "Fourth Year"],
            state="readonly",
            font=("Segoe UI", 10),
            bootstyle="primary",
            width=22
        )
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=5, pady=8, sticky=W)

        # Semester
        ttk.Label(course_grid, text="Semester:", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=2, sticky=W, padx=5, pady=8
        )
        sem_combo = ttk.Combobox(
            course_grid,
            textvariable=self.var_sem,
            values=["Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"],
            state="readonly",
            font=("Segoe UI", 10),
            bootstyle="primary",
            width=22
        )
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=5, pady=8, sticky=W)

        # Student Information Section
        info_frame = ttk.Labelframe(
            left_panel,
            text="👤 Student Information",
            bootstyle="success",
            padding=15
        )
        info_frame.pack(fill=BOTH, expand=YES, pady=(0, 15))

        # Scrollable frame for student info
        info_canvas = Canvas(info_frame, highlightthickness=0)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=VERTICAL, command=info_canvas.yview, bootstyle="success-round")
        info_scrollable = ttk.Frame(info_canvas)

        info_scrollable.bind(
            "<Configure>",
            lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all"))
        )

        info_canvas.create_window((0, 0), window=info_scrollable, anchor="nw")
        info_canvas.configure(yscrollcommand=info_scrollbar.set)

        info_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        info_scrollbar.pack(side=RIGHT, fill=Y)

        # Student info fields
        fields = [
            ("Student ID:", self.var_std_id, None),
            ("Student Name:", self.var_std_name, None),
            ("Course:", self.var_course, ["Select Course", "BTech", "MBA", "MCA", "BScITM", "BArch"]),
            ("Registration No:", self.var_roll, None),
            ("Gender:", self.var_gender, ["Select Gender", "Male", "Female"]),
            ("Date of Birth:", self.var_dob, "DATE"),
            ("Email ID:", self.var_email, None),
            ("Phone Number:", self.var_phone, None),
            ("Address:", self.var_address, None),
            ("Proctor Name:", self.var_proctor, None),
        ]

        # Store DateEntry widget reference
        self.date_entry_widget = None

        for idx, field_data in enumerate(fields):
            label_text = field_data[0]
            var = field_data[1]
            values = field_data[2]

            row = idx // 2
            col = (idx % 2) * 2

            ttk.Label(
                info_scrollable,
                text=label_text,
                font=("Segoe UI", 9, "bold")
            ).grid(row=row, column=col, sticky=W, padx=5, pady=8)

            if values == "DATE":
                # Create DateEntry widget for Date of Birth
                self.date_entry_widget = DateEntry(
                    info_scrollable,
                    bootstyle="success",
                    dateformat="%Y-%m-%d"
                )
                self.date_entry_widget.grid(row=row, column=col + 1, padx=5, pady=8, sticky=W)

                # Bind the DateEntry to update the StringVar
                def update_dob_var(event=None):
                    try:
                        self.var_dob.set(self.date_entry_widget.entry.get())
                    except Exception as e:
                        print(f"DateEntry error: {e}")

                self.date_entry_widget.bind("<<DateEntrySelected>>", update_dob_var)
                self.date_entry_widget.entry.bind("<KeyRelease>", update_dob_var)

            elif values:
                widget = ttk.Combobox(
                    info_scrollable,
                    textvariable=var,
                    values=values,
                    state="readonly",
                    font=("Segoe UI", 10),
                    bootstyle="success",
                    width=20
                )
                if values[0].startswith("Select"):
                    widget.current(0)
                widget.grid(row=row, column=col + 1, padx=5, pady=8, sticky=W)
            else:
                widget = ttk.Entry(
                    info_scrollable,
                    textvariable=var,
                    font=("Segoe UI", 10),
                    bootstyle="success",
                    width=22
                )
                widget.grid(row=row, column=col + 1, padx=5, pady=8, sticky=W)

        # Photo Sample Radio Buttons
        photo_frame = ttk.Frame(info_scrollable)
        photo_frame.grid(row=5, column=0, columnspan=4, pady=15, sticky=W, padx=5)

        ttk.Label(
            photo_frame,
            text="📸 Photo Sample:",
            font=("Segoe UI", 10, "bold")
        ).pack(side=LEFT, padx=(0, 15))

        ttk.Radiobutton(
            photo_frame,
            text="Take Photo Sample",
            variable=self.var_radio1,
            value="Yes",
            bootstyle="success-toolbutton"
        ).pack(side=LEFT, padx=5)

        ttk.Radiobutton(
            photo_frame,
            text="No Photo Sample",
            variable=self.var_radio1,
            value="No",
            bootstyle="danger-toolbutton"
        ).pack(side=LEFT, padx=5)

        # Action Buttons with modern styling
        btn_frame1 = ttk.Frame(left_panel)
        btn_frame1.pack(fill=X, pady=(0, 10))

        buttons1 = [
            ("💾 Save", self.add_data, "success"),
            ("🔄 Update", self.update_data, "info"),
            ("🗑️ Delete", self.delete_data, "danger"),
            ("↺ Reset", self.reset_data, "warning"),
        ]

        for text, command, style in buttons1:
            ttk.Button(
                btn_frame1,
                text=text,
                command=command,
                bootstyle=f"{style}",
                width=15
            ).pack(side=LEFT, padx=5, expand=YES, fill=X)

        # Photo Buttons
        btn_frame2 = ttk.Frame(left_panel)
        btn_frame2.pack(fill=X)

        ttk.Button(
            btn_frame2,
            text="📷 Take Photo Sample",
            command=self.generate_dataset,
            bootstyle="primary",
            width=25
        ).pack(side=LEFT, padx=5, expand=YES, fill=X)

        ttk.Button(
            btn_frame2,
            text="🔄 Update Photo Sample",
            command=self.update_photo_sample,
            bootstyle="secondary",
            width=25
        ).pack(side=LEFT, padx=5, expand=YES, fill=X)

        # Right Panel - Student Records
        right_panel = ttk.Labelframe(
            content_frame,
            text="📋 Student Records",
            bootstyle="info",
            padding=15
        )
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Search Section
        search_frame = ttk.Labelframe(
            right_panel,
            text="🔍 Search System",
            bootstyle="warning",
            padding=15
        )
        search_frame.pack(fill=X, pady=(0, 15))

        search_grid = ttk.Frame(search_frame)
        search_grid.pack(fill=X)

        ttk.Label(
            search_grid,
            text="Search By:",
            font=("Segoe UI", 11, "bold")
        ).pack(side=LEFT, padx=(0, 10))

        search_combo = ttk.Combobox(
            search_grid,
            textvariable=self.var_search_by,
            values=["Select", "RegdNo", "PhoneNo"],
            state="readonly",
            font=("Segoe UI", 10),
            bootstyle="warning",
            width=12
        )
        search_combo.current(0)
        search_combo.pack(side=LEFT, padx=5)

        ttk.Entry(
            search_grid,
            textvariable=self.var_search_text,
            font=("Segoe UI", 10),
            bootstyle="warning",
            width=20
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            search_grid,
            text="🔎 Search",
            command=self.search_data,
            bootstyle="warning",
            width=12
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            search_grid,
            text="📄 Show All",
            command=self.fetch_data,
            bootstyle="info-outline",
            width=12
        ).pack(side=LEFT, padx=5)

        # Table Section
        table_frame = ttk.Frame(right_panel)
        table_frame.pack(fill=BOTH, expand=YES)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL, bootstyle="info-round")
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL, bootstyle="info-round")

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("dep", "group", "year", "sem", "id", "name", "course", "roll_no",
                     "gender", "dob", "email", "phone_no", "address", "proctor", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            bootstyle="info",
            height=15
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Configure columns
        columns_config = [
            ("dep", "Department", 120),
            ("group", "Group", 80),
            ("year", "Year", 100),
            ("sem", "Semester", 100),
            ("id", "Student ID", 100),
            ("name", "Name", 150),
            ("course", "Course", 100),
            ("roll_no", "Regd No", 120),
            ("gender", "Gender", 80),
            ("dob", "DOB", 100),
            ("email", "Email", 150),
            ("phone_no", "Phone", 120),
            ("address", "Address", 150),
            ("proctor", "Proctor", 120),
            ("photo", "Photo Status", 120),
        ]

        for col, heading, width in columns_config:
            self.student_table.heading(col, text=heading)
            self.student_table.column(col, width=width)

        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=YES)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        # Load data
        self.fetch_data()

    def _init_tts_engine(self):
        """Initialize TTS engine in background thread"""
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        except Exception as e:
            print(f"Could not set TTS voice: {e}")

    # ==================== Validation Function ====================
    def validate_inputs(self):
        """Validates all required fields before database operations."""
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "Department, Student Name, and Student ID are required fields.", parent=self.root)
            return False

        name_pattern = re.compile(r"^[a-zA-Z .'-]+$")

        student_name = self.var_std_name.get()
        if not name_pattern.match(student_name):
            messagebox.showerror("Invalid Input", "Student Name contains invalid characters.", parent=self.root)
            return False

        proctor_name = self.var_proctor.get()
        if proctor_name and not name_pattern.match(proctor_name):
            messagebox.showerror("Invalid Input", "Proctor Name contains invalid characters.", parent=self.root)
            return False

        if not self.var_std_id.get().isdigit():
            messagebox.showerror("Invalid Input", "Student ID must contain only numbers.", parent=self.root)
            return False

        if not (self.var_phone.get().isdigit() and len(self.var_phone.get()) == 10):
            messagebox.showerror("Invalid Input", "Phone Number must be exactly 10 digits.", parent=self.root)
            return False

        return True

    # ==================== TTS Functions ====================
    def _speak_thread(self, text):
        """Internal function to run the speech engine."""
        if not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech Error: {e}")

    def speak(self, text):
        """Speaks the given text in a non-blocking background thread."""
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()

    # ==================== FIXED: DOB Helper Function ====================
    def get_dob_value(self):
        """Returns proper DOB value or None for MySQL NULL"""
        dob = self.var_dob.get().strip()
        if dob == "" or dob.lower() == "none":
            return None
        return dob

    # ==================== Database Functions ====================
    def add_data(self):
        if not self.validate_inputs():
            return

        # FIXED: Get proper DOB value
        dob_value = self.get_dob_value()

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="Raza@Khan2002", database="face_recog")
            my_cursor = conn.cursor()
            my_cursor.execute("""
                INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.var_dep.get(), self.var_group.get(), self.var_year.get(), self.var_sem.get(),
                self.var_std_id.get(), self.var_std_name.get(), self.var_course.get(), self.var_roll.get(),
                self.var_gender.get(), dob_value, self.var_email.get(), self.var_phone.get(),
                self.var_address.get(), self.var_proctor.get(), self.var_radio1.get()
            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Student details successfully added", parent=self.root)
            self.speak("Student has been added successfully")
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="Raza@Khan2002", database="face_recog")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM student")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", END, values=i)
        conn.close()

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        if data:
            self.var_dep.set(data[0])
            self.var_group.set(data[1])
            self.var_year.set(data[2])
            self.var_sem.set(data[3])
            self.var_std_id.set(data[4])
            self.var_std_name.set(data[5])
            self.var_course.set(data[6])
            self.var_roll.set(data[7])
            self.var_gender.set(data[8])
            self.var_dob.set(data[9] if data[9] else "")

            # Update DateEntry widget when row is selected
            if self.date_entry_widget and data[9]:
                try:
                    self.date_entry_widget.entry.delete(0, END)
                    self.date_entry_widget.entry.insert(0, str(data[9]))
                except Exception as e:
                    print(f"Error updating DateEntry: {e}")

            self.var_email.set(data[10])
            self.var_phone.set(data[11])
            self.var_address.set(data[12])
            self.var_proctor.set(data[13])
            self.var_radio1.set(data[14])

    def update_data(self):
        if not self.validate_inputs():
            return

        # FIXED: Get proper DOB value
        dob_value = self.get_dob_value()

        try:
            Update = messagebox.askyesno("Update", "Do you want to update this student details?", parent=self.root)
            if Update:
                conn = mysql.connector.connect(host="localhost", user="root", password="Raza@Khan2002", database="face_recog")
                my_cursor = conn.cursor()
                my_cursor.execute("""
                    UPDATE student SET Department=%s, GroupNo=%s, YearNo=%s, Semester=%s, StudentName=%s,
                    Course=%s, RollNo=%s, Gender=%s, DOB=%s, Email=%s, PhoneNo=%s, Home_Address=%s,
                    Proctor=%s, PhotoSampleStatus=%s WHERE StudentID=%s
                """, (
                    self.var_dep.get(), self.var_group.get(), self.var_year.get(), self.var_sem.get(),
                    self.var_std_name.get(), self.var_course.get(), self.var_roll.get(), self.var_gender.get(),
                    dob_value, self.var_email.get(), self.var_phone.get(), self.var_address.get(),
                    self.var_proctor.get(), self.var_radio1.get(), self.var_std_id.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Student details successfully updated", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
        else:
            try:
                Delete = messagebox.askyesno("Student Delete Page", "Do you want to delete the student details?", parent=self.root)
                if Delete:
                    conn = mysql.connector.connect(host="localhost", user="root", password="Raza@Khan2002", database="face_recog")
                    my_cursor = conn.cursor()
                    sql = "DELETE FROM student WHERE StudentID=%s"
                    val = (self.var_std_id.get(),)
                    my_cursor.execute(sql, val)
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Delete", "Successfully deleted student details", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_group.set("Select Group")
        self.var_year.set("Select Year")
        self.var_sem.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_course.set("Select Course")
        self.var_roll.set("")
        self.var_gender.set("Select Gender")

        # Reset DateEntry widget
        if self.date_entry_widget:
            try:
                self.date_entry_widget.entry.delete(0, END)
            except Exception as e:
                print(f"Error resetting DateEntry: {e}")

        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_proctor.set("")
        self.var_radio1.set("")

    def search_data(self):
        """Searches the database based on the selected criteria."""
        search_by_display = self.var_search_by.get()
        search_text = self.var_search_text.get()

        if search_by_display == "Select" or search_text == "":
            messagebox.showerror("Error", "Please select a search option and enter text.", parent=self.root)
            return

        column_map = {"RegdNo": "RollNo", "PhoneNo": "PhoneNo"}
        search_by_db = column_map.get(search_by_display)

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="Raza@Khan2002", database="face_recog")
            my_cursor = conn.cursor()
            query = f"SELECT * FROM student WHERE {search_by_db} LIKE %s"
            value = ('%' + search_text + '%',)
            my_cursor.execute(query, value)
            data = my_cursor.fetchall()

            if len(data) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END, values=i)
            else:
                self.student_table.delete(*self.student_table.get_children())
                messagebox.showinfo("Info", "No matching records found.", parent=self.root)

            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # ==================== CV2 Functions ====================
    def generate_dataset(self):
        if not self.validate_inputs():
            return

        # FIXED: Get proper DOB value
        dob_value = self.get_dob_value()

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="Raza@Khan2002", database="face_recog")
            my_cursor = conn.cursor()
            my_cursor.execute("""
                UPDATE student SET Department=%s, GroupNo=%s, YearNo=%s, Semester=%s, StudentName=%s,
                Course=%s, RollNo=%s, Gender=%s, DOB=%s, Email=%s, PhoneNo=%s, Home_Address=%s,
                Proctor=%s, PhotoSampleStatus=%s WHERE StudentID=%s
            """, (
                self.var_dep.get(), self.var_group.get(), self.var_year.get(), self.var_sem.get(),
                self.var_std_name.get(), self.var_course.get(), self.var_roll.get(), self.var_gender.get(),
                dob_value, self.var_email.get(), self.var_phone.get(), self.var_address.get(),
                self.var_proctor.get(), "Yes", self.var_std_id.get()
            ))
            conn.commit()
            self.fetch_data()
            conn.close()


            # Face capture logic
            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            img_id = 0
            while True:
                ret, my_frame = cap.read()
                if face_cropped(my_frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(my_frame), (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                    if not os.path.exists("data"):
                        os.makedirs("data")

                    file_name_path = "data/user." + str(self.var_std_id.get()) + "." + str(img_id) + ".jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Your Face", face)


                if cv2.waitKey(1) == 13 or int(img_id) == 100:
                    break
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Generating data sets!!")
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)


    def update_photo_sample(self):
        """Deletes old photo samples and generates new set."""
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Please select a student first.", parent=self.root)
            return


        student_id = self.var_std_id.get()
        update_confirmation = messagebox.askyesno(
            "Confirm Update",
            f"This will delete all existing photos for Student ID {student_id}. Continue?",
            parent=self.root
        )


        if not update_confirmation:
            return


        try:
            # Delete old photos
            photo_path = "data/"
            deleted_count = 0
            if os.path.exists(photo_path):
                for file in os.listdir(photo_path):
                    if file.startswith(f"user.{student_id}."):
                        os.remove(os.path.join(photo_path, file))
                        deleted_count += 1

            if deleted_count > 0:
                messagebox.showinfo("Success", f"Deleted {deleted_count} old photo samples for Student ID {student_id}.", parent=self.root)

            # Call the main function to generate the new dataset
            self.generate_dataset()


        except Exception as es:
            messagebox.showerror("Error", f"An error occurred while updating photos: {str(es)}", parent=self.root)


    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        # Schedule this method to run again after 1000ms (1 second)
        self.time_lbl.after(1000, self.update_time)



if __name__ == "__main__":
    # --- Start with a theme (e.g., "vapor' for dark, 'litera' for light) ---
    root = ttk.Window(themename="vapor") 
    obj = Student(root)
    root.mainloop()