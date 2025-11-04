import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from time import strftime
from datetime import datetime
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from chatbot import UltimateGroqChatbot
from help_desk import HelpDesk


class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")

        self.root.state('zoomed') 
        self.root.minsize(1280, 720)
        self.style = tb.Style()


        # --- UI/UX FIX: NAMESPACED STYLES ---
        # 1. Define the font you want for the dashboard
        button_font = ("Segoe UI", 10, "bold") 
        

        self.style.configure('Dashboard.primary-outline.TButton', font=button_font)
        self.style.configure('Dashboard.info-outline.TButton', font=button_font)
        self.style.configure('Dashboard.success-outline.TButton', font=button_font)
        self.style.configure('Dashboard.warning-outline.TButton', font=button_font)
        
        # --- SENIOR UI/UX CHANGE ---
        # I've changed this style from .danger. to .danger-outline. 
        # to match your request for a hover-activated background.
        self.style.configure('Dashboard.danger-outline.TButton', font=button_font) 
        # --- END OF CHANGE ---
        
        # --- RESPONSIVE LAYOUT CONFIGURATION ---
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1) 

        # --- Header Images (Row 0) ---
        header_frame = tb.Frame(self.root, bootstyle="secondary")
        header_frame.grid(row=0, column=0, sticky="nsew")
        header_frame.columnconfigure((0, 1, 2), weight=1)


        try:
            img_pil_1 = Image.open(r"college images\image1.jpg").resize((500, 130), Image.Resampling.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img_pil_1)
            f_lbl1 = tb.Label(header_frame, image=self.photoimg1, bootstyle="secondary")
            f_lbl1.grid(row=0, column=0, sticky="w", padx=10, pady=5)


            img_pil_2 = Image.open(r"college images\image2.png").resize((900, 130), Image.Resampling.LANCZOS)
            self.photoimg2 = ImageTk.PhotoImage(img_pil_2)
            f_lbl2 = tb.Label(header_frame, image=self.photoimg2, bootstyle="secondary")
            f_lbl2.grid(row=0, column=1, sticky="n", pady=5)


            img_pil_3 = Image.open(r"college images\image3.jpg").resize((550, 130), Image.Resampling.LANCZOS)
            self.photoimg3 = ImageTk.PhotoImage(img_pil_3)
            f_lbl3 = tb.Label(header_frame, image=self.photoimg3, bootstyle="secondary")
            f_lbl3.grid(row=0, column=2, sticky="e", padx=10, pady=5)
        except Exception as e:
            print(f"Error loading header images: {e}")


        # --- Title Bar (Row 1) ---
        title_frame = tb.Frame(self.root, bootstyle="primary", padding=(10, 5))
        title_frame.grid(row=1, column=0, sticky="nsew")
        title_frame.columnconfigure(1, weight=1)


        # --- Time Label (left) ---
        self.time_lbl = tb.Label(
            title_frame,
            font=("Helvetica", 18, "bold"),
            bootstyle="primary-inverse"
        )
        self.time_lbl.pack(side=LEFT, padx=20)
        self.update_time()


        # --- Title Label (center) ---
        title_lbl = tb.Label(
            title_frame,
            text="FACE RECOGNITION ATTENDANCE SYSTEM",
            font=("Helvetica", 30, "bold"),
            bootstyle="primary-inverse",
            anchor=CENTER
        )
        title_lbl.pack(side=LEFT, expand=True, fill=X)

        # --- Button Dashboard (Row 2) ---
        dashboard_frame = tb.Frame(self.root, padding=20)
        dashboard_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configure a 2x4 grid that scales
        dashboard_frame.rowconfigure((0, 1), weight=1, uniform="row")
        dashboard_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="col")


        image_size = (340, 260) 
        btn_padding = 20 
        
        # --- Student Button ---
        try:
            img_pil_4 = Image.open(r"college images\student3.jpg").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg4 = ImageTk.PhotoImage(img_pil_4)
            student_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg4,
                text="Student Details",
                command=self.student_details,
                compound="top",
                bootstyle="primary-outline-dashboard", # --- UI/UX FIX: Use specific style
                padding=20
            )
            student_btn.grid(row=0, column=0, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading student button image: {e}")


        # --- Face Recognition Button ---
        try:
            img_pil_5 = Image.open(r"college images\face_dectected.png").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg5 = ImageTk.PhotoImage(img_pil_5)
            face_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg5,
                text="Face Detector",
                command=self.face_data, 
                compound="top",
                bootstyle="info-outline-dashboard", # --- UI/UX FIX: Use specific style
                padding=20
            )
            face_btn.grid(row=0, column=1, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading face detector button image: {e}")


        # --- Attendance Button ---
        try:
            img_pil_6 = Image.open(r"college images\generated-image.png").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg6 = ImageTk.PhotoImage(img_pil_6)
            attendance_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg6,
                text="Attendance",
                command=self.attendance,
                compound="top",
                bootstyle="success-outline-dashboard", # --- UI/UX FIX: Use specific style
                padding=20
            )
            attendance_btn.grid(row=0, column=2, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading attendance button image: {e}")


        # --- Chatbot Button ---
        try:
            img_pil_7 = Image.open(r"college images\chatbot img.png").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg7 = ImageTk.PhotoImage(img_pil_7)
            chatbot_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg7,
                text="Chatbot",
                command=self.chatbot,
                compound="top",
                bootstyle="warning-outline-dashboard", # --- UI/UX FIX: Use specific style
                padding=20
            )
            chatbot_btn.grid(row=0, column=3, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading chatbot button image: {e}")


        # --- Train Button ---
        try:
            img_pil_8 = Image.open(r"college images\traindata.png").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg8 = ImageTk.PhotoImage(img_pil_8)
            train_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg8,
                text="Train Data",
                command=self.train_data,
                compound="top",
                bootstyle="primary-outline-dashboard", # --- UI/UX FIX: Use specific style
                padding=20
            )
            train_btn.grid(row=1, column=0, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading train button image: {e}")

        # --- Photo Button ---
        try:
            img_pil_9 = Image.open(r"college images\traindata2.jpg").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg9 = ImageTk.PhotoImage(img_pil_9)
            photos_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg9,
                text="Photos",
                command=self.open_img,
                compound="top",
                bootstyle="info-outline-dashboard", # --- UI/UX FIX: Use specific style
                padding=20
            )
            photos_btn.grid(row=1, column=1, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading photos button image: {e}")


        # --- Help Desk Button ---
        try:
            img_pil_10 = Image.open(r"college images\help desk.png").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg10 = ImageTk.PhotoImage(img_pil_10)
            help_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg10,
                text="Help Desk",
                command=self.help_desk,
                compound="top",
                bootstyle="success-outline-dashboard", # --- UI/UX FIX: Use specific style
                padding=20
            )
            help_btn.grid(row=1, column=2, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading help button image: {e}")


        # --- Exit Button ---
        try:
            img_pil_11 = Image.open(r"college images\exit.jpg").resize(image_size, Image.Resampling.LANCZOS)
            self.photoimg11 = ImageTk.PhotoImage(img_pil_11)
            exit_btn = tb.Button(
                dashboard_frame,
                image=self.photoimg11,
                command=self.exit_app, 
                compound="top",
                # --- SENIOR UI/UX CHANGE ---
                # I've changed this from 'danger-dashboard' to 'danger-outline-dashboard'
                # to match your request and ensure UI consistency.
                bootstyle="danger-outline-dashboard", 
                # --- END OF CHANGE ---
                padding=20
            )
            exit_btn.grid(row=1, column=3, sticky="nsew", padx=btn_padding, pady=btn_padding)
        except Exception as e:
            print(f"Error loading exit button image: {e}")


    
    def toggle_theme(self):
        """Toggle Light/Dark appearance at runtime."""
        new_theme = self.theme_var.get()
        self.style.theme_use(new_theme)


    def open_img(self):
        try:
            os.startfile("data")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open 'data' folder: {e}", parent=self.root)


    def exit_app(self):
        answer = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root)
        if answer:
            self.root.destroy()
        else:
            return
    def student_details(self):
        self.new_window = tb.Toplevel(self.root) 
        self.app = Student(self.new_window)


    def train_data(self):
        self.new_window = tb.Toplevel(self.root) 
        self.app = Train(self.new_window)


    def face_data(self):
        self.new_window = tb.Toplevel(self.root) 
        self.app = Face_Recognition(self.new_window)


    def attendance(self):
        self.new_window = tb.Toplevel(self.root) 
        self.app = Attendance(self.new_window)


    def help_desk(self):
        self.new_window = tb.Toplevel(self.root) 
        self.app = HelpDesk(self.new_window)


    def chatbot(self):
        self.new_window = tb.Toplevel(self.root) 
        self.app = UltimateGroqChatbot(self.new_window)


    # --- Time update function (Logic Unchanged) ---
    def update_time(self):
        """Fetches the current time and updates the time label."""
        string = strftime('%I:%M:%S %p') # Changed to 12-hour format for a friendlier look
        self.time_lbl.config(text=string)
        self.time_lbl.after(1000, self.update_time)



if __name__ == "__main__":
    # --- Start with a theme (e.g., 'vapor' for dark, 'litera' for light) ---
    root = tb.Window(themename="vapor") 
    obj = Face_Recognition_System(root)
    root.mainloop()