import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import * # Still needed for messagebox/filedialog
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2  # Not used in this file, but kept from original imports
import os
from datetime import datetime
from time import strftime
import csv

class Attendance:
    def __init__(self, root):
        self.root = root
        
        # --- UI/UX CHANGE: Set window to open maximized ---
        self.root.state('zoomed')
        self.root.minsize(1280, 720)
        self.root.title("Attendance Management System")

        self.mydata = []
        
        self.var_atten_id = StringVar()
        self.var_atten_roll = StringVar()
        self.var_atten_name = StringVar()
        self.var_atten_dep = StringVar()
        self.var_atten_time = StringVar()
        self.var_atten_date = StringVar()
        self.var_atten_attendance = StringVar()
        
        # --- UI/UX CHANGE: Load original PIL images for resizing ---
        try:
            self.original_img_top_left = Image.open(r"college images\student1.webp")
        except Exception as e:
            print(f"Error loading student1.webp: {e}")
            self.original_img_top_left = None

        try:
            self.original_img_top_right = Image.open(r"college images\students.png")
        except Exception as e:
            print(f"Error loading students.png: {e}")
            self.original_img_top_right = None
            

        # Store PhotoImage references
        self.photoimg_top_left = None
        self.photoimg_top_right = None
        self.photoimg_left_panel = None

        # --- UI/UX CHANGE: Header frame (replicates 50/50 split) ---
        header_frame = ttk.Frame(self.root, height=200)
        header_frame.pack(side=TOP, fill=X)
        header_frame.pack_propagate(False) # Force height to 200px

        # Left 50% of header
        self.left_header_label = ttk.Label(header_frame)
        self.left_header_label.place(relx=0, rely=0, relwidth=0.5, relheight=1.0)
        self.left_header_label.bind("<Configure>", lambda e: self.resize_image(e, self.original_img_top_left, self.left_header_label))

        # Right 50% of header
        self.right_header_label = ttk.Label(header_frame)
        self.right_header_label.place(relx=0.5, rely=0, relwidth=0.5, relheight=1.0)
        self.right_header_label.bind("<Configure>", lambda e: self.resize_image(e, self.original_img_top_right, self.right_header_label))

        # --- UI/UX CHANGE: Modern Title Bar (replaces old title) ---
        title_frame = ttk.Frame(self.root, bootstyle="primary")
        title_frame.pack(side=TOP, fill=X)
        
        self.time_lbl = ttk.Label(
            title_frame, 
            font=("Segoe UI", 16, "bold"), 
            bootstyle="inverse-primary"
        )
        self.time_lbl.pack(side=RIGHT, padx=20, pady=10) 
        self.update_time()

        title_lbl = ttk.Label(
            title_frame, 
            text="ATTENDANCE MANAGEMENT SYSTEM",
            font=("Segoe UI", 24, "bold"), 
            bootstyle="inverse-primary"
        )
        title_lbl.pack(side=LEFT, padx=20, pady=10)

        # --- UI/UX CHANGE: Main content frame (replaces bg_img and main_frame) ---
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        # Configure a 50/50 responsive grid
        main_frame.columnconfigure((0, 1), weight=1, uniform="group1")
        main_frame.rowconfigure(0, weight=1)

        # --- UI/UX CHANGE: Left label frame (modernized) ---
        Left_frame = ttk.LabelFrame(
            main_frame, 
            text="Student Attendance Details", 
            bootstyle="info"
        )
        Left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        Left_frame.rowconfigure(1, weight=1) # Let the entry frame grow
        Left_frame.columnconfigure(0, weight=1) # Let content fill width
        # --- UI/UX CHANGE: Left inside frame (modernized) ---
        left_inside_frame = ttk.Frame(Left_frame, padding=10)
        left_inside_frame.grid(row=1, column=0, sticky="nsew", padx=5)

        # Configure responsive grid
        left_inside_frame.columnconfigure((1, 3), weight=1)

        # --- UI/UX CHANGE: Modernized Labels and Entries ---
        # attendanceid 
        attendance_id = ttk.Label(left_inside_frame, text="Attendance ID:", font=("Segoe UI", 12, "bold"))
        attendance_id.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        attendance_id_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_id, font=("Segoe UI", 12), bootstyle="info")
        attendance_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # name 
        name = ttk.Label(left_inside_frame, text="Name:", font=("Segoe UI", 12, "bold"))
        name.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        name_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_name, font=("Segoe UI", 12), bootstyle="info")
        name_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        # roll 
        roll = ttk.Label(left_inside_frame, text="Regd No:", font=("Segoe UI", 12, "bold"))
        roll.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        roll_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_roll, font=("Segoe UI", 12), bootstyle="info")
        roll_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # department
        dep = ttk.Label(left_inside_frame, text="Department:", font=("Segoe UI", 12, "bold"))
        dep.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        dep_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_dep, font=("Segoe UI", 12), bootstyle="info")
        dep_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        # date
        date = ttk.Label(left_inside_frame, text="Date:", font=("Segoe UI", 12, "bold"))
        date.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        date_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_date, font=("Segoe UI", 12), bootstyle="info")
        date_entry.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        
        # time
        time_label = ttk.Label(left_inside_frame, text="Time:", font=("Segoe UI", 12, "bold"))
        time_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        time_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_time, font=("Segoe UI", 12), bootstyle="info")
        time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # attendance 
        attendance = ttk.Label(left_inside_frame, text="Attendance:", font=("Segoe UI", 12, "bold"))
        attendance.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        self.atten_status = ttk.Combobox(left_inside_frame, textvariable=self.var_atten_attendance, font=("Segoe UI", 12), state="readonly", bootstyle="info")
        self.atten_status["values"] = ("Status", "Present", "Absent")
        self.atten_status.current(0)
        self.atten_status.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        # --- UI/UX CHANGE: Modernized button frame (at bottom of left panel) ---
        btn_frame = ttk.Frame(Left_frame)
        btn_frame.grid(row=2, column=0, sticky="sew", padx=10, pady=10)
        
        save_btn = ttk.Button(btn_frame, text="Import CSV", command=self.importCsv, bootstyle="primary-outline")
        save_btn.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        update_btn = ttk.Button(btn_frame, text="Export CSV", command=self.exportCsv, bootstyle="info-outline") 
        update_btn.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Update", command=self.update_data, bootstyle="warning-outline")
        delete_btn.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_data, bootstyle="danger-outline")
        reset_btn.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # --- UI/UX CHANGE: Right label frame (modernized) ---
        right_frame = ttk.LabelFrame(
            main_frame, 
            text="Attendance Details", 
            bootstyle="info"
        )
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # --- UI/UX CHANGE: Modernized table and scrollbars ---
        table_frame = ttk.Frame(right_frame)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL, bootstyle="info-round")
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL, bootstyle="info-round")
        
        self.AttendanceReportTable = ttk.Treeview(
            table_frame,
            column=("id", "roll", "name", "department", "time", "date", "attendance"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            bootstyle="info"
        )    
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)
        
        self.AttendanceReportTable.heading("id", text="Attendance ID")
        self.AttendanceReportTable.heading("roll", text="Name")
        self.AttendanceReportTable.heading("name", text="Regd No")
        self.AttendanceReportTable.heading("department", text="Department")
        self.AttendanceReportTable.heading("time", text="Time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Attendance")
        
        self.AttendanceReportTable["show"] = "headings"
        
        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("roll", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("department", width=100)
        self.AttendanceReportTable.column("time", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)
        
        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)
        
        
    # --- UI/UX CHANGE: New method to handle responsive image resizing ---
    def resize_image(self, event, original_image, label, max_height=None):
        """Resizes any image to fit its container label."""
        if not original_image:
            return
            
        width = event.width
        height = event.height
        
        # Use provided max_height if specified (for the left panel image)
        if max_height and height > max_height:
            height = max_height
        
        # Prevent resizing to 1x1 on minimize
        if width < 2 or height < 2:
            return
            
        try:
            img = original_image.resize((width, height), Image.Resampling.LANCZOS)
            
            # Store the new PhotoImage as an attribute to prevent garbage collection
            # We need unique attributes for each label
            if label == self.left_header_label:
                self.photoimg_top_left = ImageTk.PhotoImage(img)
                label.config(image=self.photoimg_top_left)
            elif label == self.right_header_label:
                self.photoimg_top_right = ImageTk.PhotoImage(img)
                label.config(image=self.photoimg_top_right)
            elif label == self.f_lbl_left:
                self.photoimg_left_panel = ImageTk.PhotoImage(img)
                label.config(image=self.photoimg_left_panel)
        except Exception as e:
            print(f"Error resizing image: {e}")
            
            
    # ===============================================fetch data (LOGIC UNCHANGED) ===========================
    def fetchData(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("", END, values=i)
            
    # ===============================================import csv (LOGIC UNCHANGED) ===========================
    def importCsv(self):
        try:
            self.mydata.clear()
            fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
            if fln: 
                with open(fln, newline='') as myfile:
                    csvread = csv.reader(myfile, delimiter=",")
                    next(csvread, None)
                    for i in csvread:
                        self.mydata.append(i)
                self.fetchData(self.mydata)
        except Exception as es:
            messagebox.showerror("Error", f"Error reading CSV file: {str(es)}", parent=self.root)
            
    # ===============================================export csv (LOGIC UNCHANGED) ===========================
    def exportCsv(self):
        try:
            if len(self.mydata) < 1:
                messagebox.showerror("No Data", "No data found to export", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
            if fln:
                with open(fln, mode="w", newline="") as myfile:
                    exp_write = csv.writer(myfile, delimiter=",")
                    exp_write.writerow(["Attendance ID", "Roll No", "Name", "Department", "Time", "Date", "Attendance"])
                    for i in self.mydata:
                        exp_write.writerow(i)
                messagebox.showinfo("Data Exported", f"Your data has been exported to {os.path.basename(fln)} successfully", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error exporting CSV file: {str(es)}", parent=self.root)
            
    # ===============================================get_cursor (LOGIC UNCHANGED) ===========================
    def get_cursor(self, event=""):
        try:
            cursor_row = self.AttendanceReportTable.focus()
            content = self.AttendanceReportTable.item(cursor_row)
            row = content["values"]
            self.var_atten_id.set(row[0])
            self.var_atten_roll.set(row[1])
            self.var_atten_name.set(row[2])
            self.var_atten_dep.set(row[3])
            self.var_atten_time.set(row[4])
            self.var_atten_date.set(row[5])
            self.var_atten_attendance.set(row[6])
        except IndexError:
            pass 
        
    # ===============================================reset_data (LOGIC UNCHANGED) ===========================
    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("Status")
        
    # ===============================================update_data (LOGIC UNCHANGED) ===========================
    def update_data(self):
        id = self.var_atten_id.get()
        roll = self.var_atten_roll.get()
        name = self.var_atten_name.get()
        dep = self.var_atten_dep.get()
        time = self.var_atten_time.get()
        date = self.var_atten_date.get()
        attendance = self.var_atten_attendance.get()

        selected_item = self.AttendanceReportTable.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record from the table to update.", parent=self.root)
            return

        try:
            self.AttendanceReportTable.item(selected_item, values=(id, roll, name, dep, time, date, attendance))

            for index, row in enumerate(self.mydata):
                if row[0] == id:
                    self.mydata[index] = [id, roll, name, dep, time, date, attendance]
                    break
            
            messagebox.showinfo("Success", "Attendance record has been updated.", parent=self.root)
            
        except Exception as es:
            messagebox.showerror("Error", f"An error occurred during update: {str(es)}", parent=self.root)
        
        
    # ===============================================update_time (LOGIC UNCHANGED) ===========================
    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%H:%M:%S %p')
        self.time_lbl.config(text=string)
        self.time_lbl.after(1000, self.update_time)
        
        
if __name__ == "__main__":
    # --- UI/UX CHANGE: Use ttk.Window and a theme ---
    root = ttk.Window(themename="vapor") 
    obj = Attendance(root)
    root.mainloop()